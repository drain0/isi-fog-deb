'''
Created on Nov 18, 2015

:author: iitow
'''
import atexit
import os
import io
import pty
import select
import shlex
import subprocess
import sys
import time

this_path = os.path.dirname(os.path.realpath(__file__))


def waitfor(fd):
    '''poll the child for input
    
    :param fd: forked process
    '''
    poll = select.poll()
    poll.register(fd, select.POLLIN)
    poll.poll()
    return os.read(fd, 1024)


def event(fd, searches):
    '''find all output and inspect it for searches dict key & value
    
    :param fd: forked process
    :param searches: dictionary key value pair
    '''
    while True:
        output = waitfor(fd)
        if output:
            output = str(output).lower()
            print output
        for key, value in searches.iteritems():
            if key in output:
                os.write(fd, value+"\n")
                waitfor(fd)
                print "[prompt] [%s] Found" % key
                return key
            else:
                pass


def set_rsa(host, rsa_pub, user, password):
    '''logs into system via ssh and appends to authorized_keys using username password
    
    :param     host: name over the server
    :param  rsa_pub: absolute path to your id_rsa.pub
    :param     user: host login creds
    :param password: host login creds
    :param home_dir: home directory for user
    '''
    output = None
    with open(rsa_pub, 'r') as file:
        output = file.read()
    cmd = '/bin/mkdir -p /root/.ssh && echo "%s" >>'
    ' /root/.ssh/authorized_keys &&'
    ' /bin/chmod -R 600 /root/.ssh' % (output.strip())
    pid, fd = pty.fork()
    if pid == 0:
        os.execvp("/usr/bin/ssh", ["ssh",
                                   user+'@'+host,
                                   '-o',
                                   'NumberOfPasswordPrompts=1',
                                   '-o',
                                   'StrictHostKeyChecking=no',
                                   '-o',
                                   'UserKnownHostsFile=/dev/null',
                                   cmd])
    elif pid > 0:
        searches = {'password': password, 'continue connecting': 'yes'}
        if event(fd, searches) == 'continue connecting':
            event(fd, searches)
        os.wait4(pid,  0)
        os.close(fd)


def create_rsa_public(rsa_private):
    '''generate a public key from the private key
    
    :param rsa_private: path to private key
    '''
    rsa_public = "%s.pub" % rsa_private
    if not os.path.exists(rsa_public):
        cmd = 'ssh-keygen -y -f %s > %s' % (rsa_private, rsa_public)
        shell(cmd, shell=True)
    return rsa_public


def ssh(server,
        cmd,
        rsa_private='/root/.ssh/id_rsa.default',
        add_rsa=False,
        user='root',
        password='a',
        strict=True,
        verbose=True,
        show_cmd=True,
        shell_set=True):
    '''Run a single ssh command on a remote server
    
    :param server: username@servername
    :param cmd: single command you wish to run
    '''
    if add_rsa:
        public = create_rsa_public(rsa_private)
        set_rsa(server, public, user, password)
    try:
        output = shell("ssh -o LogLevel=quiet"
                       " -o NumberOfPasswordPrompts=0"
                       " -o StrictHostKeyChecking=no"
                       " -o UserKnownHostsFile=/dev/null -i %s %s@%s \"%s\""
                       % (rsa_private,
                          user,
                          server,
                          cmd),
                       strict=strict,
                       verbose=verbose,
                       show_cmd=show_cmd,
                       shell=shell_set)
    except IOError as e:
        print "Error in ssh: %s" % (e)
    return output


def rsync(server,
          src,
          dest,
          option='pull',
          remote=True,
          excludes=[],
          rsa_private='/root/.ssh/id_rsa.default',
          user='root',
          verbose=False):
    ''' Performs an rsync of files; requires ssh keys setup.
    
    :param   server: username@server
    :param      src: full path of src directory/file
    :param     dest: full path to dest directory
    :param   option: [pull] get file from a remote,[push] put a file from your server into a remote
    :param   remote: [True] assumes we are working with a remote system, [False] assumes we are copying files locally
    :param excludes: exclude directory, or file from array
    :note: --delete will delete files on dest if it does not match src
    '''
    excludes_str = ''
    if excludes:
        for exclude in excludes:
            excludes_str = "%s --exclude=%s" % (excludes_str, exclude)
    if remote:
        if option == 'pull':
            try:
                session = shell("rsync -e \"ssh"
                                " -oStrictHostKeyChecking=no"
                                " -oUserKnownHostsFile=/dev/null -i %s\""
                                " -Pavz %s"
                                " --delete %s@%s:%s %s" % (rsa_private,
                                                           excludes_str,
                                                           user,
                                                           server,
                                                           src,
                                                           dest),
                                strict=True,
                                verbose=verbose,
                                shell=True)
            except IOError as e:
                print "Error in rsync: %s" % (e)
        elif option == 'push':
            try:
                session = shell("rsync -e \"ssh"
                                " -oStrictHostKeyChecking=no"
                                " -oUserKnownHostsFile=/dev/null -i %s\""
                                " -Pavz %s"
                                " --delete %s %s@%s:%s" % (rsa_private,
                                                           excludes_str,
                                                           src,
                                                           user,
                                                           server,
                                                           dest),
                                strict=True,
                                verbose=verbose,
                                shell=True)
            except IOError as e:
                print "Error in rsync: %s" % (e)
        elif option == 'local':
            try:
                session = shell("rsync -Pavz %s --delete %s %s" % (excludes_str,
                                                                   src,
                                                                   dest),
                                strict=True,
                                verbose=verbose,
                                shell=True)
            except IOError as e:
                print "Error in rsync: %s" % (e)
    else:
        print "Invalid option: %s" (option)
    return session


def shell(cmd,
          verbose=True,
          strict=False,
          shell=True,
          buffer_size=1048576,
          show_cmd=True):
    
    '''Run Shell commands  [Non Blocking, no Buffer, print live, log it]
    
    :param cmd: String command
    :param verbose:bool
    :param strict:bool will exit based on code if enabled
    :param shell:bool, run as a shell client
    :param buffer_size: int, for large amounts of output
    :return:  {command, stdout, code} as dict
    '''
    path = os.path.dirname(os.path.realpath(__file__))
    stamp = str(int(time.time()))
    temp_path = path+os.sep+".tmp_shell_"+stamp+".log"
    output = ""
    if verbose or show_cmd:
        print "\n[%s]\n" % (cmd)
    if shell is False:
        cmd = shlex.split(cmd)
    with io.open(temp_path, 'wb', buffering=buffer_size)as writer:
        with io.open(temp_path, 'rb', buffering=buffer_size) as reader:
            process = subprocess.Popen(cmd,
                                       stdout=writer,
                                       stderr=writer,
                                       shell=shell)
            while process.poll() is None:
                out = reader.read()
                output = output+out
                if verbose:
                    sys.stdout.write(out)
                time.sleep(0.5)
            out = reader.read()
            output = output+out
        if verbose:
            sys.stdout.write(out)
    cmd_info = {'cmd': "".join(cmd),
                'stdout': output,
                'code': process.returncode}
    if os.path.isfile(temp_path):
        os.remove(temp_path)
    if strict is True and int(cmd_info.get("code")) > 0:
        print "\n [Fatal Error] %s \n" % (cmd_info.get("stdout"))
        os.sys.exit(int(cmd_info.get("code")))
    return cmd_info


def _exit_clean():
    ''' cleans .tmp_shell files before exit
    '''
    for file in os.listdir(this_path):
        if ".tmp_shell_" in file:
            file_remove = this_path+os.sep+file
            os.remove(file_remove)
atexit.register(_exit_clean)
