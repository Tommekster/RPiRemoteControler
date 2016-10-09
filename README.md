# RPiRemoteControler
I want to control Raspbery Pi via TV's infra-red remote controler and a component TSOP4836.

## Hardware
	/-----------[===]--+----\
	|     +--+      R  |    |
	\3v3--|oo|-- 5v   === C |       +---+
	 02 --|oo|-- 5v    |    \--VCC--|3  |\
	 03 --|oo|---GND---+-------GND--|2  | )
	 04 --|oo|-- 14     /------OUT--|1  |/
	GND --|oo|-- 15    /            +---+
	 17 --|oo|---18---/        TSOP4836
	 27 --|oo|-- GND
	 22 --|oo|-- 23
	3v3 --|oo|-- 24
	 10 --|oo|-- GND
	 09 --|oo|-- 25
	 11 --|oo|-- 08
	GND --|oo|-- 07
	IDSD--|oo|-- ID_SC
	 05 --|oo|-- GND
	 06 --|oo|-- 12
	 13 --|oo|-- GND
	 19 --|oo|-- 16
	 26 --|oo|-- 20
	GND --|oo|-- 21
	      +--+

