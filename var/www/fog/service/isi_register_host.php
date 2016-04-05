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
        $mac         = $_REQUEST['mac'];
        if (!$hostname || !$mac)
        {
        	//$output['stderr'] = 'error please define hostname example: {url}/fog/service/isi_register_host.php?hostname={hostname}&mac={mac}';
        	//$output['code'] = 1;
        	throw new Exception('error please define hostname example: {url}/fog/service/isi_register_host.php?hostname={hostname}&mac={mac}');
        }
        // Get the host if it exists
        $Host = $HostManager->getHostByName($hostname);
        if(!$Host)
        {
        	foreach($FOGCore->getClass('ModuleManager')->find() AS $Module) $ModuleIDs[] = $Module->get('id');
        	$MACs = explode('|',$_REQUEST['mac']);
        	$PriMAC = array_shift($MACs);
        	$Host = $FOGCore->getClass('Host')
        	->set('name', $_REQUEST['hostname'])
        	->set('description','isi_registration=True')
        	->set('pending',0)
        	->set('imageID',1)
        	->set('useAD',0)
        	->set('sec_tok','')
        	->set('pub_key','')
        	->addModule($ModuleIDs)
        	->addPriMAC($PriMAC)
        	->save();
        	foreach($MACs AS $MAC) $AllMacs[] = strtolower($MAC);
        	$KnownMacs = $Host->getMyMacs(false);
        	$MACs = array_unique(array_diff((array)$AllMacs,(array)$KnownMacs));
        	$Host->addPendMAC($MACs);
        	$Host->save();
        	$output['stdout'] = 'True';
        	$output['code'] =  0;
        	
        }else{
        	//$output['stderr'] ='Host Already Exists';
        	//$output['code'] = 1;
        	throw new Exception('Host Already Exists');
        }
}
catch (Exception $e)
{
	$output['code'] =  1;
	$output['stderr'] = $e->getMessage();	
}
print json_encode($output,JSON_UNESCAPED_SLASHES);