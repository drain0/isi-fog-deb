<?php
require_once('../commons/base.inc.php');
try
{
        $HostManager = new HostManager();
        $hostname    = $_REQUEST['hostname'];
        $kernel_args = $_REQUEST['kernel_args'];

        if (!$hostname)
        {
        	throw new Exception('error please define hostname example: {url}/fog/service/isi_set_host_kernel_args.php?hostname={name}&kernel_args={kernel_args}');
        }

        if (!$kernel_path)
        {
        	throw new Exception('error please define kernel_path example: {url}/fog/service/isi_set_host_kernel_args.php?hostname={name}&kernel_args={kernel_args}');
        }

        // Get the Host
        $Host = $HostManager->getHostByName($hostname);

        if (!$Host)
        {
        	throw new Exception('error host not found');
        }

       $Host->set('kernelArgs', $kernel_args);
       if ($Host->save()) $Datatosend = "#!ok\n";
       else throw new Exception('#!er: Error adding kernel path');
        print 'True';

}
catch (Exception $e)
{
        print $e->getMessage();
}
