# Requires Python 3.12 with pip. Does not modify any OpenTTD installation.
$ErrorActionPreference = 'Stop'
$PackageRoot = Split-Path -Parent $PSScriptRoot
& py -3 -m pip install -r (Join-Path $PackageRoot 'requirements.txt')
if ($LASTEXITCODE -ne 0) { throw 'Python dependencies failed' }
& py -3 (Join-Path $PSScriptRoot 'make_sprites.py')
if ($LASTEXITCODE -ne 0) { throw 'Sprite generation failed' }
Push-Location (Join-Path $PackageRoot 'newgrf')
try {
    & py -3 -c "from nml.main import run; run()" --grf teleport-gateway-preview.grf gateway.nml
    if ($LASTEXITCODE -ne 0) { throw 'NewGRF compilation failed' }
} finally { Pop-Location }
