# ---------------------------------------------------------------------------------------
# -- Données brutees : f70300020007b15e
# -- Request
# -- * slave    : 247
# -- * function :  3 Read Holding Registers
# --   * starting address : 0x0002 (2)  R&W Température de consigne zone Ecran
# --   * quantity         : 7
# ---------------------------------------------------------------------------------------
# -- Données brutees : f7030e000041a0cccd41980001000000009a1a
# -- Response
# -- * slave    : 247
# -- * function :  3 Read Holding Registers
# --   * byte count       : 14
# --   * registers values : [  0000 41A0     CCCD 4198      0001     0000     0000  ]
# --                        [<Temp Zone 1> <Temp Zone 2>  <PAC ON>  <FROID > <BOOST >]
# --                        [                            <!PAC OFF> <!CHAUD> < !ECO >]
# ---------------------------------------------------------------------------------------