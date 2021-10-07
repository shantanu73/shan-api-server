$svc = Get-WmiObject win32_service -filter "name='SHAN_API_SERVER'"
$svc.Change($Null, $Null, $Null, $Null, $Null, $Null, $args[0], "")