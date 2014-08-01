
import subprocess


def watchTahoeCmd(tahoeCmd=None):
    """Run the given Tahoe-LAFS command and assert that it exits 0
    while watching for new data in realtime."""

    # Torsocks will go away once we merge my native Tor integration for Tahoe-LAFS
    # see tahoe trac ticket #517
    if tahoeCmd.startswith('start') or tahoeCmd.startswith('restart'):
        cmd = "usewithtor tahoe %s" % (tahoeCmd,)
    else:
        cmd = "tahoe %s" % (tahoeCmd,)

    print "watching Tahoe command: %s" % cmd

    pipe = subprocess.Popen(cmd,shell=True)
    while True:
        returncode = pipe.poll()
        if returncode == 0:
            return 0
        elif returncode >= 0:
            raise Exception( "%s exited with %s" % (cmd, returncode) )

def tahoeStop(nodeDir=None):
    return watchTahoeCmd("stop %s" % nodeDir)

def tahoeStart(nodeDir=None):
    return watchTahoeCmd("start %s" % nodeDir)

def tahoeBackup(nodeDir, remote, local, excludes=None):
    if excludes is not None:
        excludes_str = ""
        for exclude in excludes:
            excludes_str += "--exclude='%s' " % exclude
        watchTahoeCmd("-d %s backup -v %s %s %s" % (nodeDir, excludes_str, local, remote))
    else:
        watchTahoeCmd("-d %s backup -v %s %s" % (nodeDir, local, remote))

def tahoeRestore(nodeDir, local, remote, restoreVersion):
    # XXX must needs idempotency!
    watchTahoeCmd("cp -d %s -v -r %s/%s %s" % (nodeDir, remote, restoreVersion, local))

def processTasks(isRestore=None, nodeDir=None, manifest=None):
    for task in manifest['fields']['tasks']:
        remote = task['backupAlias'] + ':' + task['remoteSnapshot']
        local = task['localDirectory']
        if isRestore:
            tahoeRestore(nodeDir, local, remote, restoreVersion=task['restoreVersion'])
        else:
            if 'excludes' in task.keys():
                tahoeBackup(nodeDir, remote, local, excludes=task['excludes'])
            else:
                tahoeBackup(nodeDir, remote, local)
