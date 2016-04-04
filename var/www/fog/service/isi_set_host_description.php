<?php
require_once('../commons/base.inc.php');
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

        if (!$Host)
        {
        	throw new Exception('error host not found');
        }

       $Host->set('description', $description);
       if ($Host->save()) $Datatosend = "#!ok\n";
       else throw new Exception('#!er: Error adding kernel path');
        print 'True';

}
catch (Exception $e)
{
        print $e->getMessage();
}