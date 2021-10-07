set CERT_DOMAIN=""
set CERT_EMAIL=""
set CERT_TOKEN=""

set CERT_FILE_PATH="C:\Program Files\shan-api-server\certificates"
set CERT_SCRIPT="C:\Program Files\shan-api-server\Scripts\restart_service.bat"
wacs.exe --target manual --host %CERT_DOMAIN% --emailaddress %CERT_EMAIL% --accepttos --store pemfiles --pemfilespath %CERT_FILE_PATH% --validationmode dns-01 --validation cloudflare --cloudflareapitoken %CERT_TOKEN% --installation script --script %CERT_SCRIPT%
net start "SHAN_API_SERVER"