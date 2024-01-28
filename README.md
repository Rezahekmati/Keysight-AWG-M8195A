# Keysight-AWG-M8195A
Control Keysight AWG 8195A with Python

### Notes:
- I used "Keysight M8195A Arbitrary Waveform Generator Revision 2", Edition 7.0, March 2019
- For connection, socket is being used, but you can use VISA. In the future, I will add VISA connection to the code.
- Make sure to change the IP address/port.
- Please refer to "Functions tracker.xlsx" to see developed functions.
- Only "6.20 CARRier Subsystem" section and two functions in section "6.21 :TRACe Subsystem" are not being developed.

### Caution:
- This code has not been tested on a hardware yet.

### Useful & related codes:
While working on this project, I found following codes very useful:
- for M8195A_Connection:
  - [socketscpi](https://github.com/morgan-at-keysight/socketscpi/tree/master)
  - [M8195A_scripts](https://github.com/acidbourbon/M8195A_scripts)
- for M8195_Configuration:
  - [SchusterLab](https://github.com/SchusterLab/slab/tree/master)

___
**Drop me an email if you have any queries.** 