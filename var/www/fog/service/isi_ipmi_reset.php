<?php
require_once('../commons/base.inc.php');
$output = array();
$output['code'] =  0;
$output['stdout'] = 'None';
$output['stderr'] = 'None';
$output['stdin'] = 'None';
try
{
	$ip      = $_REQUEST['ip'];
	$user    = $_REQUEST['user'];
	$password= $_REQUEST['password'];
	if (!$ip || !$user || !$password)
	{
		//$output['stderr'] = 'error please define hostname example: {url}/fog/service/isi_ipmi_reset.php?ip={ip}&user={user}&password={password}';
		throw new Exception('error please define hostname example: {url}/fog/service/isi_ipmi_reset.php?ip={ip}&user={user}&password={password}');
	}
	$cmd = "/usr/bin/python /var/www/fog/service/isi_ipmi_reset.py -i ".$ip." -u ".$user." -p ".$password;
	$command = escapeshellcmd($cmd);
        $output = shell_exec($command);
        print $output;
    if (!output)
    {
    	//$output['code'] = 1;
    	//$output['stderr'] = 'error /var/www/fog/service/isi_vm_reboot.py';
    	throw new Exception('error /var/www/fog/service/isi_vm_reboot.py');
    }
}
catch (Exception $e)
{
	$output['code'] =  1;
	$output['stderr'] = $e->getMessage();	
}
print json_encode($output,JSON_UNESCAPED_SLASHES);
