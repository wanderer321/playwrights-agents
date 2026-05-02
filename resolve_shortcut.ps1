[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$shell = New-Object -ComObject WScript.Shell
$shortcutPath = "$env:APPDATA\Microsoft\Windows\Start Menu\Programs\微信开发者工具\微信开发者工具.lnk"
$lnk = $shell.CreateShortcut($shortcutPath)
Write-Output "TargetPath: $($lnk.TargetPath)"
Write-Output "WorkingDirectory: $($lnk.WorkingDirectory)"
