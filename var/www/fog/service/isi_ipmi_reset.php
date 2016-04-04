<?php
require_once('../commons/base.inc.php');
try
{
	$ip      = $_REQUEST['ip'];
	$user    = $_REQUEST['user'];
	$password= $_REQUEST['password'];
	if (!$ip || !$user || !$password)
	{
		throw new Exception('error please define hostname example: {url}/fog/service/isi_ipmi_reset.php?ip={ip}&user={user}&password={password}');
	}
	$cmd = "/usr/bin/python /var/www/fog/service/isi_ipmi_reset.py -i ".$ip." -u ".$user." -p ".$password;
	$command = escapeshellcmd($cmd);
        $output = shell_exec($command);
        print $output;
    if (!output)
    {
        throw new Exception('error /var/www/fog/service/isi_vm_reboot.py');
    }
}
catch (Exception $e)
{
	print $e->getMessage();
}
