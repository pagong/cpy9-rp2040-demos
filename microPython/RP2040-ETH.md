## Example code for RP2040-ETH in MicroPython

## The internal connection between CH9120 and RP2040:

| CH9120 pins | RP2040 pins | Function |
| --- | --- | --- |
| RXD | GP21 | Serial data input |
| TXD | GP20 | Serial data output |
| TCPCS | GP17 | In TCP client mode, indicates connection status, low level for successful connection |
| CFG0 | GP18 | Network configuration enabled pin, low level for serial debugging mode |
| RSTI | GP19 |	Reset, active LOW |

