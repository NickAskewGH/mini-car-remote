# Technical notes

## Source reconciliation

The current MakeCode representations disagree on one important parameter:

| Representation | Radio group | TX power | Interval |
| --- | ---: | ---: | ---: |
| `main.blocks` | 20 | 7 | 50 ms |
| `main.ts` | 20 | 7 | 50 ms |
| `main.py` | 22 | 7 | 50 ms |

`pxt.json` declares `blocksprj` as the preferred editor. Since Blocks and TypeScript agree, group **20** is treated as authoritative for current documentation.

The discrepancy should be rechecked if the project is reopened/saved in MakeCode. A regenerated Python representation may resolve it automatically; until then, do not silently assume group 22 is intentional.

## Startup

The Blocks/TypeScript implementation performs:

```text
radio.setGroup(20)
radio.setTransmitPower(7)
show Target icon
```

There is no pairing/discovery handshake with the car receiver.

## Sampling and transport

A MakeCode `loops.everyInterval(50, ...)` callback reads X and Y and sends them separately using `radio.sendValue`.

The two values therefore do not form an atomic packet. A receiver can observe a new X paired temporarily with an older Y, depending on scheduling, packet delivery and its own receive logic.

For a simple toy/demo this may be acceptable. For more deterministic control, a future protocol could add a sequence number or package both axes into one application-level sample.

## Accelerometer semantics

The transmitter sends MakeCode accelerometer values directly.

It does not:

- normalize to a -1..1 control range;
- establish a neutral calibration;
- apply a dead zone;
- low-pass filter hand movement/noise;
- clamp to a receiver-specific motor command;
- invert or remap axes for vehicle orientation.

Those choices belong to the receiver/control design unless this transmitter is deliberately evolved.

## Radio power

Transmit power is set to 7, MakeCode's highest selectable radio power level. Higher power is not equivalent to guaranteed delivery: interference, range, orientation and receiver scheduling can still cause loss.

## Receiver contract implied by this repository

A compatible receiver needs at minimum:

- radio group 20;
- handlers for named values `x` and `y`;
- a defined mapping from accelerometer values to steering/drive behaviour.

For a moving car, the receiver should additionally implement a timeout that returns motors to a safe state if fresh control data stops arriving.

Because X and Y are separate messages, the receiver should also decide whether receiving either axis refreshes the failsafe timer or whether it requires sufficiently recent values for both.

## Verification status

`test.ts` contains only the generated placeholder comment. No behavioural tests are present.

A useful manual verification procedure is:

1. build/flash the transmitter using a compatible MakeCode/PXT environment;
2. use a second micro:bit/test receiver on **group 20** to display/log received named values;
3. verify the Target startup icon;
4. verify approximately 20 X/Y sampling cycles per second;
5. tilt through positive/negative X and Y and confirm the received signs/ranges;
6. introduce radio loss (power off or move transmitter away) and verify the **receiver** enters its intended safe state;
7. re-open/save the transmitter in MakeCode and check whether `main.py` regenerates to group 20;
8. only then test against a powered vehicle, initially with wheels lifted or otherwise unable to cause unintended motion.

A successful transmitter build does not validate receiver safety.

## Generated project infrastructure

The repository includes standard MakeCode project scaffolding such as `_config.yml`, `Gemfile`, `.gitignore`, `.vscode/`, and `tsconfig.json`. These support editing/building/presentation and do not define the radio-control protocol.
