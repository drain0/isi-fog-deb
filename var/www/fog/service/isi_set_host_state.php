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
        $MAC  = $_REQUEST['mac'];
        $STATE = $_REQUEST['state'];
        if (!$MAC || !$STATE)
        {
            throw new Exception('Error unable to get description example. {url}/fog/service/isi_set_host_state.php?mac={mac}&state={#1-5}');
        }
        // Get the Host
        $Host = $HostManager->getHostByMacAddresses($MAC);
        if(!$Host)
        {
        	throw new Exception('Host not found');
        }
        $Task = $Host->get('task');
        #if (!$Task->isValid()) throw new Exception(sprintf('%s: %s (%s)',_('No Active Task found for Host'), $Host->get('name'),$Host->get('mac')));
        
        if (!in_array($Task->get('typeID'),array(12,13)))
        {
        	$Task->set('stateID',$STATE);
        }

        
        if (!$Task->save()) {
        	$EventManager->notify('HOST_IMAGE_Fail', array(HostName=>$Host->get('name')));
        	throw new Exception('Failed to update task.');
        }
        if($STATE=='4')
        {
        	// Log it
        	$ImagingLogs = $FOGCore->getClass('ImagingLogManager')->find(array('hostID' => $Host->get('id')));
        	foreach($ImagingLogs AS $ImagingLog) $id[] = $ImagingLog->get('id');
        	// Update Last deploy
        	$Host->set('deployed',date('Y-m-d H:i:s'))->save();
        	$il = new ImagingLog(max($id));
        	$il->set('finish',date('Y-m-d H:i:s'))->save();
        	// Task Logging.
        	$TaskLog = new TaskLog($Task);
        	$TaskLog->set('taskID',$Task->get('id'))->set('taskStateID',$Task->get('stateID'))->set('createdTime',$Task->get('createdTime'))->set('createdBy',$Task->get('createdBy'))->save();
        	$EventManager->notify('HOST_IMAGE_COMPLETE', array(HostName=>$Host->get('name')));
        }
        
        if($STATE=='6')
        {
        	// Log it
        	$ImagingLogs = $FOGCore->getClass('ImagingLogManager')->find(array('hostID' => $Host->get('id')));
        	foreach($ImagingLogs AS $ImagingLog) $id[] = $ImagingLog->get('id');
        	// Update Last deploy
        	$Host->set('deployed',date('Y-m-d H:i:s'))->save();
        	$il = new ImagingLog(max($id));
        	$il->set('finish',date('Y-m-d H:i:s'))->save();
        	// Task Logging.
        	$TaskLog = new TaskLog($Task);
        	$TaskLog->set('taskID',$Task->get('id'))->set('taskStateID',$Task->get('stateID'))->set('createdTime',$Task->get('createdTime'))->set('createdBy',$Task->get('createdBy'))->save();
        	$EventManager->notify('HOST_IMAGE_COMPLETE', array(HostName=>$Host->get('name')));
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