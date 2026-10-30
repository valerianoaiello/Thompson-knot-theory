# Oriented vec{F}-index of the non-invertible knots

Non-invertible knots of KnotInfo with <= 13 crossings whose HOMFLY class appears at n <= 17; every tree diagram of vec{F} of those classes with n <= 17 was compared with the oriented KnotInfo diagram K (oriented_scan.py). K = KnotInfo orientation, Kr = reverse, Km = mirror image, Kmr = both. index(K) = index(Kmr) and index(Kr) = index(Km) (L(g^-1) is the mirror image of the reverse of L(g)); for invertible knots all four values equal the index of results/Fvec_index.csv.

Rule for g^-1 checked directly on 2426 diagrams: ok. Chunks skipped because they crash SnapPy: 0. min(index K, index Kr) differs from the unoriented table for: none.

| knot | symmetry | first n of HOMFLY | table (unoriented) | K | Kr | Km | Kmr | verdict |
|---|---|---|---|---|---|---|---|---|
| 8_17 | negative amphicheiral | 13 | 13 | 13 | 13 | 13 | 13 | equal |
| 9_32 | chiral | 15 | 15 | 15 | 15 | 15 | 15 | equal |
| 9_33 | chiral | 13 | 13 | 13 | 13 | 13 | 13 | equal |
| 10_81 | negative amphicheiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 10_82 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 10_83 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 10_84 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 10_86 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 10_87 | chiral | 15 | 15 | 15 | 15 | 15 | 15 | equal |
| 10_88 | negative amphicheiral | 13 | 13 | 15 | 13 | 13 | 15 | DIFFERENT |
| 10_90 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 10_91 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 10_93 | chiral | 15 | 15 | 15 | 17 | 17 | 15 | DIFFERENT |
| 10_94 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 10_95 | chiral | 17 | 17 | 17 | > 17 | > 17 | 17 | DIFFERENT |
| 10_102 | chiral | 15 | 15 | 15 | 17 | 17 | 15 | DIFFERENT |
| 10_106 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 10_107 | chiral | 15 | 15 | 15 | 15 | 15 | 15 | equal |
| 10_110 | chiral | 15 | 15 | 15 | 15 | 15 | 15 | equal |
| 10_115 | negative amphicheiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 10_117 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 10_118 | negative amphicheiral | 15 | 15 | 15 | 15 | 15 | 15 | equal |
| 10_119 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 10_147 | chiral | 15 | 15 | 15 | 15 | 15 | 15 | equal |
| 10_148 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 10_150 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 10_151 | chiral | 13 | 13 | 13 | 13 | 13 | 13 | equal |
| 10_153 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 11a_15 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 11a_17 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 11a_19 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 11a_26 | chiral | 15 | 15 | 17 | 15 | 15 | 17 | DIFFERENT |
| 11a_28 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 11a_29 | chiral | 15 | 15 | 15 | 15 | 15 | 15 | equal |
| 11a_30 | chiral | 15 | 15 | 17 | 15 | 15 | 17 | DIFFERENT |
| 11a_38 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 11a_52 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 11a_66 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 11a_67 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 11a_68 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 11a_69 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 11a_70 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 11a_71 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 11a_72 | chiral | 15 | 15 | 15 | 15 | 15 | 15 | equal |
| 11a_76 | chiral | 15 | 15 | 15 | 17 | 17 | 15 | DIFFERENT |
| 11a_79 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 11a_80 | chiral | 15 | 15 | 15 | 15 | 15 | 15 | equal |
| 11a_81 | chiral | 15 | 15 | 15 | 15 | 15 | 15 | equal |
| 11a_102 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 11a_103 | chiral | 15 | 15 | 17 | 15 | 15 | 17 | DIFFERENT |
| 11a_104 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 11a_112 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 11a_115 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 11a_125 | chiral | 17 | 17 | 17 | > 17 | > 17 | 17 | DIFFERENT |
| 11a_131 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 11a_132 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 11a_137 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 11a_138 | chiral | 15 | 17 | 17 | 17 | 17 | 17 | equal |
| 11a_141 | chiral | 15 | 15 | 15 | 15 | 15 | 15 | equal |
| 11a_146 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 11a_147 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 11a_149 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 11a_151 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 11a_152 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 11a_157 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 11a_162 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 11a_163 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 11a_164 | chiral | 15 | 15 | 15 | 15 | 15 | 15 | equal |
| 11a_167 | chiral | 15 | 15 | 15 | 15 | 15 | 15 | equal |
| 11a_168 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 11a_169 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 11a_172 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 11a_187 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 11a_189 | chiral | 15 | 15 | 15 | 15 | 15 | 15 | equal |
| 11a_199 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 11a_201 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 11a_209 | chiral | 15 | 15 | 15 | 15 | 15 | 15 | equal |
| 11a_216 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 11a_217 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 11a_218 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 11a_232 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 11a_233 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 11a_252 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 11a_253 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 11a_256 | chiral | 15 | 15 | 15 | 17 | 17 | 15 | DIFFERENT |
| 11a_264 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 11a_265 | chiral | 15 | 17 | 17 | 17 | 17 | 17 | equal |
| 11a_267 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 11a_268 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 11a_269 | chiral | 15 | 15 | 15 | 15 | 15 | 15 | equal |
| 11a_270 | chiral | 15 | 15 | 15 | 17 | 17 | 15 | DIFFERENT |
| 11a_272 | chiral | 15 | 15 | 15 | 15 | 15 | 15 | equal |
| 11a_274 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 11a_282 | chiral | 15 | 15 | 15 | 15 | 15 | 15 | equal |
| 11a_284 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 11a_286 | chiral | 15 | 15 | 15 | 15 | 15 | 15 | equal |
| 11a_287 | chiral | 15 | 15 | 17 | 15 | 15 | 17 | DIFFERENT |
| 11a_289 | chiral | 15 | 15 | 15 | 15 | 15 | 15 | equal |
| 11a_290 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 11a_300 | chiral | 15 | 15 | 15 | 15 | 15 | 15 | equal |
| 11a_301 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 11a_303 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 11a_315 | chiral | 15 | 15 | 15 | 15 | 15 | 15 | equal |
| 11a_316 | chiral | 17 | 17 | > 17 | 17 | 17 | > 17 | DIFFERENT |
| 11a_322 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 11a_323 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 11a_326 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 11a_331 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 11n_4 | chiral | 15 | 15 | 15 | 15 | 15 | 15 | equal |
| 11n_5 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 11n_6 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 11n_7 | chiral | 15 | 15 | 15 | 15 | 15 | 15 | equal |
| 11n_11 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 11n_21 | chiral | 15 | 15 | 15 | 15 | 15 | 15 | equal |
| 11n_24 | chiral | 15 | 15 | 15 | 15 | 15 | 15 | equal |
| 11n_25 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 11n_26 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 11n_32 | chiral | 13 | 13 | 13 | 13 | 13 | 13 | equal |
| 11n_33 | chiral | 13 | 13 | 13 | 13 | 13 | 13 | equal |
| 11n_37 | chiral | 15 | 15 | 15 | 15 | 15 | 15 | equal |
| 11n_39 | chiral | 15 | 15 | 15 | 15 | 15 | 15 | equal |
| 11n_42 | chiral | 15 | 15 | 15 | 15 | 15 | 15 | equal |
| 11n_44 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 11n_50 | chiral | 15 | 17 | 17 | 17 | 17 | 17 | equal |
| 11n_67 | chiral | 15 | 15 | 15 | 17 | 17 | 15 | DIFFERENT |
| 11n_68 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 11n_80 | chiral | 17 | 17 | > 17 | 17 | 17 | > 17 | DIFFERENT |
| 11n_97 | chiral | 15 | 15 | 15 | 15 | 15 | 15 | equal |
| 11n_100 | chiral | 13 | 13 | 13 | 13 | 13 | 13 | equal |
| 11n_110 | chiral | 15 | 15 | 15 | 15 | 15 | 15 | equal |
| 11n_114 | chiral | 15 | 15 | 15 | 15 | 15 | 15 | equal |
| 11n_116 | chiral | 15 | 15 | 15 | 15 | 15 | 15 | equal |
| 11n_120 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 11n_124 | chiral | 13 | 13 | 13 | 13 | 13 | 13 | equal |
| 11n_128 | chiral | 15 | 15 | 15 | 15 | 15 | 15 | equal |
| 11n_129 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 11n_130 | chiral | 15 | 15 | 15 | 15 | 15 | 15 | equal |
| 11n_131 | chiral | 15 | 15 | 15 | 15 | 15 | 15 | equal |
| 11n_132 | chiral | 15 | 15 | 15 | 17 | 17 | 15 | DIFFERENT |
| 11n_139 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 11n_151 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 11n_154 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 11n_160 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 11n_172 | chiral | 15 | 15 | 15 | 15 | 15 | 15 | equal |
| 11n_177 | chiral | 15 | 15 | 15 | 17 | 17 | 15 | DIFFERENT |
| 12a_1 | chiral | 15 | 15 | 17 | 15 | 15 | 17 | DIFFERENT |
| 12a_2 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 12a_4 | negative amphicheiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 12a_6 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 12a_8 | chiral | 17 | 17 | > 17 | 17 | 17 | > 17 | DIFFERENT |
| 12a_13 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 12a_15 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 12a_23 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 12a_48 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 12a_57 | chiral | 17 | 17 | 17 | > 17 | > 17 | 17 | DIFFERENT |
| 12a_58 | negative amphicheiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 12a_61 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 12a_66 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 12a_68 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 12a_71 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 12a_72 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 12a_125 | negative amphicheiral | 15 | 15 | 15 | 15 | 15 | 15 | equal |
| 12a_126 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 12a_131 | chiral | 17 | 17 | 17 | > 17 | > 17 | 17 | DIFFERENT |
| 12a_133 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 12a_135 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 12a_136 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 12a_137 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 12a_138 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 12a_139 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 12a_140 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 12a_155 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 12a_184 | chiral | 15 | 15 | 15 | 15 | 15 | 15 | equal |
| 12a_185 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 12a_189 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 12a_198 | chiral | 15 | 15 | 15 | 15 | 15 | 15 | equal |
| 12a_202 | chiral | 15 | 15 | 17 | 15 | 15 | 17 | DIFFERENT |
| 12a_213 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 12a_214 | chiral | 15 | 15 | 15 | 17 | 17 | 15 | DIFFERENT |
| 12a_222 | chiral | 15 | 15 | 15 | 15 | 15 | 15 | equal |
| 12a_224 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 12a_228 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 12a_233 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 12a_261 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 12a_262 | chiral | 15 | 15 | 15 | 17 | 17 | 15 | DIFFERENT |
| 12a_268 | negative amphicheiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 12a_272 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 12a_282 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 12a_283 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 12a_284 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 12a_285 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 12a_286 | chiral | 15 | 15 | 17 | 15 | 15 | 17 | DIFFERENT |
| 12a_301 | chiral | 17 | 17 | 17 | > 17 | > 17 | 17 | DIFFERENT |
| 12a_308 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 12a_309 | chiral | 15 | 17 | 17 | 17 | 17 | 17 | equal |
| 12a_310 | chiral | 15 | 17 | 17 | 17 | 17 | 17 | equal |
| 12a_316 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 12a_328 | chiral | 17 | 17 | > 17 | 17 | 17 | > 17 | DIFFERENT |
| 12a_333 | chiral | 15 | 17 | 17 | 17 | 17 | 17 | equal |
| 12a_334 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 12a_341 | negative amphicheiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 12a_342 | chiral | 15 | 15 | 17 | 15 | 15 | 17 | DIFFERENT |
| 12a_348 | chiral | 15 | 15 | 15 | 15 | 15 | 15 | equal |
| 12a_351 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 12a_360 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 12a_361 | chiral | 15 | 15 | 17 | 15 | 15 | 17 | DIFFERENT |
| 12a_377 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 12a_387 | chiral | 15 | 15 | 15 | 17 | 17 | 15 | DIFFERENT |
| 12a_388 | chiral | 15 | 15 | 17 | 15 | 15 | 17 | DIFFERENT |
| 12a_402 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 12a_403 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 12a_404 | chiral | 15 | 15 | 15 | 15 | 15 | 15 | equal |
| 12a_415 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 12a_416 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 12a_418 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 12a_419 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 12a_427 | positive amphicheiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 12a_439 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 12a_446 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 12a_451 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 12a_452 | chiral | 17 | 17 | > 17 | 17 | 17 | > 17 | DIFFERENT |
| 12a_455 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 12a_456 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 12a_457 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 12a_458 | negative amphicheiral | 15 | 17 | 17 | 17 | 17 | 17 | equal |
| 12a_464 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 12a_465 | negative amphicheiral | 17 | 17 | 17 | > 17 | > 17 | 17 | DIFFERENT |
| 12a_469 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 12a_473 | chiral | 15 | 15 | 15 | 15 | 15 | 15 | equal |
| 12a_479 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 12a_484 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 12a_488 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 12a_492 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 12a_529 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 12a_555 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 12a_560 | chiral | 17 | 17 | 17 | > 17 | > 17 | 17 | DIFFERENT |
| 12a_627 | negative amphicheiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 12a_635 | chiral | 17 | 17 | > 17 | 17 | 17 | > 17 | DIFFERENT |
| 12a_670 | chiral | 17 | 17 | 17 | > 17 | > 17 | 17 | DIFFERENT |
| 12a_674 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 12a_696 | chiral | 15 | 15 | 15 | 15 | 15 | 15 | equal |
| 12a_697 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 12a_698 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 12a_699 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 12a_707 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 12a_709 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 12a_711 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 12a_782 | chiral | 15 | 17 | 17 | 17 | 17 | 17 | equal |
| 12a_818 | chiral | 17 | 17 | > 17 | 17 | 17 | > 17 | DIFFERENT |
| 12a_865 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 12a_867 | chiral | 15 | 15 | 15 | 15 | 15 | 15 | equal |
| 12a_887 | negative amphicheiral | 15 | 15 | 15 | 15 | 15 | 15 | equal |
| 12a_888 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 12a_889 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 12a_894 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 12a_913 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 12a_928 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 12a_932 | chiral | 15 | 15 | 15 | 17 | 17 | 15 | DIFFERENT |
| 12a_935 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 12a_951 | chiral | 17 | 17 | > 17 | 17 | 17 | > 17 | DIFFERENT |
| 12a_961 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 12a_964 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 12a_965 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 12a_990 | negative amphicheiral | 17 | 17 | > 17 | 17 | 17 | > 17 | DIFFERENT |
| 12a_992 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 12a_1065 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 12a_1070 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 12a_1076 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 12a_1087 | chiral | 17 | 17 | 17 | > 17 | > 17 | 17 | DIFFERENT |
| 12a_1096 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 12a_1102 | negative amphicheiral | 15 | 15 | 15 | 17 | 17 | 15 | DIFFERENT |
| 12a_1122 | chiral | 17 | 17 | > 17 | 17 | 17 | > 17 | DIFFERENT |
| 12a_1124 | negative amphicheiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 12a_1152 | negative amphicheiral | 15 | 17 | 17 | 17 | 17 | 17 | equal |
| 12a_1188 | negative amphicheiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 12a_1195 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 12a_1211 | negative amphicheiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 12a_1249 | negative amphicheiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 12n_1 | chiral | 15 | 15 | 15 | 15 | 15 | 15 | equal |
| 12n_2 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 12n_3 | chiral | 15 | 15 | 15 | 17 | 17 | 15 | DIFFERENT |
| 12n_4 | chiral | 15 | 15 | 15 | 15 | 15 | 15 | equal |
| 12n_7 | chiral | 15 | 15 | 15 | 15 | 15 | 15 | equal |
| 12n_10 | chiral | 15 | 15 | 15 | 15 | 15 | 15 | equal |
| 12n_14 | chiral | 15 | 15 | 15 | 15 | 15 | 15 | equal |
| 12n_17 | chiral | 15 | 15 | 15 | 15 | 15 | 15 | equal |
| 12n_18 | chiral | 13 | 13 | 15 | 13 | 13 | 15 | DIFFERENT |
| 12n_19 | chiral | 15 | 15 | 15 | 17 | 17 | 15 | DIFFERENT |
| 12n_20 | chiral | 15 | 15 | 15 | 15 | 15 | 15 | equal |
| 12n_22 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 12n_23 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 12n_24 | chiral | 15 | 15 | 15 | 15 | 15 | 15 | equal |
| 12n_26 | chiral | 15 | 15 | 15 | 15 | 15 | 15 | equal |
| 12n_27 | chiral | 15 | 17 | 17 | 17 | 17 | 17 | equal |
| 12n_28 | chiral | 17 | 17 | > 17 | 17 | 17 | > 17 | DIFFERENT |
| 12n_30 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 12n_31 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 12n_32 | chiral | 15 | 17 | 17 | 17 | 17 | 17 | equal |
| 12n_33 | chiral | 15 | 15 | 17 | 15 | 15 | 17 | DIFFERENT |
| 12n_34 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 12n_49 | chiral | 13 | 13 | 15 | 13 | 13 | 15 | DIFFERENT |
| 12n_50 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 12n_51 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 12n_69 | chiral | 15 | 17 | > 17 | 17 | 17 | > 17 | DIFFERENT |
| 12n_73 | chiral | 15 | 15 | 15 | 15 | 15 | 15 | equal |
| 12n_84 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 12n_95 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 12n_97 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 12n_109 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 12n_111 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 12n_119 | chiral | 15 | 15 | 15 | 15 | 15 | 15 | equal |
| 12n_124 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 12n_129 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 12n_141 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 12n_173 | chiral | 15 | 17 | 17 | 17 | 17 | 17 | equal |
| 12n_174 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 12n_180 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 12n_181 | chiral | 17 | 17 | > 17 | 17 | 17 | > 17 | DIFFERENT |
| 12n_182 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 12n_189 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 12n_197 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 12n_216 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 12n_265 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 12n_266 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 12n_268 | chiral | 15 | 15 | 17 | 15 | 15 | 17 | DIFFERENT |
| 12n_275 | chiral | 15 | 15 | 15 | 15 | 15 | 15 | equal |
| 12n_278 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 12n_281 | chiral | 15 | 15 | 15 | 17 | 17 | 15 | DIFFERENT |
| 12n_286 | chiral | 15 | 15 | 15 | 15 | 15 | 15 | equal |
| 12n_298 | chiral | 15 | 15 | 15 | 15 | 15 | 15 | equal |
| 12n_312 | chiral | 15 | 15 | 15 | 15 | 15 | 15 | equal |
| 12n_313 | chiral | 15 | 15 | 15 | 15 | 15 | 15 | equal |
| 12n_315 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 12n_317 | chiral | 17 | 17 | > 17 | 17 | 17 | > 17 | DIFFERENT |
| 12n_319 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 12n_320 | chiral | 15 | 17 | 17 | 17 | 17 | 17 | equal |
| 12n_322 | chiral | 15 | 17 | 17 | 17 | 17 | 17 | equal |
| 12n_323 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 12n_325 | chiral | 15 | 15 | 17 | 15 | 15 | 17 | DIFFERENT |
| 12n_334 | chiral | 17 | 17 | > 17 | 17 | 17 | > 17 | DIFFERENT |
| 12n_335 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 12n_337 | chiral | 15 | 15 | 15 | 15 | 15 | 15 | equal |
| 12n_351 | chiral | 15 | 15 | 17 | 15 | 15 | 17 | DIFFERENT |
| 12n_356 | negative amphicheiral | 13 | 13 | 13 | 13 | 13 | 13 | equal |
| 12n_357 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 12n_358 | chiral | 15 | 15 | 15 | 15 | 15 | 15 | equal |
| 12n_359 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 12n_360 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 12n_362 | chiral | 15 | 15 | 15 | 15 | 15 | 15 | equal |
| 12n_364 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 12n_365 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 12n_367 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 12n_376 | chiral | 17 | 17 | 17 | > 17 | > 17 | 17 | DIFFERENT |
| 12n_382 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 12n_385 | chiral | 15 | 15 | 15 | 15 | 15 | 15 | equal |
| 12n_390 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 12n_393 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 12n_396 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 12n_399 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 12n_408 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 12n_410 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 12n_412 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 12n_413 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 12n_415 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 12n_421 | chiral | 15 | 15 | 15 | 15 | 15 | 15 | equal |
| 12n_422 | chiral | 15 | 17 | 17 | 17 | 17 | 17 | equal |
| 12n_423 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 12n_424 | chiral | 15 | 17 | 17 | 17 | 17 | 17 | equal |
| 12n_430 | chiral | 15 | 15 | 15 | 15 | 15 | 15 | equal |
| 12n_431 | chiral | 15 | 15 | 15 | 15 | 15 | 15 | equal |
| 12n_434 | chiral | 15 | 15 | 15 | 15 | 15 | 15 | equal |
| 12n_435 | chiral | 15 | 15 | 17 | 15 | 15 | 17 | DIFFERENT |
| 12n_440 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 12n_444 | chiral | 15 | 15 | 17 | 15 | 15 | 17 | DIFFERENT |
| 12n_447 | chiral | 15 | 17 | 17 | 17 | 17 | 17 | equal |
| 12n_448 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 12n_461 | chiral | 15 | 15 | 15 | 15 | 15 | 15 | equal |
| 12n_462 | negative amphicheiral | 11 | 15 | 15 | 15 | 15 | 15 | equal |
| 12n_463 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 12n_465 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 12n_484 | chiral | 15 | 15 | 15 | 15 | 15 | 15 | equal |
| 12n_485 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 12n_491 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 12n_492 | chiral | 15 | 15 | 17 | 15 | 15 | 17 | DIFFERENT |
| 12n_493 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 12n_504 | chiral | 15 | 15 | 15 | 17 | 17 | 15 | DIFFERENT |
| 12n_506 | chiral | 15 | 17 | 17 | 17 | 17 | 17 | equal |
| 12n_517 | chiral | 17 | 17 | 17 | > 17 | > 17 | 17 | DIFFERENT |
| 12n_529 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 12n_530 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 12n_531 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 12n_532 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 12n_534 | chiral | 15 | 15 | 15 | 15 | 15 | 15 | equal |
| 12n_536 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 12n_539 | chiral | 15 | 15 | 15 | 15 | 15 | 15 | equal |
| 12n_540 | chiral | 15 | 17 | 17 | 17 | 17 | 17 | equal |
| 12n_541 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 12n_561 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 12n_562 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 12n_566 | chiral | 17 | 17 | > 17 | 17 | 17 | > 17 | DIFFERENT |
| 12n_584 | chiral | 15 | 15 | 15 | 15 | 15 | 15 | equal |
| 12n_586 | chiral | 13 | 15 | 15 | 15 | 15 | 15 | equal |
| 12n_588 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 12n_599 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 12n_608 | chiral | 17 | 17 | 17 | > 17 | > 17 | 17 | DIFFERENT |
| 12n_614 | chiral | 15 | 15 | 15 | 15 | 15 | 15 | equal |
| 12n_616 | chiral | 15 | 15 | 15 | 15 | 15 | 15 | equal |
| 12n_618 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 12n_622 | chiral | 17 | 17 | > 17 | 17 | 17 | > 17 | DIFFERENT |
| 12n_631 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 12n_633 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 12n_634 | chiral | 15 | 15 | 15 | 15 | 15 | 15 | equal |
| 12n_635 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 12n_645 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 12n_646 | chiral | 15 | 15 | 15 | 15 | 15 | 15 | equal |
| 12n_652 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 12n_656 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 12n_657 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 12n_661 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 12n_662 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 12n_687 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 12n_702 | chiral | 15 | 15 | 15 | 15 | 15 | 15 | equal |
| 12n_704 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 12n_705 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 12n_709 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 12n_710 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 12n_711 | chiral | 15 | 15 | 15 | 15 | 15 | 15 | equal |
| 12n_712 | chiral | 17 | 17 | 17 | > 17 | > 17 | 17 | DIFFERENT |
| 12n_714 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 12n_716 | chiral | 15 | 15 | 15 | 15 | 15 | 15 | equal |
| 12n_727 | chiral | 15 | 15 | 15 | 15 | 15 | 15 | equal |
| 12n_728 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 12n_730 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 12n_731 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 12n_733 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 12n_757 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 12n_775 | chiral | 17 | 17 | > 17 | 17 | 17 | > 17 | DIFFERENT |
| 12n_776 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 12n_779 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 12n_782 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 12n_784 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 12n_786 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 12n_787 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 12n_788 | chiral | 15 | 17 | 17 | 17 | 17 | 17 | equal |
| 12n_789 | chiral | 17 | 17 | 17 | > 17 | > 17 | 17 | DIFFERENT |
| 12n_790 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 12n_792 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 12n_794 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 12n_800 | chiral | 15 | 15 | 17 | 15 | 15 | 17 | DIFFERENT |
| 12n_802 | chiral | 15 | 15 | 15 | 15 | 15 | 15 | equal |
| 12n_816 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 12n_827 | chiral | 15 | 15 | 15 | 15 | 15 | 15 | equal |
| 12n_841 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 12n_842 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 12n_852 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 12n_857 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 12n_859 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 12n_864 | chiral | 17 | 17 | 17 | > 17 | > 17 | 17 | DIFFERENT |
| 12n_865 | chiral | 17 | 17 | > 17 | 17 | 17 | > 17 | DIFFERENT |
| 12n_866 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 12n_870 | chiral | 17 | 17 | 17 | > 17 | > 17 | 17 | DIFFERENT |
| 12n_872 | chiral | 15 | 15 | 15 | 17 | 17 | 15 | DIFFERENT |
| 12n_877 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 12n_883 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 12n_884 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 12n_885 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13a_2 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13a_10 | chiral | 17 | 17 | 17 | > 17 | > 17 | 17 | DIFFERENT |
| 13a_21 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13a_22 | chiral | 17 | 17 | 17 | > 17 | > 17 | 17 | DIFFERENT |
| 13a_24 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13a_30 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13a_103 | chiral | 17 | 17 | > 17 | 17 | 17 | > 17 | DIFFERENT |
| 13a_115 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13a_212 | chiral | 15 | 15 | 17 | 15 | 15 | 17 | DIFFERENT |
| 13a_227 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13a_235 | chiral | 17 | 17 | > 17 | 17 | 17 | > 17 | DIFFERENT |
| 13a_310 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13a_315 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13a_375 | chiral | 17 | 17 | 17 | > 17 | > 17 | 17 | DIFFERENT |
| 13a_435 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13a_439 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13a_441 | chiral | 17 | 17 | > 17 | 17 | 17 | > 17 | DIFFERENT |
| 13a_570 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13a_583 | chiral | 17 | 17 | > 17 | 17 | 17 | > 17 | DIFFERENT |
| 13a_590 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13a_599 | chiral | 17 | 17 | > 17 | 17 | 17 | > 17 | DIFFERENT |
| 13a_604 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13a_605 | chiral | 17 | 17 | 17 | > 17 | > 17 | 17 | DIFFERENT |
| 13a_612 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13a_615 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13a_655 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13a_663 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13a_683 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13a_687 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13a_728 | chiral | 17 | 17 | 17 | > 17 | > 17 | 17 | DIFFERENT |
| 13a_750 | chiral | 17 | 17 | 17 | > 17 | > 17 | 17 | DIFFERENT |
| 13a_782 | chiral | 17 | 17 | > 17 | 17 | 17 | > 17 | DIFFERENT |
| 13a_791 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13a_807 | chiral | 17 | 17 | > 17 | 17 | 17 | > 17 | DIFFERENT |
| 13a_886 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13a_946 | chiral | 17 | 17 | > 17 | 17 | 17 | > 17 | DIFFERENT |
| 13a_949 | chiral | 17 | 17 | 17 | > 17 | > 17 | 17 | DIFFERENT |
| 13a_953 | chiral | 17 | 17 | 17 | > 17 | > 17 | 17 | DIFFERENT |
| 13a_955 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13a_957 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13a_958 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13a_1092 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13a_1132 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13a_1172 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13a_1173 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13a_1175 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13a_1200 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13a_1286 | chiral | 17 | 17 | 17 | > 17 | > 17 | 17 | DIFFERENT |
| 13a_1289 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13a_1338 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13a_1340 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13a_1375 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13a_1380 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13a_1381 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13a_1385 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13a_1424 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13a_1446 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13a_1502 | chiral | 15 | 17 | 17 | 17 | 17 | 17 | equal |
| 13a_1526 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13a_1527 | chiral | 17 | 17 | 17 | > 17 | > 17 | 17 | DIFFERENT |
| 13a_1620 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13a_1625 | chiral | 17 | 17 | 17 | > 17 | > 17 | 17 | DIFFERENT |
| 13a_1626 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13a_1646 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13a_1674 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13a_1680 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13a_1682 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13a_1691 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13a_1704 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13a_1705 | chiral | 17 | 17 | 17 | > 17 | > 17 | 17 | DIFFERENT |
| 13a_1708 | chiral | 17 | 17 | > 17 | 17 | 17 | > 17 | DIFFERENT |
| 13a_1713 | chiral | 15 | 15 | 15 | 15 | 15 | 15 | equal |
| 13a_1722 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13a_1723 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13a_1734 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13a_1737 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13a_1746 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13a_1760 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13a_1775 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13a_1803 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13a_1828 | chiral | 17 | 17 | 17 | > 17 | > 17 | 17 | DIFFERENT |
| 13a_1830 | chiral | 17 | 17 | 17 | > 17 | > 17 | 17 | DIFFERENT |
| 13a_1834 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13a_1841 | chiral | 17 | 17 | > 17 | 17 | 17 | > 17 | DIFFERENT |
| 13a_1842 | chiral | 17 | 17 | 17 | > 17 | > 17 | 17 | DIFFERENT |
| 13a_1851 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13a_1949 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13a_1981 | chiral | 17 | 17 | 17 | > 17 | > 17 | 17 | DIFFERENT |
| 13a_1992 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13a_2014 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13a_2017 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13a_2071 | chiral | 17 | 17 | 17 | > 17 | > 17 | 17 | DIFFERENT |
| 13a_2140 | chiral | 17 | 17 | 17 | > 17 | > 17 | 17 | DIFFERENT |
| 13a_2163 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13a_2223 | chiral | 17 | 17 | > 17 | 17 | 17 | > 17 | DIFFERENT |
| 13a_2224 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13a_2226 | chiral | 17 | 17 | 17 | > 17 | > 17 | 17 | DIFFERENT |
| 13a_2227 | chiral | 15 | 15 | 17 | 15 | 15 | 17 | DIFFERENT |
| 13a_2282 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13a_2297 | chiral | 17 | 17 | > 17 | 17 | 17 | > 17 | DIFFERENT |
| 13a_2340 | chiral | 17 | 17 | 17 | > 17 | > 17 | 17 | DIFFERENT |
| 13a_2371 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13a_2420 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13a_2430 | chiral | 17 | 17 | 17 | > 17 | > 17 | 17 | DIFFERENT |
| 13a_2432 | chiral | 17 | 17 | > 17 | 17 | 17 | > 17 | DIFFERENT |
| 13a_2440 | chiral | 17 | 17 | > 17 | 17 | 17 | > 17 | DIFFERENT |
| 13a_2461 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13a_2527 | chiral | 17 | 17 | 17 | > 17 | > 17 | 17 | DIFFERENT |
| 13a_2540 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13a_2544 | chiral | 17 | 17 | > 17 | 17 | 17 | > 17 | DIFFERENT |
| 13a_2569 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13a_2571 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13a_2637 | chiral | 17 | 17 | > 17 | 17 | 17 | > 17 | DIFFERENT |
| 13a_2638 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13a_2640 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13a_2646 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13a_2653 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13a_2654 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13a_2746 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13a_2764 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13a_2765 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13a_2914 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13a_2932 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13a_2964 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13a_3003 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13a_3067 | chiral | 17 | 17 | > 17 | 17 | 17 | > 17 | DIFFERENT |
| 13a_3144 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13a_3149 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13a_3294 | chiral | 17 | 17 | 17 | > 17 | > 17 | 17 | DIFFERENT |
| 13a_3298 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13a_3347 | chiral | 17 | 17 | > 17 | 17 | 17 | > 17 | DIFFERENT |
| 13a_3348 | chiral | 17 | 17 | > 17 | 17 | 17 | > 17 | DIFFERENT |
| 13a_3350 | chiral | 17 | 17 | 17 | > 17 | > 17 | 17 | DIFFERENT |
| 13a_3362 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13a_3387 | chiral | 17 | 17 | 17 | > 17 | > 17 | 17 | DIFFERENT |
| 13a_3403 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13a_3442 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13a_3450 | chiral | 17 | 17 | > 17 | 17 | 17 | > 17 | DIFFERENT |
| 13a_3470 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13a_3481 | chiral | 17 | 17 | 17 | > 17 | > 17 | 17 | DIFFERENT |
| 13a_3630 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13a_3639 | chiral | 17 | 17 | 17 | > 17 | > 17 | 17 | DIFFERENT |
| 13a_3650 | chiral | 17 | 17 | 17 | > 17 | > 17 | 17 | DIFFERENT |
| 13a_3684 | chiral | 17 | 17 | > 17 | 17 | 17 | > 17 | DIFFERENT |
| 13a_3700 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13a_3709 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13a_3766 | chiral | 17 | 17 | > 17 | 17 | 17 | > 17 | DIFFERENT |
| 13a_3836 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13a_3837 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13a_3849 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13a_3863 | chiral | 17 | 17 | 17 | > 17 | > 17 | 17 | DIFFERENT |
| 13a_3876 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13a_3909 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13a_4038 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13a_4044 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13a_4050 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13a_4098 | chiral | 17 | 17 | > 17 | 17 | 17 | > 17 | DIFFERENT |
| 13a_4118 | chiral | 17 | 17 | 17 | > 17 | > 17 | 17 | DIFFERENT |
| 13a_4130 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13a_4175 | chiral | 17 | 17 | > 17 | 17 | 17 | > 17 | DIFFERENT |
| 13a_4182 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13a_4183 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13a_4197 | chiral | 17 | 17 | > 17 | 17 | 17 | > 17 | DIFFERENT |
| 13a_4199 | chiral | 17 | 17 | 17 | > 17 | > 17 | 17 | DIFFERENT |
| 13a_4345 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13a_4428 | chiral | 15 | 17 | 17 | 17 | 17 | 17 | equal |
| 13a_4437 | chiral | 17 | 17 | 17 | > 17 | > 17 | 17 | DIFFERENT |
| 13a_4439 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13a_4445 | chiral | 17 | 17 | 17 | > 17 | > 17 | 17 | DIFFERENT |
| 13a_4446 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13a_4620 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13a_4629 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13a_4716 | chiral | 17 | 17 | 17 | > 17 | > 17 | 17 | DIFFERENT |
| 13a_4730 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_1 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_2 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_3 | chiral | 15 | 15 | 15 | 15 | 15 | 15 | equal |
| 13n_4 | chiral | 15 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_7 | chiral | 15 | 15 | 15 | 15 | 15 | 15 | equal |
| 13n_9 | chiral | 17 | 17 | 17 | > 17 | > 17 | 17 | DIFFERENT |
| 13n_10 | chiral | 15 | 15 | 15 | 17 | 17 | 15 | DIFFERENT |
| 13n_27 | chiral | 15 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_37 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_38 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_39 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_40 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_53 | chiral | 15 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_60 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_64 | chiral | 17 | 17 | > 17 | 17 | 17 | > 17 | DIFFERENT |
| 13n_65 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_66 | chiral | 17 | 17 | > 17 | 17 | 17 | > 17 | DIFFERENT |
| 13n_70 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_71 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_78 | chiral | 15 | 15 | 15 | 15 | 15 | 15 | equal |
| 13n_84 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_85 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_86 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_115 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_116 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_117 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_121 | chiral | 15 | 15 | 15 | 17 | 17 | 15 | DIFFERENT |
| 13n_122 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_124 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_125 | chiral | 17 | 17 | 17 | > 17 | > 17 | 17 | DIFFERENT |
| 13n_129 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_138 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_147 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_202 | chiral | 17 | 17 | 17 | > 17 | > 17 | 17 | DIFFERENT |
| 13n_212 | chiral | 17 | 17 | > 17 | 17 | 17 | > 17 | DIFFERENT |
| 13n_215 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_216 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_217 | chiral | 17 | 17 | 17 | > 17 | > 17 | 17 | DIFFERENT |
| 13n_253 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_288 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_316 | chiral | 17 | 17 | > 17 | 17 | 17 | > 17 | DIFFERENT |
| 13n_318 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_319 | chiral | 15 | 15 | 15 | 17 | 17 | 15 | DIFFERENT |
| 13n_323 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_326 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_327 | chiral | 15 | 17 | 17 | > 17 | > 17 | 17 | DIFFERENT |
| 13n_334 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_336 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_337 | chiral | 15 | 15 | 15 | 15 | 15 | 15 | equal |
| 13n_341 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_342 | chiral | 15 | 15 | 17 | 15 | 15 | 17 | DIFFERENT |
| 13n_343 | chiral | 15 | 15 | 15 | 15 | 15 | 15 | equal |
| 13n_348 | chiral | 17 | 17 | 17 | > 17 | > 17 | 17 | DIFFERENT |
| 13n_349 | chiral | 15 | 15 | 17 | 15 | 15 | 17 | DIFFERENT |
| 13n_355 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_377 | chiral | 15 | 15 | 15 | 15 | 15 | 15 | equal |
| 13n_379 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_381 | chiral | 15 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_382 | chiral | 15 | 15 | 15 | 15 | 15 | 15 | equal |
| 13n_385 | chiral | 15 | 17 | > 17 | 17 | 17 | > 17 | DIFFERENT |
| 13n_398 | chiral | 17 | 17 | 17 | > 17 | > 17 | 17 | DIFFERENT |
| 13n_410 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_411 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_420 | chiral | 15 | 15 | 15 | 15 | 15 | 15 | equal |
| 13n_423 | chiral | 17 | 17 | > 17 | 17 | 17 | > 17 | DIFFERENT |
| 13n_426 | chiral | 15 | 17 | 17 | > 17 | > 17 | 17 | DIFFERENT |
| 13n_427 | chiral | 15 | 15 | 15 | 15 | 15 | 15 | equal |
| 13n_443 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_444 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_446 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_475 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_484 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_498 | chiral | 15 | 15 | 17 | 15 | 15 | 17 | DIFFERENT |
| 13n_501 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_510 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_511 | chiral | 15 | 17 | > 17 | 17 | 17 | > 17 | DIFFERENT |
| 13n_524 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_529 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_543 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_544 | chiral | 15 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_576 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_600 | chiral | 17 | 17 | > 17 | 17 | 17 | > 17 | DIFFERENT |
| 13n_606 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_610 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_613 | chiral | 15 | 15 | 15 | 17 | 17 | 15 | DIFFERENT |
| 13n_630 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_646 | chiral | 15 | 17 | > 17 | 17 | 17 | > 17 | DIFFERENT |
| 13n_673 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_714 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_715 | chiral | 17 | 17 | 17 | > 17 | > 17 | 17 | DIFFERENT |
| 13n_723 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_742 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_745 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_747 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_748 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_762 | chiral | 17 | 17 | > 17 | 17 | 17 | > 17 | DIFFERENT |
| 13n_772 | chiral | 17 | 17 | 17 | > 17 | > 17 | 17 | DIFFERENT |
| 13n_775 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_777 | chiral | 15 | 15 | 15 | 17 | 17 | 15 | DIFFERENT |
| 13n_804 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_806 | chiral | 17 | 17 | > 17 | 17 | 17 | > 17 | DIFFERENT |
| 13n_810 | chiral | 15 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_813 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_816 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_819 | chiral | 17 | 17 | 17 | > 17 | > 17 | 17 | DIFFERENT |
| 13n_824 | chiral | 17 | 17 | 17 | > 17 | > 17 | 17 | DIFFERENT |
| 13n_827 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_829 | chiral | 17 | 17 | > 17 | 17 | 17 | > 17 | DIFFERENT |
| 13n_854 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_860 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_878 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_881 | chiral | 15 | 17 | 17 | > 17 | > 17 | 17 | DIFFERENT |
| 13n_892 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_893 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_895 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_896 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_942 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_969 | chiral | 17 | 17 | 17 | > 17 | > 17 | 17 | DIFFERENT |
| 13n_1026 | chiral | 17 | 17 | > 17 | 17 | 17 | > 17 | DIFFERENT |
| 13n_1031 | chiral | 17 | 17 | 17 | > 17 | > 17 | 17 | DIFFERENT |
| 13n_1034 | chiral | 17 | 17 | 17 | > 17 | > 17 | 17 | DIFFERENT |
| 13n_1042 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_1045 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_1070 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_1108 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_1109 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_1116 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_1119 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_1120 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_1126 | chiral | 17 | 17 | > 17 | 17 | 17 | > 17 | DIFFERENT |
| 13n_1129 | chiral | 15 | 17 | > 17 | 17 | 17 | > 17 | DIFFERENT |
| 13n_1130 | chiral | 15 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_1156 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_1213 | chiral | 17 | 17 | 17 | > 17 | > 17 | 17 | DIFFERENT |
| 13n_1215 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_1219 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_1231 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_1250 | chiral | 17 | 17 | 17 | > 17 | > 17 | 17 | DIFFERENT |
| 13n_1258 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_1259 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_1335 | chiral | 17 | 17 | > 17 | 17 | 17 | > 17 | DIFFERENT |
| 13n_1336 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_1339 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_1342 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_1343 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_1346 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_1347 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_1359 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_1392 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_1403 | chiral | 15 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_1436 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_1443 | chiral | 15 | 15 | 15 | 17 | 17 | 15 | DIFFERENT |
| 13n_1444 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_1449 | chiral | 17 | 17 | 17 | > 17 | > 17 | 17 | DIFFERENT |
| 13n_1450 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_1468 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_1472 | chiral | 15 | 17 | > 17 | 17 | 17 | > 17 | DIFFERENT |
| 13n_1476 | chiral | 15 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_1481 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_1482 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_1486 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_1487 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_1518 | chiral | 17 | 17 | 17 | > 17 | > 17 | 17 | DIFFERENT |
| 13n_1538 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_1540 | chiral | 15 | 15 | 15 | 15 | 15 | 15 | equal |
| 13n_1546 | chiral | 15 | 15 | 15 | 15 | 15 | 15 | equal |
| 13n_1547 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_1549 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_1550 | chiral | 15 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_1555 | chiral | 17 | 17 | 17 | > 17 | > 17 | 17 | DIFFERENT |
| 13n_1559 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_1560 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_1561 | chiral | 15 | 15 | 15 | 17 | 17 | 15 | DIFFERENT |
| 13n_1562 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_1564 | chiral | 17 | 17 | > 17 | 17 | 17 | > 17 | DIFFERENT |
| 13n_1570 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_1598 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_1604 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_1605 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_1606 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_1607 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_1608 | chiral | 15 | 15 | 15 | 15 | 15 | 15 | equal |
| 13n_1616 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_1625 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_1626 | chiral | 15 | 15 | 15 | 15 | 15 | 15 | equal |
| 13n_1627 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_1631 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_1634 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_1635 | chiral | 17 | 17 | > 17 | 17 | 17 | > 17 | DIFFERENT |
| 13n_1638 | chiral | 15 | 15 | 15 | 15 | 15 | 15 | equal |
| 13n_1640 | chiral | 17 | 17 | 17 | > 17 | > 17 | 17 | DIFFERENT |
| 13n_1646 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_1650 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_1677 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_1680 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_1694 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_1711 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_1724 | chiral | 17 | 17 | 17 | > 17 | > 17 | 17 | DIFFERENT |
| 13n_1728 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_1736 | chiral | 17 | 17 | 17 | > 17 | > 17 | 17 | DIFFERENT |
| 13n_1740 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_1752 | chiral | 13 | 17 | 17 | > 17 | > 17 | 17 | DIFFERENT |
| 13n_1757 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_1759 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_1763 | chiral | 17 | 17 | > 17 | 17 | 17 | > 17 | DIFFERENT |
| 13n_1796 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_1803 | chiral | 17 | 17 | 17 | > 17 | > 17 | 17 | DIFFERENT |
| 13n_1813 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_1817 | chiral | 17 | 17 | > 17 | 17 | 17 | > 17 | DIFFERENT |
| 13n_1819 | chiral | 17 | 17 | > 17 | 17 | 17 | > 17 | DIFFERENT |
| 13n_1820 | chiral | 13 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_1824 | chiral | 15 | 15 | 15 | 15 | 15 | 15 | equal |
| 13n_1829 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_1830 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_1831 | chiral | 15 | 15 | 15 | 15 | 15 | 15 | equal |
| 13n_1832 | chiral | 15 | 15 | 15 | 15 | 15 | 15 | equal |
| 13n_1834 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_1835 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_1840 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_1844 | chiral | 13 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_1852 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_1855 | chiral | 15 | 17 | 17 | > 17 | > 17 | 17 | DIFFERENT |
| 13n_1856 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_1858 | chiral | 13 | 13 | 13 | 15 | 15 | 13 | DIFFERENT |
| 13n_1860 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_1866 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_1868 | chiral | 15 | 15 | 15 | 15 | 15 | 15 | equal |
| 13n_1872 | chiral | 17 | 17 | 17 | > 17 | > 17 | 17 | DIFFERENT |
| 13n_1875 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_1880 | chiral | 15 | 15 | 15 | 17 | 17 | 15 | DIFFERENT |
| 13n_1884 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_1885 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_1887 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_1888 | chiral | 15 | 15 | 15 | 15 | 15 | 15 | equal |
| 13n_1890 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_1892 | chiral | 15 | 15 | 17 | 15 | 15 | 17 | DIFFERENT |
| 13n_1898 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_1901 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_1903 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_1931 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_1935 | chiral | 15 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_1945 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_1957 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_1966 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_1983 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_1990 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_1991 | chiral | 15 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_2000 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_2025 | chiral | 17 | 17 | > 17 | 17 | 17 | > 17 | DIFFERENT |
| 13n_2041 | chiral | 17 | 17 | > 17 | 17 | 17 | > 17 | DIFFERENT |
| 13n_2043 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_2044 | chiral | 15 | 17 | 17 | > 17 | > 17 | 17 | DIFFERENT |
| 13n_2055 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_2068 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_2070 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_2076 | chiral | 15 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_2079 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_2081 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_2082 | chiral | 15 | 15 | 15 | 15 | 15 | 15 | equal |
| 13n_2084 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_2085 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_2088 | chiral | 17 | 17 | 17 | > 17 | > 17 | 17 | DIFFERENT |
| 13n_2090 | chiral | 15 | 15 | 15 | 15 | 15 | 15 | equal |
| 13n_2096 | chiral | 15 | 15 | 15 | 17 | 17 | 15 | DIFFERENT |
| 13n_2097 | chiral | 17 | 17 | 17 | > 17 | > 17 | 17 | DIFFERENT |
| 13n_2112 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_2115 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_2117 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_2124 | chiral | 15 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_2129 | chiral | 17 | 17 | > 17 | 17 | 17 | > 17 | DIFFERENT |
| 13n_2143 | chiral | 17 | 17 | > 17 | 17 | 17 | > 17 | DIFFERENT |
| 13n_2150 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_2152 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_2158 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_2170 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_2173 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_2185 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_2189 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_2203 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_2205 | chiral | 17 | 17 | > 17 | 17 | 17 | > 17 | DIFFERENT |
| 13n_2208 | chiral | 15 | 15 | 15 | 17 | 17 | 15 | DIFFERENT |
| 13n_2212 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_2216 | chiral | 17 | 17 | 17 | > 17 | > 17 | 17 | DIFFERENT |
| 13n_2227 | chiral | 15 | 15 | 15 | 15 | 15 | 15 | equal |
| 13n_2229 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_2233 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_2244 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_2254 | chiral | 17 | 17 | 17 | > 17 | > 17 | 17 | DIFFERENT |
| 13n_2255 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_2257 | chiral | 15 | 15 | 15 | 17 | 17 | 15 | DIFFERENT |
| 13n_2258 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_2260 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_2261 | chiral | 17 | 17 | 17 | > 17 | > 17 | 17 | DIFFERENT |
| 13n_2262 | chiral | 15 | 15 | 17 | 15 | 15 | 17 | DIFFERENT |
| 13n_2264 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_2269 | chiral | 15 | 15 | 17 | 15 | 15 | 17 | DIFFERENT |
| 13n_2275 | chiral | 15 | 15 | 17 | 15 | 15 | 17 | DIFFERENT |
| 13n_2276 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_2277 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_2284 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_2326 | chiral | 15 | 15 | 15 | 15 | 15 | 15 | equal |
| 13n_2328 | chiral | 13 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_2329 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_2330 | chiral | 15 | 15 | 15 | 17 | 17 | 15 | DIFFERENT |
| 13n_2332 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_2333 | chiral | 17 | 17 | > 17 | 17 | 17 | > 17 | DIFFERENT |
| 13n_2336 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_2338 | chiral | 13 | 13 | 13 | 15 | 15 | 13 | DIFFERENT |
| 13n_2339 | chiral | 17 | 17 | 17 | > 17 | > 17 | 17 | DIFFERENT |
| 13n_2340 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_2381 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_2424 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_2440 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_2447 | chiral | 17 | 17 | 17 | > 17 | > 17 | 17 | DIFFERENT |
| 13n_2471 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_2473 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_2476 | chiral | 15 | 15 | 15 | 17 | 17 | 15 | DIFFERENT |
| 13n_2477 | chiral | 15 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_2478 | chiral | 15 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_2483 | chiral | 17 | 17 | 17 | > 17 | > 17 | 17 | DIFFERENT |
| 13n_2488 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_2489 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_2506 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_2517 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_2520 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_2521 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_2522 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_2523 | chiral | 17 | 17 | 17 | > 17 | > 17 | 17 | DIFFERENT |
| 13n_2524 | chiral | 15 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_2527 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_2529 | chiral | 15 | 15 | 15 | 15 | 15 | 15 | equal |
| 13n_2531 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_2538 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_2562 | chiral | 15 | 15 | 17 | 15 | 15 | 17 | DIFFERENT |
| 13n_2564 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_2585 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_2590 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_2593 | chiral | 17 | 17 | 17 | > 17 | > 17 | 17 | DIFFERENT |
| 13n_2598 | chiral | 15 | 17 | > 17 | 17 | 17 | > 17 | DIFFERENT |
| 13n_2603 | chiral | 17 | 17 | > 17 | 17 | 17 | > 17 | DIFFERENT |
| 13n_2610 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_2620 | chiral | 15 | 15 | 15 | 15 | 15 | 15 | equal |
| 13n_2622 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_2623 | chiral | 15 | 15 | 15 | 15 | 15 | 15 | equal |
| 13n_2624 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_2626 | chiral | 15 | 15 | 15 | 15 | 15 | 15 | equal |
| 13n_2629 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_2632 | chiral | 15 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_2633 | chiral | 15 | 15 | 17 | 15 | 15 | 17 | DIFFERENT |
| 13n_2634 | chiral | 15 | 15 | 15 | 17 | 17 | 15 | DIFFERENT |
| 13n_2652 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_2653 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_2659 | chiral | 15 | 15 | 15 | 15 | 15 | 15 | equal |
| 13n_2661 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_2663 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_2679 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_2683 | chiral | 17 | 17 | 17 | > 17 | > 17 | 17 | DIFFERENT |
| 13n_2686 | chiral | 15 | 15 | 15 | 15 | 15 | 15 | equal |
| 13n_2689 | chiral | 17 | 17 | > 17 | 17 | 17 | > 17 | DIFFERENT |
| 13n_2690 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_2695 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_2696 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_2707 | chiral | 15 | 15 | 17 | 15 | 15 | 17 | DIFFERENT |
| 13n_2727 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_2739 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_2741 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_2742 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_2747 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_2754 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_2759 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_2763 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_2764 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_2765 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_2771 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_2773 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_2775 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_2776 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_2778 | chiral | 17 | 17 | 17 | > 17 | > 17 | 17 | DIFFERENT |
| 13n_2783 | chiral | 17 | 17 | > 17 | 17 | 17 | > 17 | DIFFERENT |
| 13n_2788 | chiral | 17 | 17 | 17 | > 17 | > 17 | 17 | DIFFERENT |
| 13n_2793 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_2794 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_2795 | chiral | 15 | 15 | 17 | 15 | 15 | 17 | DIFFERENT |
| 13n_2801 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_2802 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_2805 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_2816 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_2827 | chiral | 15 | 15 | 17 | 15 | 15 | 17 | DIFFERENT |
| 13n_2835 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_2836 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_2838 | chiral | 17 | 17 | > 17 | 17 | 17 | > 17 | DIFFERENT |
| 13n_2839 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_2841 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_2842 | chiral | 15 | 15 | 15 | 15 | 15 | 15 | equal |
| 13n_2851 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_2857 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_2868 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_2873 | chiral | 15 | 15 | 15 | 15 | 15 | 15 | equal |
| 13n_2874 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_2875 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_2876 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_2877 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_2880 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_2892 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_2893 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_2894 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_2895 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_2908 | chiral | 17 | 17 | > 17 | 17 | 17 | > 17 | DIFFERENT |
| 13n_2929 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_2930 | chiral | 17 | 17 | 17 | > 17 | > 17 | 17 | DIFFERENT |
| 13n_2945 | chiral | 17 | 17 | 17 | > 17 | > 17 | 17 | DIFFERENT |
| 13n_2946 | chiral | 15 | 17 | > 17 | 17 | 17 | > 17 | DIFFERENT |
| 13n_2971 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_2976 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_2980 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_2986 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_3023 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_3036 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_3047 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_3057 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_3063 | chiral | 17 | 17 | 17 | > 17 | > 17 | 17 | DIFFERENT |
| 13n_3090 | chiral | 17 | 17 | > 17 | 17 | 17 | > 17 | DIFFERENT |
| 13n_3122 | chiral | 15 | 15 | 15 | 17 | 17 | 15 | DIFFERENT |
| 13n_3126 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_3130 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_3131 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_3141 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_3146 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_3152 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_3153 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_3155 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_3156 | chiral | 17 | 17 | > 17 | 17 | 17 | > 17 | DIFFERENT |
| 13n_3157 | chiral | 15 | 15 | 15 | 17 | 17 | 15 | DIFFERENT |
| 13n_3159 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_3161 | chiral | 17 | 17 | > 17 | 17 | 17 | > 17 | DIFFERENT |
| 13n_3178 | chiral | 15 | 15 | 17 | 15 | 15 | 17 | DIFFERENT |
| 13n_3181 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_3182 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_3183 | chiral | 15 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_3184 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_3186 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_3187 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_3194 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_3202 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_3211 | chiral | 15 | 15 | 15 | 15 | 15 | 15 | equal |
| 13n_3218 | chiral | 15 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_3229 | chiral | 17 | 17 | 17 | > 17 | > 17 | 17 | DIFFERENT |
| 13n_3230 | chiral | 15 | 15 | 15 | 15 | 15 | 15 | equal |
| 13n_3233 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_3240 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_3252 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_3288 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_3296 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_3305 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_3328 | chiral | 17 | 17 | 17 | > 17 | > 17 | 17 | DIFFERENT |
| 13n_3331 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_3342 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_3345 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_3352 | chiral | 17 | 17 | > 17 | 17 | 17 | > 17 | DIFFERENT |
| 13n_3361 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_3366 | chiral | 15 | 15 | 17 | 15 | 15 | 17 | DIFFERENT |
| 13n_3368 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_3376 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_3382 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_3412 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_3414 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_3417 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_3419 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_3423 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_3425 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_3437 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_3439 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_3440 | chiral | 17 | 17 | > 17 | 17 | 17 | > 17 | DIFFERENT |
| 13n_3448 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_3449 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_3450 | chiral | 17 | 17 | > 17 | 17 | 17 | > 17 | DIFFERENT |
| 13n_3451 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_3452 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_3453 | chiral | 17 | 17 | > 17 | 17 | 17 | > 17 | DIFFERENT |
| 13n_3461 | chiral | 17 | 17 | 17 | > 17 | > 17 | 17 | DIFFERENT |
| 13n_3471 | chiral | 17 | 17 | 17 | > 17 | > 17 | 17 | DIFFERENT |
| 13n_3476 | chiral | 17 | 17 | > 17 | 17 | 17 | > 17 | DIFFERENT |
| 13n_3481 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_3482 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_3485 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_3487 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_3509 | chiral | 17 | 17 | 17 | > 17 | > 17 | 17 | DIFFERENT |
| 13n_3510 | chiral | 17 | 17 | > 17 | 17 | 17 | > 17 | DIFFERENT |
| 13n_3541 | chiral | 17 | 17 | > 17 | 17 | 17 | > 17 | DIFFERENT |
| 13n_3549 | chiral | 17 | 17 | > 17 | 17 | 17 | > 17 | DIFFERENT |
| 13n_3563 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_3564 | chiral | 15 | 15 | 17 | 15 | 15 | 17 | DIFFERENT |
| 13n_3577 | chiral | 17 | 17 | > 17 | 17 | 17 | > 17 | DIFFERENT |
| 13n_3578 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_3579 | chiral | 17 | 17 | 17 | > 17 | > 17 | 17 | DIFFERENT |
| 13n_3591 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_3600 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_3607 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_3615 | chiral | 15 | 15 | 17 | 15 | 15 | 17 | DIFFERENT |
| 13n_3626 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_3640 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_3725 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_3726 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_3783 | chiral | 17 | 17 | > 17 | 17 | 17 | > 17 | DIFFERENT |
| 13n_3794 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_3796 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_3812 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_3833 | chiral | 17 | 17 | 17 | > 17 | > 17 | 17 | DIFFERENT |
| 13n_3844 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_3849 | chiral | 15 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_3851 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_3852 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_3865 | chiral | 17 | 17 | > 17 | 17 | 17 | > 17 | DIFFERENT |
| 13n_3900 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_3927 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_3931 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_3932 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_3936 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_3938 | chiral | 17 | 17 | 17 | > 17 | > 17 | 17 | DIFFERENT |
| 13n_3950 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_3952 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_3957 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_3958 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_3959 | chiral | 15 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_3966 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_3969 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_3970 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_3971 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_3973 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_3974 | chiral | 15 | 17 | 17 | > 17 | > 17 | 17 | DIFFERENT |
| 13n_3982 | chiral | 17 | 17 | > 17 | 17 | 17 | > 17 | DIFFERENT |
| 13n_3983 | chiral | 17 | 17 | > 17 | 17 | 17 | > 17 | DIFFERENT |
| 13n_3987 | chiral | 17 | 17 | 17 | > 17 | > 17 | 17 | DIFFERENT |
| 13n_3988 | chiral | 15 | 15 | 15 | 17 | 17 | 15 | DIFFERENT |
| 13n_3991 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_4004 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_4005 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_4008 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_4015 | chiral | 17 | 17 | > 17 | 17 | 17 | > 17 | DIFFERENT |
| 13n_4016 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_4017 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_4019 | chiral | 15 | 15 | 15 | 15 | 15 | 15 | equal |
| 13n_4027 | chiral | 15 | 15 | 15 | 15 | 15 | 15 | equal |
| 13n_4030 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_4036 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_4037 | chiral | 15 | 15 | 17 | 15 | 15 | 17 | DIFFERENT |
| 13n_4041 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_4042 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_4048 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_4063 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_4064 | chiral | 17 | 17 | 17 | > 17 | > 17 | 17 | DIFFERENT |
| 13n_4075 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_4076 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_4078 | chiral | 17 | 17 | > 17 | 17 | 17 | > 17 | DIFFERENT |
| 13n_4081 | chiral | 15 | 15 | 15 | 15 | 15 | 15 | equal |
| 13n_4086 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_4100 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_4102 | chiral | 17 | 17 | 17 | > 17 | > 17 | 17 | DIFFERENT |
| 13n_4104 | chiral | 17 | 17 | > 17 | 17 | 17 | > 17 | DIFFERENT |
| 13n_4110 | chiral | 15 | 15 | 17 | 15 | 15 | 17 | DIFFERENT |
| 13n_4122 | chiral | 15 | 15 | 17 | 15 | 15 | 17 | DIFFERENT |
| 13n_4130 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_4131 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_4134 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_4156 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_4164 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_4165 | chiral | 15 | 15 | 17 | 15 | 15 | 17 | DIFFERENT |
| 13n_4191 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_4193 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_4194 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_4201 | chiral | 17 | 17 | > 17 | 17 | 17 | > 17 | DIFFERENT |
| 13n_4203 | chiral | 17 | 17 | 17 | > 17 | > 17 | 17 | DIFFERENT |
| 13n_4239 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_4255 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_4258 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_4279 | chiral | 17 | 17 | 17 | > 17 | > 17 | 17 | DIFFERENT |
| 13n_4289 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_4290 | chiral | 17 | 17 | > 17 | 17 | 17 | > 17 | DIFFERENT |
| 13n_4294 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_4312 | chiral | 17 | 17 | 17 | > 17 | > 17 | 17 | DIFFERENT |
| 13n_4315 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_4317 | chiral | 15 | 15 | 15 | 15 | 15 | 15 | equal |
| 13n_4323 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_4325 | chiral | 17 | 17 | 17 | > 17 | > 17 | 17 | DIFFERENT |
| 13n_4331 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_4341 | chiral | 17 | 17 | > 17 | 17 | 17 | > 17 | DIFFERENT |
| 13n_4348 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_4351 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_4355 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_4356 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_4357 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_4372 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_4378 | chiral | 17 | 17 | 17 | > 17 | > 17 | 17 | DIFFERENT |
| 13n_4390 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_4400 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_4402 | chiral | 17 | 17 | 17 | > 17 | > 17 | 17 | DIFFERENT |
| 13n_4413 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_4427 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_4430 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_4431 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_4433 | chiral | 15 | 15 | 15 | 15 | 15 | 15 | equal |
| 13n_4434 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_4436 | chiral | 15 | 15 | 17 | 15 | 15 | 17 | DIFFERENT |
| 13n_4449 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_4454 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_4461 | chiral | 15 | 15 | 15 | 15 | 15 | 15 | equal |
| 13n_4466 | chiral | 15 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_4468 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_4488 | chiral | 15 | 15 | 15 | 17 | 17 | 15 | DIFFERENT |
| 13n_4500 | chiral | 15 | 15 | 15 | 15 | 15 | 15 | equal |
| 13n_4517 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_4530 | chiral | 17 | 17 | 17 | > 17 | > 17 | 17 | DIFFERENT |
| 13n_4543 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_4551 | chiral | 17 | 17 | 17 | > 17 | > 17 | 17 | DIFFERENT |
| 13n_4554 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_4557 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_4570 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_4575 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_4590 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_4591 | chiral | 15 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_4593 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_4598 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_4599 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_4618 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_4620 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_4652 | chiral | 17 | 17 | 17 | > 17 | > 17 | 17 | DIFFERENT |
| 13n_4666 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_4692 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_4699 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_4701 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_4706 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_4707 | chiral | 15 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_4710 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_4734 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_4753 | chiral | 15 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_4767 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_4769 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_4784 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_4786 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_4808 | chiral | 17 | 17 | 17 | > 17 | > 17 | 17 | DIFFERENT |
| 13n_4813 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_4824 | chiral | 15 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_4869 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_4873 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_4874 | chiral | 15 | 15 | 15 | 17 | 17 | 15 | DIFFERENT |
| 13n_4878 | chiral | 17 | 17 | 17 | > 17 | > 17 | 17 | DIFFERENT |
| 13n_4880 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_4898 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_4901 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_4905 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_4912 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_4916 | chiral | 15 | 17 | > 17 | 17 | 17 | > 17 | DIFFERENT |
| 13n_4922 | chiral | 15 | 15 | 15 | 17 | 17 | 15 | DIFFERENT |
| 13n_4924 | chiral | 17 | 17 | 17 | > 17 | > 17 | 17 | DIFFERENT |
| 13n_4925 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_4934 | chiral | 17 | 17 | 17 | > 17 | > 17 | 17 | DIFFERENT |
| 13n_4936 | chiral | 17 | 17 | > 17 | 17 | 17 | > 17 | DIFFERENT |
| 13n_4999 | chiral | 17 | 17 | 17 | > 17 | > 17 | 17 | DIFFERENT |
| 13n_5000 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_5001 | chiral | 17 | 17 | > 17 | 17 | 17 | > 17 | DIFFERENT |
| 13n_5005 | chiral | 17 | 17 | 17 | > 17 | > 17 | 17 | DIFFERENT |
| 13n_5006 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_5009 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_5031 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_5039 | chiral | 15 | 15 | 15 | 17 | 17 | 15 | DIFFERENT |
| 13n_5041 | chiral | 15 | 15 | 15 | 15 | 15 | 15 | equal |
| 13n_5042 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 13n_5067 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
