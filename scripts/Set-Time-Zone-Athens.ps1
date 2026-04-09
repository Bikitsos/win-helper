Write-Host "Setting Time Zone to Athens, Bucharest..."
Set-TimeZone -Id "GTB Standard Time"

Write-Host "Enabling automatic Daylight Savings Time adjustment..."
# 0 means Daylight Savings adjustment is enabled, 1 means disabled
Set-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Control\TimeZoneInformation" -Name "DynamicDaylightTimeDisabled" -Value 0 -Type DWord -Force

Write-Host "Time zone configured successfully."
