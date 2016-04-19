<?php
require_once('../commons/base.inc.php');
$output = array();
$output['code'] =  1;
$output['stdout'] = 'None';
$output['stderr'] = 'None';
$output['stdin'] = 'None';
try
{
	$ip    = $_REQUEST['ip'];
	$user        = $_REQUEST['user'];
	$password    = $_REQUEST['password'];
	$outlet      = $_REQUEST['outlet'];
	if (!$ip || !$user || !$password || !$output)
	{
		throw new Exception('error please define example: {url}/fog/service/isi_pdu_reboot.php?host={name}&user={user}&password={password}&outlet={outlet}');
	}
	$command = escapeshellcmd('/usr/bin/python /var/www/fog/service/isi_pdu_reboot.py -i '.$ip.' -u '.$user.' -p '.$password.' -o '.$outlet);
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
    	throw new Exception('error /var/www/fog/service/isi_pdu_reboot.py');
    }
}
catch (Exception $e)
{
	$output['code'] =  1;
	$output['stderr'] = $e->getMessage();	
}
print json_encode($output,JSON_UNESCAPED_SLASHES);