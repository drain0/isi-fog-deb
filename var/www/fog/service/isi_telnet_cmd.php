<?php
require_once('../commons/base.inc.php');
$output = array();
$output['code'] =  0;
$output['stdout'] = 'None';
$output['stderr'] = 'None';
$output['stdin'] = 'None';
try
{
	$host    = $_REQUEST['host'];
	$port    = $_REQUEST['port'];
	$cmdline     = $_REQUEST['cmdline'];
	if (!$host || !$port)
	{
		//$output['stderr'] ='error please define hostname example: {url}/fog/service/isi_telnet_cmd.php?host={host}&port={port}&cmdline={cmd}';
		throw new Exception('error please define hostname example: {url}/fog/service/isi_telnet_cmd.php?host={host}&port={port}&cmdline={cmd}');
	}
	if (!$cmdline)
	{
		$cmd = "/usr/bin/python /var/www/fog/service/isi_telnet_cmd.py -H ".$host." -p ".$port;
	}else{
		$cmd = "/usr/bin/python /var/www/fog/service/isi_telnet_cmd.py -H ".$host." -p ".$port." -c '".$cmdline."'";
	}
	$command = escapeshellcmd($cmd);
        $output = shell_exec($command);
        print "<pre>".$output."</pre>";
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
