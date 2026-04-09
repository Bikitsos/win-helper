$ErrorActionPreference = 'Stop'

$cultureName = 'en-CY'
$geoId = 57
$currencyLabel = ' '

function Assert-Administrator {
    $currentIdentity = [Security.Principal.WindowsIdentity]::GetCurrent()
    $principal = New-Object Security.Principal.WindowsPrincipal($currentIdentity)
    if (-not $principal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)) {
        throw 'This script must be run as Administrator.'
    }
}

Assert-Administrator

Write-Host "Applying regional settings for $cultureName..."

Write-Host 'Setting current user culture...'
Set-Culture -CultureInfo $cultureName

Write-Host 'Setting current user language list...'
$languageList = New-WinUserLanguageList -Language $cultureName
Set-WinUserLanguageList -LanguageList $languageList -Force

Write-Host 'Setting home location to Cyprus...'
Set-WinHomeLocation -GeoId $geoId

Write-Host 'Setting system locale...'
Set-WinSystemLocale -SystemLocale $cultureName

Write-Host "Replacing currency symbol with '$currencyLabel' for current user..."
$currentUserIntl = 'HKCU:\Control Panel\International'
Set-ItemProperty -Path $currentUserIntl -Name sCurrency -Value $currencyLabel

Write-Host 'Copying current user international settings to welcome screen and new users...'
Copy-UserInternationalSettingsToSystem -WelcomeScreen $true -NewUser $true

Write-Host 'Regional settings updated successfully.'
Write-Host 'Sign out or restart Windows to ensure all applications pick up the new settings.'