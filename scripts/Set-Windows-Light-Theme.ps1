Write-Host "Setting Windows theme to Light..."

# The registry method often fails to apply fully if the script is run as Administrator
# because HKCU points to the Admin profile, or it just fails to broadcast the UI update.
# Applying the default aero.theme is the most reliable way to switch to the Light theme.

$themeFile = "C:\Windows\Resources\Themes\aero.theme"

if (Test-Path $themeFile) {
    Write-Host "Applying $themeFile..."
    Invoke-Item $themeFile
    
    # Give Windows a moment to apply the theme and open the Settings window
    Start-Sleep -Seconds 2
    
    # Close the Settings app that opens automatically when executing a .theme file
    Stop-Process -Name "SystemSettings" -ErrorAction SilentlyContinue
    
    Write-Host "Windows theme set to Light successfully."
} else {
    Write-Host "Windows Light theme file not found at $themeFile."
}

