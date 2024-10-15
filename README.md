# cpy9-rp2040-demos
CircuitPython demos running on various RP2040 based boards.

## Raspberry Pi Pico
[This](media/Raspberry-Pi-Pico-H-details-7.jpg) is the original **Pico** with Micro-USB port and 2MB flash.

- RGB matrix
  - Analog [clock](rgb-matrix/clocks/analog.py), uses "displayio" and Adafruit's "turtle" graphics
  - German Word [clock](rgb-matrix/clocks/word-de.py). Inspired by an English word [clock](rgb-matrix/clocks/word-en.py), by [VtechOps](https://adafruit-playground.com/u/VPTechOps/pages/rgb-matrix-word-clocks). 
- NEOpixel matrix
  - Fire [demo](neopixel/fire/fire12.py), based on [Fire2012](https://blog.kriegsman.org/2014/04/04/fire2012-an-open-source-fire-simulation-for-arduino-and-leds/) algorithm by Mark Kriegsman
 
## Raspberry Pi Pico-W
[This](media/Raspberry-Pi-Pico-W-details-17.jpg) is the enhanced **Pico** with Micro-USB port, 2MB flash and an onboard WiFi chip.

## WaveShare RP2040-Matrix
[This](media/RP2040-Matrix-details-9.jpg) is a tiny **Pico** [clone](http://www.waveshare.com/wiki/RP2040-Matrix) with USB-C port, 2MB flash and a 5x5 NEOpixel matrix.

- Rainbow [demo](neopixel/rainbow/rainbow7.py), based on an Adafruit example
- Fire [demo](neopixel/fire/fire8.py), also based on the Fire2012 algorithm by Mark Kriegsman

## WaveShare RP2040-Zero
[This](media/RP2040-Zero-details-7.jpg) is a tiny **Pico** [clone](http://www.waveshare.com/wiki/RP2040-Zero) with USB-C port, 2MB flash and a single NEOpixel.

## WaveShare RP2040-One
[This](media/RP2040-One-details-9.jpg) is a tiny **Pico** [clone](http://www.waveshare.com/wiki/RP2040-One) with USB-A port, 4MB flash and a single NEOpixel.

## WaveShare RP2040-ETH
[This](media/RP2040-ETH-details-inter.jpg) is a tiny **Pico** [clone](http://www.waveshare.com/wiki/RP2040-ETH) with USB-C port, 4MB flash and an onboard Ethernet interface.

- some usage [hints](microPython/RP2040-ETH.md)

## WaveShare RP2040-LCD-0.96
[This](media/RP2040-LCD-0.96-details-7.jpg) is a tiny **Pico** [clone](http://www.waveshare.com/wiki/RP2040-LCD-0.96) with USB-C port, 2MB flash and a 160x80 pixel colorful LCD display.

- some LCD demos (by [richteel](https://github.com/richteel/Waveshare-RP2040-LCD-0.96))

## VCC-GND YD-RP2040
[This](media/YD-2040-PIN.png) is a **Pico** [clone](https://sites.google.com/view/raspberrypibuenosaires/yd-rp2040-16mb) with USB-C port, 16MB flash, user button and a single NEOpixel.

- Pico DVI
  - Slide show [demo](pico-dvi/slide-show/slide-show.py). The "YD-RP2040" has 15MB free on the `CIRCUITPY` drive, which is great for a slide show. But you need to install the CircuitPython firmware for the "Raspberry Pi" **Pico**, as the "picodvi" module is only included there.

# YubiKey simulator
See this [repo](https://github.com/pagong/cpy9-rp2040-yksim)

