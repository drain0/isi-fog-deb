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
        $taskTypeID  = $_REQUEST['taskTypeID'];
        $taskName    = 'Custom Kernel';
        if (!$hostname || !$taskTypeID)
        	throw new Exception('error please define hostname example: {url}/fog/service/isi_queue_host.php?hostname={name}&taskTypeID={id}');
        // Get the Host
        $Host = $HostManager->getHostByName($hostname);
        if(!$Host)
        {
        	throw new Exception('Host not found');
        }
        $Host->createImagePackage($taskTypeID, $taskName, false, false, -1, false, 'fog');
        $output['stdout'] = 'True';
        $output['code'] =  0;
}
catch (Exception $e)
{
	$output['code'] =  1;
	$output['stderr'] = $e->getMessage();	
}
print json_encode($output,JSON_UNESCAPED_SLASHES);
