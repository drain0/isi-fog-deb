<?php
require_once('../commons/base.inc.php');
$output = array();
$output['code'] =  1;
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
		throw new Exception('error please define hostname example: {url}/fog/service/isi_ipmi_reset.php?ip={ip}&user={user}&password={password}');
	}
	$cmd = "/usr/bin/python /var/www/fog/service/isi_ipmi_reset.py -i ".$ip." -u ".$user." -p ".$password;
	$output['stdin'] = $cmd;
        $output_str = shell_exec($cmd);
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
    	throw new Exception('error /var/www/fog/service/isi_ipmi_reset.py');
    }
}
catch (Exception $e)
{
	$output['code'] =  1;
	$output['stderr'] = $e->getMessage();	
}
print json_encode($output,JSON_UNESCAPED_SLASHES);
