# Certified verification of the F3-index table

Script `certify_indices.py` (exact or certified methods only, see its docstring).

- exclusions (diagrams certified not to be the knot): {'crossings': 15824, 'volume': 10781, 'canonical': 687, 'hfk': 1079}
- witnesses (diagrams certified to be the knot): {'knotinfo': 7, 'canonical': 11309}
- **contradictions with the table: 0**
- not certified: 4; crashed tasks: 1

## Not certified

- ('witnesses', '13n_4587', '0,1,20,210,21100,21101,21102,2111,2112,2120,2121,2122,220,2210,2211,2212,222', '0,10,1100,1101,1102,1110,1111,111200,111201,111202,111210,111211,111212,11122,112,12,2', 'K not hyperbolic')
- ('witnesses', '13n_4639', '0,1,20,2100,21010,21011,21012,21020,210210,210211,210212,21022,211,2120,2121,2122,22', '000,0010,0011,0012,002,010,011,012,02,10,11,1200,1201,1202,121,122,2', 'K not hyperbolic')
- ('witnesses', '12n_839', '0,1,20,210,211,2120,21210,21211,212120,2121210,2121211,2121212,2121220,2121221,2121222,2122,22', '0000,00010,00011,00012,00020,00021,00022,001,002,01,02,10,11,12,20,21,22', 'timeout (180 s)')
- ('witnesses', '12a_1022', '0,1,20,21,2200,2201,220200,22020100,22020101,22020102,2202011,2202012,220202,22021,22022,221,222', '00,0100,0101,0102,011,012,02,1,20,210,211,21200,21201,21202,2121,2122,22', 'timeout (180 s)')

## Crashed tasks

- ['F3', '13a_3949']

