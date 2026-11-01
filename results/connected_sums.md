# Indices of connected sums

Script `connected_sums.py` (see its docstring). The bound is ind(K1) + ind(K2) - 1 (graft of two minimal diagrams).

| knot | F (bound) | F3 (bound) | Fvec (bound) | F3vec (bound) |
|---|---|---|---|---|
| 3_1 # 3_1 (granny knot) | **8** (9) | **5** (7) | 17 (17) | **5** (9) |
| 3_1 # 3_1^m (square knot) | 9 (9) | **6** (7) | **13** (17) | **7** (9) |
| 3_1 # 4_1 | **9** (11) | **6** (8) | **13** (15) | **7** (9) |

Bold: the inequality is strict.

## Witnesses

Normal form (x_i: generators of F; y_i: generators of F_3, with y_{2m} = iota(x_m), see make_table.py) and tree diagram (leaf addresses of the top and bottom trees).

- 3_1 # 3_1 (granny knot) in F, n = 8 (7 diagrams in the class, 7 of 7 checked): `x1 x2 x4 x5^-1 x3^-1 x0^-3`; trees `0,100,1010,1011,1100,1101,1110,1111 | 0000,0001,001,010,011,100,101,11`
- 3_1 # 3_1 (granny knot) in F3, n = 5 (1 diagrams in the class, 1 of 1 checked): `y2 y5^-1 y1^-2`; trees `0,1,200,201,202,21,220,221,222 | 0,100,101,102,11,120,121,122,2`
- 3_1 # 3_1 (granny knot) in Fvec, n = 17 (15962 diagrams in the class, 8 of 8 checked): `x3 x4 x7 x8^3 x9^2 x10 x12 x11^-1 x10^-3 x5^-1 x4^-2 x3^-2 x2^-2 x1^-2 x0^-1`; trees `0,10,110,11100,111010,111011,11110,1111100,1111101000,111110100100,1111101001010,1111101001011,111110100110,111110100111,111110101,11111011,111111 | 00,0100,010100,01010100,0101010100,01010101010,01010101011,010101011,0101011,01011,011000,0110010,0110011,01101,0111,10,11`
- 3_1 # 3_1 (granny knot) in F3vec, n = 5 (1 diagrams in the class, 1 of 1 checked): `y2 y5^-1 y1^-2`; trees `0,1,200,201,202,21,220,221,222 | 0,100,101,102,11,120,121,122,2`
- 3_1 # 3_1^m (square knot) in F, n = 9 (140 diagrams in the class, 8 of 8 checked): `x2^3 x3 x6^-1 x4^-1 x1^-3 x0^-2`; trees `0,10,110000,1100010,1100011,11001,1101,1110,1111 | 000,001000,001001,00101,00110,00111,010,011,1`
- 3_1 # 3_1^m (square knot) in F3, n = 6 (16 diagrams in the class, 8 of 8 checked): `y4 y7 y5^-1 y1^-3`; trees `0,1,20,21,2200,2201,2202,2210,2211,2212,222 | 0,1000,1001,1002,101,1020,1021,1022,11,12,2`
- 3_1 # 3_1^m (square knot) in Fvec, n = 13 (41 diagrams in the class, 8 of 8 checked): `x1 x2 x4^2 x5 x7^2 x8 x10 x6^-1 x5^-2 x4^-2 x3^-2 x1^-1 x0^-3`; trees `0,100,1010,1011,11000,110010,110011,110100,1101010,1101011,110110,110111,111 | 0000,00010,00011,00100,0010100,001010100,0010101010,0010101011,00101011,001011,0011,01,1`
- 3_1 # 3_1^m (square knot) in F3vec, n = 7 (34 diagrams in the class, 8 of 8 checked): `y3 y6 y8 y7^-1 y4^-1 y0^-1`; trees `0,1,20,210,211,212,2200,2201,22020,22021,22022,221,222 | 00,01,02,1,200,201,202,210,211,212,220,221,222`
- 3_1 # 4_1 in F, n = 9 (34 diagrams in the class, 8 of 8 checked): `x1 x2^2 x3^2 x4 x2^-2 x0^-2`; trees `0,100,10100,1010100,10101010,10101011,101011,1011,11 | 000,001,0100,0101,011,10,110,1110,1111`
- 3_1 # 4_1 in F3, n = 6 (14 diagrams in the class, 8 of 8 checked): `y2 y6 y7^-1 y3^-2 y0^-1`; trees `0,1,200,201,202,21,2200,2201,2202,221,222 | 00,01,02,100,101,102,11,120,121,122,2`
- 3_1 # 4_1 in Fvec, n = 13 (150 diagrams in the class, 8 of 8 checked): `x1^2 x2 x4^2 x5 x9 x10 x8^-1 x7^-2 x3^-1 x2^-2 x1^-2 x0^-2`; trees `0,1000,10010,10011,10100,101010,101011,1011,110,11100,111010,111011,1111 | 000,00100,0010100,00101010,00101011,001011,0011,0100,01010,01011,011,10,11`
- 3_1 # 4_1 in F3vec, n = 7 (25 diagrams in the class, 8 of 8 checked): `y6 y9 y7^-1 y4^-1 y1^-2`; trees `0,1,20,21,220,221,22200,22201,22202,22210,22211,22212,2222 | 0,100,101,102,110,111,112,120,121,122,20,21,22`
