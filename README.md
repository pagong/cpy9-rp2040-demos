# cpy9-rp2040-demos
CircuitPython demos running on various RP2040 based boards.

## Raspberry Pi Pico
[This](media/Raspberry-Pi-Pico-H-details-7.jpg) is the original **Pico** with Micro-USB port and 2MB flash.

- RGB matrix
  - Analog [clock](rgb-matrix/clocks/analog.py), uses `displayio` and Adafruit's `turtle` graphics
  - German Word [clock](rgb-matrix/clocks/word-de.py). Inspired by an English Word [clock](rgb-matrix/clocks/word-en.py), by [VPTechOps](https://adafruit-playground.com/u/VPTechOps/pages/rgb-matrix-word-clocks). 
- NEOpixel matrix
  - Fire [demo](neopixel/fire/fire12.py), based on [Fire2012](https://blog.kriegsman.org/2014/04/04/fire2012-an-open-source-fire-simulation-for-arduino-and-leds/) algorithm by Mark Kriegsman
- Pico-LCD-0.96

## Raspberry Pi Pico-W
[This](media/Raspberry-Pi-Pico-W-details-17.jpg) is the enhanced **Pico** with Micro-USB port, 2MB flash and an onboard WiFi chip.

- The following GPIO pins are used for communicating with the WLAN chip (CYW43439):
  - GP23 - wifi power
  - GP24 - SPI data
  - GP25 - SPI CS
  - GP29 - SPI clock

## WaveShare RP2040-Matrix
[This](media/RP2040-Matrix-details-9.jpg) is a tiny **Pico** [clone](http://www.waveshare.com/wiki/RP2040-Matrix) with USB-C port, 2MB flash and a 5x5 NEOpixel matrix.

- Tiny rainbow [demo](neopixel/rainbow/rainbow7.py), based on an Adafruit example
- Tiny fire [demo](neopixel/fire/fire8.py), also based on the Fire2012 algorithm by Mark Kriegsman

## WaveShare RP2040-Zero
[This](media/RP2040-Zero-details-7.jpg) is a tiny **Pico** [clone](http://www.waveshare.com/wiki/RP2040-Zero) with USB-C port, 2MB flash and a single NEOpixel.

## WaveShare RP2040-One
[This](media/RP2040-One-details-9.jpg) is a tiny **Pico** [clone](http://www.waveshare.com/wiki/RP2040-One) with USB-A port, 4MB flash and a single NEOpixel.

## WaveShare RP2040-ETH
[This](media/RP2040-ETH-details-inter.jpg) is a tiny **Pico** [clone](http://www.waveshare.com/wiki/RP2040-ETH) with USB-C port, 4MB flash and an onboard Ethernet interface.

- some usage [hints](microPython/RP2040-ETH.md)

## WaveShare RP2040-LCD-0.96
[This](media/RP2040-LCD-0.96-details-7.jpg) is a tiny **Pico** [clone](http://www.waveshare.com/wiki/RP2040-LCD-0.96) with USB-C port, 2MB flash and a 160x80 pixel colorful LCD display. Additionally a Li-Ion charger is available.

- some LCD demos (by [richteel](https://github.com/richteel/Waveshare-RP2040-LCD-0.96)); use `adafruit_st7735r` as display driver

## WaveShare RP2040-LCD-1.28
[This](media/RP2040-LCD-1.28_Spec01.jpg) is a tiny **Pico** [clone](https://www.waveshare.com/wiki/RP2040-LCD-1.28) with USB-C port, 2MB flash and a round 240x240 pixel colorful LCD display. Additionally a 6-axis sensor and a Li-Ion charger are available.

- are these supported by CPy9??
  - LCD module: GC9A01A
  - 6 axis sensor: QMI8658A 
- Demos on Github
  - Clock demo (by [Daniel Wienzek](https://github.com/dawigit/picoclock))
  - Boilerplate demo (by [Philipp Molitor](https://github.com/PhilippMolitor/waveshare-rp2040-roundlcd-boilerplate))

## VCC-GND YD-RP2040
[This](media/YD-2040-PIN.png) is a **Pico** [clone](https://sites.google.com/view/raspberrypibuenosaires/yd-rp2040-16mb) with USB-C port, 16MB flash, user button and a single NEOpixel.

- Pico DVI
  - Slide show [demo](pico-dvi/dvi-sock/slide-show.py). The "YD-RP2040" has 15MB free on the `CIRCUITPY` drive, which is great for a slide show. But you need to install the CircuitPython firmware for the "Raspberry Pi" **Pico**, as the `picodvi` module is only included there.

## WaveShare RP2040-PiZero
[This](media/RP2040-PiZero-Schematic.pdf) is a **Pico** [clone](http://www.waveshare.com/wiki/RP2040-PiZero) with size and features similar to the Raspberry Pi Zero. The board has two USB-C ports, a mini-HDMI port which can be used with the `picodvi` module and a SD card slot.

- Pico DVI
  - Blinking Circles [demo](pico-dvi/pi-zero/plusses.py), by Tod Kurt
  - Spirograph [demo](pico-dvi/pi-zero/spiro.py), also by Tod Kurt

# Hardware Add-Ons

## DVI-Sock
[This](media/DVISockfrRaspberryPiPico-130853.jpg) is an add-on board for the **Pico** which uses an HDMI connector to send DVI signals to a digital monitor.

## WaveShare Pico-LCD-0.96
[This](media/Pico-LCD-0.96-details-inter.jpg) is an add-on board for the **Pico** with a 4-wire LCD (ST7735S), a digital joystick and 2 user buttons. See the [wiki](https://www.waveshare.com/wiki/Pico-LCD-0.96) for more details.

- pin-out of the 4-wire LCD is similar to the RP2040-LCD-0.96; use `adafruit_st7735r` as display driver

# YubiKey simulator
See this [repo](https://github.com/pagong/cpy9-rp2040-yksim)


