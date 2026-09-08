# micro:bit mini-car remote

A small BBC micro:bit MakeCode transmitter intended to act as a tilt remote for a radio-controlled mini-car project.

Every 50 ms the firmware reads the micro:bit accelerometer and broadcasts the raw X and Y acceleration values as named MakeCode radio values. A separate receiver/car project is required to interpret those values and drive motors; **this repository contains only the remote/transmitter side**.

The implementation dates from July 2023. This documentation describes the files currently present on `master` and does not imply that the historical MakeCode target or radio behaviour has been revalidated with current tooling.

## Behaviour

On startup the authoritative Blocks/TypeScript program:

1. selects MakeCode radio group **20**;
2. sets transmit power to **7** (the maximum MakeCode radio power setting);
3. displays the **Target** icon.

It then runs a 50 ms periodic task:

```text
radio.sendValue("x", acceleration X)
radio.sendValue("y", acceleration Y)
```

This nominally produces 20 sampling cycles per second, with two radio datagrams per cycle.

The values are raw MakeCode accelerometer readings. This transmitter performs no scaling, dead-zone processing, smoothing, calibration or motor mixing.

## Radio protocol

The receiver must use the same MakeCode radio group and understand two named integer values:

| Name | Value |
| --- | --- |
| `x` | `input.acceleration(Dimension.X)` |
| `y` | `input.acceleration(Dimension.Y)` |

The transmitter does not send sequence numbers, timestamps, heartbeats, acknowledgements or an explicit neutral/stop command.

That matters for a vehicle receiver: loss-of-radio/failsafe behaviour must be implemented by the receiver rather than inferred from this transmitter.

## Source authority

The repository contains MakeCode Blocks, TypeScript and Python representations, but they are currently inconsistent.

`main.blocks` and `main.ts` both configure **radio group 20**.

`main.py` configures **radio group 22**:

```python
radio.set_group(22)
```

All three otherwise represent the same basic 50 ms X/Y transmitter.

Because `pxt.json` specifies `blocksprj` as the preferred editor and Blocks/TypeScript agree, this documentation treats **`main.blocks` + `main.ts` as the current behavioural authority**. Group **20** is therefore the documented transmitter group.

Do not configure a receiver from `main.py` without first resolving/regenerating that stale representation.

## Platform

`pxt.json` currently records:

- package name: `mini-car-remote`
- MakeCode target: BBC micro:bit
- target version: `6.0.15`
- preferred editor: `blocksprj`
- dependencies: `core`, `radio`, and `microphone`

There are no third-party MakeCode extensions in this project.

## Editing in MakeCode

To edit the project:

1. Open the MakeCode micro:bit editor.
2. Choose **Import** → **Import URL**.
3. Enter the GitHub repository URL for `NickAskewGH/mini-car-remote`.

Prefer editing through MakeCode and review all generated representations after saving, particularly the existing group-20/group-22 discrepancy.

## PXT command line

The Makefile provides:

```bash
make build    # pxt build
make deploy   # pxt deploy
make test     # pxt test
```

A compatible MakeCode/PXT environment must already be installed. The repository does not pin the Node/PXT toolchain.

`test.ts` is only a placeholder, so `make test` is not evidence of behavioural coverage.

## Vehicle safety considerations

This repository transmits control input but contains **no receiver-side failsafe**.

Any car/robot receiver using these packets should independently define safe behaviour for:

- radio timeout/loss;
- stale X/Y values;
- receiver startup before the transmitter is available;
- malformed/unexpected values;
- neutral/dead-zone handling;
- maximum motor output;
- emergency/manual stop.

Do not rely on continued receipt of this transmitter's packets as the sole safety mechanism for a moving vehicle.

## Repository structure

- `main.blocks` — authoritative Blocks representation.
- `main.ts` — matching TypeScript representation.
- `main.py` — stale/inconsistent Python representation (radio group 22).
- `pxt.json` — MakeCode target/dependency/editor metadata.
- `Makefile` — thin PXT build/deploy/test wrappers.
- `test.ts` — placeholder test file.
- `_config.yml` / `Gemfile` — generated GitHub Pages/Jekyll support.
- `.vscode/` — editor convenience settings.

## Known limitations

- Transmitter-only repository; the receiver/car implementation is not present here.
- Experimental 2023 project with no current release/versioning policy.
- No substantive automated tests.
- No repository evidence of current hardware/toolchain revalidation.
- `main.py` disagrees with Blocks/TypeScript about the radio group.
- Raw accelerometer values are sent without filtering or calibration.
- X and Y are separate radio messages rather than one atomic sample.
- No sequence/timestamp or packet-loss detection.
- No transmitter-side explicit stop/failsafe message.
- No documented receiver protocol beyond the X/Y values visible in this source.

## Further technical documentation

See [`docs/technical-notes.md`](docs/technical-notes.md) for protocol implications, source reconciliation and a manual verification checklist.
