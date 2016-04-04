<?php
require_once('../commons/base.inc.php');
try
{
        $HostManager = new HostManager();
        $hostname    = $_REQUEST['hostname'];
        if (!$hostname)
                throw new Exception('error please define hostname example: {url}/fog/service/isi_get_host_state.php?hostname={name}');
        // Get the Host
        $Host = $HostManager->getHostByName($hostname);
        if (!$Host)
        	throw new Exception('Host does not exist');
        $isActive = $Host->getActiveTaskCount();
        if($isActive >= 1)
        {
	        $status   = implode(',',$Host->getActiveTask());
	        print "is active:".$isActive;
	        print "   status:".$status;
        }
}
catch (Exception $e)
{
        print $e->getMessage();
}
