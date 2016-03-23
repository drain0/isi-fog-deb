<?php
require_once('../commons/base.inc.php');
try
{
	$hostname    = $_REQUEST['hostname'];
	if (!$hostname)
	{
		throw new Exception('error please define hostname example: {url}/fog/service/isi_queue_host.php?hostname={name}');
	}
	$command = escapeshellcmd('/usr/bin/python /var/www/fog/service/isi_vm_reboot.py -n ').$hostname;
        $output = shell_exec($command);
        print $output;
    if (!output)
    {
        throw new Exception('error /var/www/fog/service/isi_vm_reboot.py');
    }
}
catch (Exception $e)
{
	print $e->getMessage();
}
