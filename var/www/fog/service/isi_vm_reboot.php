<?php
require_once('../commons/base.inc.php');
$output = array();
$output['code'] =  0;
$output['stdout'] = 'None';
$output['stderr'] = 'None';
$output['stdin'] = 'None';
try
{
	$hostname    = $_REQUEST['hostname'];
	if (!$hostname)
	{
		//$output['stderr'] ='error please define hostname example: {url}/fog/service/isi_vm_reboot.php?hostname={name}';
		throw new Exception('error please define hostname example: {url}/fog/service/isi_vm_reboot.php?hostname={name}');
	}
	$command = escapeshellcmd('/usr/bin/python /var/www/fog/service/isi_vm_reboot.py -n ').$hostname;
        $output = shell_exec($command);
        print $output;
    if (!output)
    {
    	//$output['stderr'] ='error /var/www/fog/service/isi_vm_reboot.py';
    	//$output['code'] = 1;
    	throw new Exception('error /var/www/fog/service/isi_vm_reboot.py');
    }
}
catch (Exception $e)
{
	$output['code'] =  1;
	$output['stderr'] = $e->getMessage();	
}
print json_encode($output,JSON_UNESCAPED_SLASHES);
