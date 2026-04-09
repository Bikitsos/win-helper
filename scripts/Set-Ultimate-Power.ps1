Write-Host "Setting power plan to Ultimate Performance..."

# Check if Ultimate Performance plan already exists
$ultimatePlan = powercfg /l | Select-String "Ultimate Performance"

if (-not $ultimatePlan) {
    Write-Host "Ultimate Performance plan not found. Creating it..."
    $output = powercfg -duplicatescheme e9a42b02-d5df-448d-aa00-03f14749eb61
    $guid = $output -replace '.*GUID: ([a-f0-9\-]+).*','$1'
    powercfg /setactive $guid
} else {
    Write-Host "Ultimate Performance plan already exists. Setting it as active..."
    # Extract GUID from the existing plan
    $guid = $ultimatePlan -replace '.*GUID: ([a-f0-9\-]+).*','$1'
    powercfg /setactive $guid
}

Write-Host "Disabling screen turn-off and sleep on both AC and DC..."
powercfg /change monitor-timeout-ac 0
powercfg /change monitor-timeout-dc 0
powercfg /change standby-timeout-ac 0
powercfg /change standby-timeout-dc 0

Write-Host "Power settings updated successfully."
