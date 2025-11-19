
' Скрипт для создания ярлыка на рабочем столе
Set objShell = CreateObject("WScript.Shell")
strDesktop = objShell.SpecialFolders("Desktop")
Set objLink = objShell.CreateShortCut(strDesktop & "\Генератор Паролей.lnk")
objLink.TargetPath = "PasswordGenerator.exe"
objLink.Description = "Генератор Паролей"
objLink.WorkingDirectory = objShell.CurrentDirectory
objLink.Save
