# Teleport gateway — restricted test prototype

This experimental build is based on JGRPP 0.73.0 for Windows 64-bit. It is intended for the included isolated demonstration game. It is not an upgrade for your normal installation or your Sadingham save.

## Start the test

1. Extract the entire ZIP into a new folder.
2. Double-click `Test-Gateway.bat`.
3. Unpause the demonstration game if necessary. Open the train list, select the only train, and use its centre-view button to find it. Follow the three-part coal train as it travels between the two ordinary stations. The blue gateways link the two disconnected straight rail lines.
4. Open the console with the backtick key and enter `gateway_status` to see its passage counter. `gateway_pairs` shows the linked stations.

The whole train should appear at the partner gateway when it crosses the source. The initial train has three vehicle parts, seven units of coal, and two orders. The portals are not loading stops.

## Build your own controlled layout

Use the Energy gateways station category. Build each gateway as a separate one-tile, one-platform station. Gateways pair in construction order within the same company: first with second, third with fourth. Use the same track orientation and rail type at both ends, with flat straight track long enough to accommodate the entire train and one extra tile at each end. Set train braking to Original/classic.

For this prototype, use one moving train per pair. Keep the gateway buffers clear of junctions, signals, other stations, and depots. Curves in the train footprint, rotation between gateways, realistic braking, opposed simultaneous trains, multiplayer, and general shared-network traffic have not been validated.

An occupied destination buffer should hold the train at the source until the buffer clears. If it does not move, check both buffers and the layout restrictions above.

## Report a result

Please report whether the game launches, whether the train disappears and reappears as a complete consist, whether it keeps its orders and coal, and whether it completes a return trip. Include `gateway_status` output and any crash message if something fails.

This build uses a custom save extension. Keep prototype saves separate; stock JGRPP is not expected to load saves containing gateway state. Existing-save gateway migration is not supported in this package.

Engine source and the patch are provided with this package under the accompanying licenses. Gateway artwork is the approved blue/cyan preview artwork.
