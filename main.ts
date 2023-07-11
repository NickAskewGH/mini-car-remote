radio.setGroup(22)
radio.setTransmitPower(7)
basic.showIcon(IconNames.Target)
loops.everyInterval(50, function () {
    radio.sendValue("x", input.acceleration(Dimension.X))
    radio.sendValue("y", input.acceleration(Dimension.Y))
})
basic.forever(function () {
	
})
