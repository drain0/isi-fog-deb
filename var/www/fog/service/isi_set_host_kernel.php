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
        $hostname    = $_REQUEST['hostname'];
        $kernel_path = $_REQUEST['kernel_path'];

        if (!$hostname || !$kernel_path)
        {
        	//$output['stderr'] ='error please define hostname example: {url}/fog/service/isi_set_host_kernel.php?hostname={name}&kernel_path={url path}';
        	throw new Exception('error please define hostname example: {url}/fog/service/isi_set_host_kernel.php?hostname={name}&kernel_path={url path}');
        }
        // Get the Host
        $Host = $HostManager->getHostByName($hostname);

        if(!$Host)
        {
        	throw new Exception('Host not found');
        }

       $Host->set('kernel', $kernel_path);
       if ($Host->save()){
       	$Datatosend = "#!ok\n";
       }
       else{
       	//$output['stderr'] = "Error adding kernel path";
       	//$output['code'] = 1;
       	//json_encode($output,JSON_UNESCAPED_SLASHES);
       	throw new Exception("Error adding kernel path");
       }
        print 'True';

}
catch (Exception $e)
{
	$output['code'] =  1;
	$output['stderr'] = $e->getMessage();	
}
print json_encode($output,JSON_UNESCAPED_SLASHES);
