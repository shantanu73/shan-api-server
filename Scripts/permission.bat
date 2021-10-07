set SHAN_SERVICE_ACCOUNT=""

icacls "C:\Program Files\shan-api-server" /grant %SHAN_SERVICE_ACCOUNT%:(OI)(CI)(F)
icacls "C:\Python38" /grant %SHAN_SERVICE_ACCOUNT%:(OI)(CI)(F)
icacls "C:\Program Files\nssm-2.24" /grant %SHAN_SERVICE_ACCOUNT%:(OI)(CI)(F)
netsh advfirewall firewall add rule name="TCP Port 443" dir=in action=allow protocol=TCP localport=443

"C:\Program Files\nssm-2.24\win64\nssm.exe" install SHAN_API_SERVER "C:\Program Files\shan-api-server\Scripts\start_server.bat"

powershell -executionPolicy bypass -file "C:\Program Files\shan-api-server\Scripts\modify_service.ps1" %SHAN_SERVICE_ACCOUNT%