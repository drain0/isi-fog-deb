<?php
require_once('../commons/base.inc.php');
$output = array();
$output['code'] =  1;
$output['stdout'] = 'None';
$output['stderr'] = 'None';
$output['stdin'] = 'None';
try
{
	$hostname    = $_REQUEST['hostname'];
	$user        = $_REQUEST['user'];
	$password    = $_REQUEST['password'];
	if (!$hostname || !$user || !$password)
	{
		throw new Exception('error please define hostname example: {url}/fog/service/isi_vm_reboot.php?hostname={name}&user={user}&password={password}');
	}
	$command = escapeshellcmd('/usr/bin/python /var/www/fog/service/isi_vm_reboot.py -n '.$hostname.' -u '.$user.' -p '.$password);
	$output['stdin'] = $command;
        $output_str = shell_exec($command);
        if($output_str!="True\n")
        {
        	throw new Exception("${output_str}");
        }
        else{
        $output['stdout'] = $output_str;
        $output['code'] =  0;
        }
    if (!output)
    {
    	throw new Exception('error /var/www/fog/service/isi_vm_reboot.py');
    }
}
catch (Exception $e)
{
	$output['code'] =  1;
	$output['stderr'] = $e->getMessage();	
}
print json_encode($output,JSON_UNESCAPED_SLASHES);
