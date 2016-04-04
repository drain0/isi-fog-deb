<?php
require_once('../commons/base.inc.php');
try
{
        $HostManager = new HostManager();
        $MACs = $_REQUEST['mac'];
        if (!$MACs)
                throw new Exception('Error unable to get description example: {url}/fog/service/isi_get_host_kernel.php?mac={mac}');
        // Get the Host
        $Host = $HostManager->getHostByMacAddresses($MACs);
        print ''.$Host->get('kernel');
}
catch (Exception $e)
{
        print $e->getMessage();
}