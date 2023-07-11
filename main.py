radio.set_group(22)
radio.set_transmit_power(7)
basic.show_icon(IconNames.TARGET)

def on_every_interval():
    radio.send_value("x", input.acceleration(Dimension.X))
    radio.send_value("y", input.acceleration(Dimension.Y))
loops.every_interval(50, on_every_interval)
