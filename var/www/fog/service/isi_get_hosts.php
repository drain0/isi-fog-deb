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
		$Host = $FOGCore->getClass('Host');
		$macs = $Host->getMyMacs(false);
		$hosts = array();
		foreach ($macs as &$mac) 
		{
			if(!empty($mac))
			{
				$host = $HostManager->getHostByMacAddresses($mac);
				if(!empty($host))
				{
					$hosts[$host->get('name')] = $host->getActiveTaskCount();
				}
			}
		}
        $output['stdout'] = $hosts;
        $output['code'] =  0;
}
catch (Exception $e)
{
	$output['code'] =  1;
	$output['stderr'] = $e->getMessage();	
}
print json_encode($output,JSON_UNESCAPED_SLASHES);