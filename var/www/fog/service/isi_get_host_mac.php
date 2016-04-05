<?php
require_once('../commons/base.inc.php');
$output = array();
$output['code'] =  1;
$output['stdout'] = 'None';
$output['stderr'] = 'None';
$output['stdin'] = 'None';
try
{
        $HostManager = new HostManager();
        $hostname    = $_REQUEST['hostname'];
        if (!$hostname)
        {
            throw new Exception('error please define hostname example: {url}/fog/service/isi_get_host_mac.php?hostname={hostname}');
        }
        // Get the host if it exists
        $Host = $HostManager->getHostByName($hostname);
        if(!$Host)
        {
        	throw new Exception('Host not found');
        }
        $output['stdout'] =  $Host->getMACAddress();
        $output['code'] =  0;
}
catch (Exception $e)
{
	$output['code'] =  1;
	$output['stderr'] = $e->getMessage();	
}
print json_encode($output,JSON_UNESCAPED_SLASHES);