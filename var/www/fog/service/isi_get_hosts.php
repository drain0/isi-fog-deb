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
					$Task = $host->get('task');
					$state = $Task->get('stateID');
					if(empty($state))
					{
						$state="0";
					}
					$hosts[$host->get('name')] = (int)$state;
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