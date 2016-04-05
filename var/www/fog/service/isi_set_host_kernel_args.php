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
        $kernel_args = $_REQUEST['kernel_args'];

        if (!$hostname || !$kernel_path)
        {
        	//$output['stderr'] = 'error please define hostname example: {url}/fog/service/isi_set_host_kernel_args.php?hostname={name}&kernel_args={kernel_args}';
        	throw new Exception('error please define hostname example: {url}/fog/service/isi_set_host_kernel_args.php?hostname={name}&kernel_args={kernel_args}');
        }

        // Get the Host
        $Host = $HostManager->getHostByName($hostname);

        if(!$Host)
        {
        	throw new Exception('Host not found');
        }

       $Host->set('kernelArgs', $kernel_args);
       if ($Host->save()){
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
