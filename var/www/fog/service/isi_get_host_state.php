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
        if (!$hostname)
        {
        	throw new Exception('error please define hostname example: {url}/fog/service/isi_get_host_state.php?hostname={name}');
        }
        // Get the Host
        $Host = $HostManager->getHostByName($hostname);
        if(!$Host)
        {
        	throw new Exception('Host not found');
        }
        $Task = $Host->get('task');
        if (!$Task->isValid()) throw new Exception(sprintf('%s: %s (%s)',_('No Active Task found for Host'), $Host->get('name'),$Host->get('mac')));
        $state = $Task->get('stateID',$STATE);
        $STATE_DICT = array();
        $STATE_DICT['state']=$state;
        $output['stdout'] = $STATE_DICT;
        $output['code'] = 0;
        
}
catch (Exception $e)
{
	$output['code'] =  1;
	$output['stderr'] = $e->getMessage();	
}
print json_encode($output,JSON_UNESCAPED_SLASHES);
