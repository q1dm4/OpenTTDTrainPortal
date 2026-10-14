# Source and build notes

Base: official JGRPP tag `jgrpp-0.73.0`, commit `a1a28d11a2ae4569d6d4216b1543996141d8cd36`.

Extract `jgrpp-0.73.0-base-source.tar.gz` into a fresh directory and apply `engine.patch` with `git apply`. The patch includes the gateway implementation, custom save fields, routing changes, diagnostic/test console commands, and three missing standard-header fixes needed by the cross compiler. The independent pairing-policy test is supplied in `gateway-source/tests`.

The Windows cross compiler used is the official LLVM MinGW UCRT x86_64 Ubuntu 22.04 distribution, release `20261006`. See `windows-toolchain-reference.cmake`; replace the absolute paths with your local directories.

Build the included zlib and xz sources as Windows static libraries with that toolchain. zlib source commit: `767c4c947852e143f582c85f14cf573411df1b35`. xz source commit: `3b1efb04d17c3a9ef7f473d73af13f1531428ffe`.

Build native Linux host tools first, using CMake/Ninja with `OPTION_DEDICATED=ON`. Then configure the Windows build with `OPTION_DEDICATED=OFF`, `HOST_BINARY_DIR` pointing to that host build, `CMAKE_TOOLCHAIN_FILE` pointing to the adapted toolchain file, and explicit `ZLIB_LIBRARY`, `ZLIB_INCLUDE_DIR`, `LIBLZMA_LIBRARY`, and `LIBLZMA_INCLUDE_DIR`. Both engine builds use Release mode with upstream assertions enabled.

The graphics preview uses the supplied NML and original sprite generator. Build with NML 0.9.0. The engine identifies internal GRFID `0x01574754`, station local ID zero; the displayed/config GRFID is `54475701`.

The runtime test fixture is `gateway_demo`, or `gateway_demo y` for the second track axis, in a fresh flat single-player 128×128 map with the gateway NewGRF enabled. These commands construct native track/stations and a three-part train with seven coal units and two station orders. They are test helpers for empty maps, not existing-save migration tools. The included user launcher does not execute the automated developer scripts.

Compilation and runtime validation results are recorded separately in `TEST-RESULTS.md`. Native Windows execution must be tested on a Windows machine.
