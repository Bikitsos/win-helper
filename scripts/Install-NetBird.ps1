$ErrorActionPreference = 'Stop'

$packageId = 'Netbird.Netbird'

if (-not (Get-Command winget -ErrorAction SilentlyContinue)) {
    throw 'winget is not installed or not available in PATH. Run the Winget installer first.'
}

Write-Host "Installing NetBird with winget package $packageId..."

winget install \
    --id $packageId \
    --exact \
    --source winget \
    --accept-package-agreements \
    --accept-source-agreements

if ($LASTEXITCODE -ne 0) {
    throw "winget install failed with exit code $LASTEXITCODE."
}

Write-Host 'NetBird installation completed successfully.'