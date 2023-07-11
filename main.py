radio.set_group(22)
radio.set_transmit_power(7)

def on_forever():
    pass
basic.forever(on_forever)

def on_every_interval():
    radio.send_value("x", input.acceleration(Dimension.X))
    radio.send_value("y", input.acceleration(Dimension.Y))
loops.every_interval(100, on_every_interval)
