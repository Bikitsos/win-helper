Write-Host "Disabling Windows Update service..."
Stop-Service -Name wuauserv -Force -ErrorAction SilentlyContinue
Set-Service -Name wuauserv -StartupType Disabled -ErrorAction SilentlyContinue

Write-Host "Configuring registry to disable automatic updates..."
$registryPath = "HKLM:\SOFTWARE\Policies\Microsoft\Windows\WindowsUpdate\AU"
if (!(Test-Path $registryPath)) {
    New-Item -Path $registryPath -Force | Out-Null
}
Set-ItemProperty -Path $registryPath -Name "NoAutoUpdate" -Value 1 -Type DWord -Force

Write-Host "Windows Update disabled successfully."
