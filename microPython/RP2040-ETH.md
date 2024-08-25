## Example code for RP2040-ETH in MicroPython

- examples from WaveShare wiki: [Demo](RP2040-ETH-Demo/) and [MQTT](RP2040-ETH-MQTT/)
- Github examples by [nichokap](https://github.com/nichokap/RP2040-ETH)

- documentation by the chip manufacturer [WCH](https://www.wch-ic.com/products/CH9120.html)
- download specs from [here](https://www.wch-ic.com/search?q=CH9120&t=downloads)


## The internal connection between CH9120 and RP2040:

| CH9120 pins | RP2040 pins | Function |
| --- | --- | --- |
| RXD | GP21 | Serial data input |
| TXD | GP20 | Serial data output |
| TCPCS | GP17 | In TCP client mode, indicates connection status, low level for successful connection |
| CFG0 | GP18 | Network configuration enabled pin, low level for serial debugging mode |
| RSTI | GP19 |	Reset, active LOW |


## Code and documentation for Pico-ETH-CH9121

- WaveShare [site](https://www.waveshare.com/pico-eth-ch9121.htm) and [wiki](https://www.waveshare.com/wiki/Pico-ETH-CH9121) and [examples](CH9121/)

- Github examples by [Danielerikrust](https://github.com/Danielerikrust/CH9121)
- Github examples by [Splashaudio](https://github.com/Splashaudio/Pico-ETH-CH9121_basic)


