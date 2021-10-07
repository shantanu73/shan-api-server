$eligibilityGroupsFile = $args[0]
$user = $args[1]
$givenAdminGroup = $args[2]
$timeToElevate = $args[3]

$flag = "ShanPowershell1"
$adReachable = $true

try {
    $adminMembers = Get-ADGroupMember -Identity $givenAdminGroup -Recursive | Select -ExpandProperty SamAccountName
}
catch {
    Write $_.Exception.GetType().FullName, $_.Exception.Message
    $flag = "ShanPowershell2"
    $adReachable = $false
}

If ($adReachable) {
    If ($adminMembers -contains $user) {
        $flag = "ShanPowershell3"
    }
    Else {
        $groupConfigFlag = $false
        foreach($line in [System.IO.File]::ReadLines($eligibilityGroupsFile)) {
            $eligibilityGroup, $adminGroup = $line.Split(":")
            If ($adminGroup -eq $givenAdminGroup) {
                $groupConfigFlag = $true
                $members = Get-ADGroupMember -Identity $eligibilityGroup -Recursive | Select -ExpandProperty SamAccountName
                If ($members -contains $user) {
                    try{
                        Add-ADGroupMember -Identity $adminGroup -Members $user -MemberTimeToLive (New-TimeSpan -Hours $timeToElevate)
                        $flag = "ShanPowershell4"
                    }
                    catch {
                        Write $_.Exception.GetType().FullName, $_.Exception.Message
                        $flag = "ShanPowershell5"
                    }
                    break
                }
            }
        }
        If ( -not $groupConfigFlag ) {
            $flag = "ShanPowershell6"
        }
    }
}

Write $flag
