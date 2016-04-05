<?php
require_once('../commons/base.inc.php');
$output = array();
$output['code'] =  0;
$output['stdout'] = 'None';
$output['stderr'] = 'None';
$output['stdin'] = 'None';
try
{
        $HostManager = new HostManager();
        $MACs = $_REQUEST['mac'];
        if (!$MACs)
        {
        	//$output['stderr'] = 'Error unable to get description example: {url}/fog/service/isi_get_host_kernel.php?mac={mac}';
        	//$output['code'] = 1;
            throw new Exception('Error unable to get description example: {url}/fog/service/isi_get_host_kernel.php?mac={mac}');
        }
        // Get the Host
        $Host = $HostManager->getHostByMacAddresses($MACs);
        if(!$Host)
        {
        	throw new Exception('Host not found');
        }
        print ''.$Host->get('kernelArgs');
}
catch (Exception $e)
{
	$output['code'] =  1;
	$output['stderr'] = $e->getMessage();	
}
print json_encode($output,JSON_UNESCAPED_SLASHES);