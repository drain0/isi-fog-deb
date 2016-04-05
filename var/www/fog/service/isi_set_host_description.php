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
        $description = $_REQUEST['description'];

        if (!$hostname || !$description)
        {
        	throw new Exception('error please define hostname example: {url}/fog/service/isi_set_host_description.php?hostname={name}&description={url path}');
        }

        // Get the Host
        $Host = $HostManager->getHostByName($hostname);
		
        if(!$Host)
        {
        	throw new Exception('Host not found');
        }

       $Host->set('description', $description);
       if ($Host->save())
       {
       $Datatosend = "#!ok\n";
       }
       $output['stdout'] = 'True';
       $output['code'] =  0;

}
catch (Exception $e)
{
	$output['code'] =  1;
	$output['stderr'] = $e->getMessage();	
}
print json_encode($output,JSON_UNESCAPED_SLASHES);