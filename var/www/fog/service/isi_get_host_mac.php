<?php
require_once('../commons/base.inc.php');
try
{
        $HostManager = new HostManager();
        $hostname    = $_REQUEST['hostname'];
        if (!$hostname)
                throw new Exception('error please define hostname example: {url}/fog/service/isi_get_host_mac.php?hostname={hostname}');
        // Get the host if it exists
        $Host = $HostManager->getHostByName($hostname);
        if(!$Host)
        {
        	throw new Exception('Host not found');
        }
        $mac = $Host->getMACAddress();
        print $mac;
}
catch (Exception $e)
{
		print "error:";
        print $e->getMessage();
}