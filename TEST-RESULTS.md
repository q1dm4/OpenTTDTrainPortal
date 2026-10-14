# Verification

The latest Linux dedicated engine build completed successfully with assertions enabled. Runtime checks used native game construction and train movement, not a standalone teleport simulation.

| Check | Result |
| --- | --- |
| Automatic pairing policy | Passed construction ordering, multiple pairs, ownership, deletion, ID reuse, stale-link repair, reload ordering, and 500 randomized topology mutations |
| Initial demonstration save reload | Passed; restored pair and initial three-part train |
| X-axis forward and return transfers | Passed; two passages, three parts, seven coal units, two orders |
| Y-axis forward and return transfers | Passed; two passages, same consist/cargo/order invariants |
| Occupied destination | Passed; source train held at zero speed with no transfer; resumed and completed two passages after obstruction removed |
| Reserved destination | Passed; train held with no transfer until the destination reservation cleared, then completed two passages |
| Save/reload after transfer | Passed; pair persisted and passage count advanced from two to four, preserving parts/cargo/orders |

These results apply to the restricted single-train, same-axis, flat straight-buffer, classic-braking demonstration. General shared-network traffic, opposed trains, realistic braking, multiplayer, long curved train footprints, rotated gateways, and existing-save gateway migration are not validated.

Original Sadingham save investigation previously confirmed all four uploaded NewGRF checksums and a headless load/save/reload. That was not a gateway migration test, and Iron Horse emitted a capacity-change warning. The user save is not included or modified by this test package.

Windows GUI cross-compilation completed successfully. PE inspection confirms COFF x86-64 and the Windows GUI subsystem. The executable imports only Windows system libraries and UCRT API sets; no separate compiler-runtime DLLs are required. zlib and liblzma are statically linked. The package targets Windows 10/11 64-bit.

Native Windows execution has not been performed in this Linux environment. Launching the included executable on the user's Windows machine is the next test. The isolated package configuration and demonstration save were smoke-tested with the latest Linux engine and completed repeated transfers.
