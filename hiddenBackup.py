#!/usr/bin/env python

import argparse
import json
import sys
import re
import os
import os.path
import subprocess
import time

# XXX TODO: generate the "introducers" file
def createIntroducers(introducerNodes, tahoeDir=None):
    pass

def genStorageConfig(storageNodes):
    config = "\n[client-server-selection]"
    for name, furl in storageNodes.items():
        m = re.match(r'pb://(.*)@.+', furl)
        if m:
            seed = m.group(1)
        else:
            print "fail"
            sys.exit(-1)
        config += """
server.v0-%s.type = tahoe-foolscap
server.v0-%s.nickname = %s
server.v0-%s.seed = %s
server.v0-%s.furl = %s
""" % (seed, seed, name, seed, seed, seed, furl)

    return config

def genTahoeConfig(manifest, tahoeDir=None):

    if len(manifest['fields']['introducerNodes']) > 1:
        createIntroducers(manifest['fields']['introducerNodes'], tahoeDir=tahoeDir)
        client = """
[client]
shares.needed = 3
shares.happy = 6
shares.total = 6
"""
    else:
        client = """
[client]
introducer.furl = %s
shares.needed = 3
shares.happy = 6
shares.total = 6
""" % manifest['fields']['introducerNodes'][0]

    config = """
[node]
nickname = client
web.reveal_storage_furls = true
web.port = tcp:7657:interface=127.0.0.1
web.static = public_html
tub.location = client.fakelocation:1
[storage]
enabled = false
[helper]
enabled = false
[drop_upload]
enabled = false
""" % manifest['fields']['introducerNodes']

    if len(manifest['fields']['storageNodes']) > 0:
        config += genStorageConfig(manifest['fields']['storageNodes'])

    return client + config


# XXX TODO: make idempotent
def createTahoeConfigDir(nodeDir=None, manifest=None):

    # XXX
    watchTahoeCmd("create-client %s" % (nodeDir,))

    config = genTahoeConfig(manifest)

    # XXX
    config_fh = open(nodeDir + '/tahoe.cfg', 'w')
    config_fh.write(config)
    config_fh.close()

    # Tahoe-LAFS cryptographic capability aliases
    aliases_str = ""
    for name, capability in manifest['fields']['snapshotAliases'].items():
        aliases_str += name + ": " + capability + "\n"

    # XXX
    aliases_file = os.path.join(nodeDir, 'private', 'aliases')
    aliases_fh = open(aliases_file, 'w')
    aliases_fh.write(aliases_str)
    aliases_fh.close()

def watchTahoeCmd(tahoeCmd=None):
    """Run the given Tahoe-LAFS command and assert that it exits 0 while watching for new data in realtime."""

    if tahoeCmd.startswith('start'):
        cmd = "usewithtor tahoe %s" % (tahoeCmd,)
    else:
        cmd = "tahoe %s" % (tahoeCmd,)

    print "watchTahoeCmd: %s" % cmd

    pipe = subprocess.Popen(cmd,shell=True)
    while True:
        returncode = pipe.poll()
        if returncode == 0:
            return 0
        elif returncode >= 0:
            raise Exception( "%s exited with %s" % (cmd, returncode) )
    return

def tahoeStop(nodeDir=None):
    return watchTahoeCmd("stop %s" % nodeDir)

def tahoeStart(nodeDir=None):
    return watchTahoeCmd("start %s" % nodeDir)

def tahoeBackup(nodeDir, remote, local, excludes=None):
    # XXX

    print "tahoeBackup"

    if excludes is not None:
        excludes_str = ""
        for exclude in excludes:
            excludes_str += "--exclude='%s' " % exclude
        watchTahoeCmd("-d %s backup -v %s %s %s" % (nodeDir, excludes_str, local, remote))
    else:
        watchTahoeCmd("-d %s backup -v %s %s" % (nodeDir, local, remote))

def tahoeRestore(nodeDir, local, remote, restoreVersion):
    # XXX idempotency!
    print "tahoeRestore"
    watchTahoeCmd("cp -d %s -v -r %s/%s %s" % (nodeDir, remote, restoreVersion, local))

def processTasks(isRestore=None, nodeDir=None, manifest=None):
    print "processTasks"
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


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('--start', dest='start', default=False, action="store_true", help="start Tahoe-LAFS client")
    parser.add_argument('--stop', dest='stop', default=False, action="store_true", help="stop Tahoe-LAFS client")
    parser.add_argument('--restore', dest='restore', default=False, action="store_true", help="restore")
    parser.add_argument('--backup', dest='backup', default=False, action="store_true", help="backup")
    parser.add_argument("--manifest", dest='manifest', help="Backup manifest", default=None)
    parser.add_argument("--node-directory", dest='nodeDir', help="Specify which Tahoe node directory should be used.", default=None)
    args = parser.parse_args()

    if args.start is True and args.stop is True:
        print "Must specific either start or stop."
        parser.print_help()
        return

    if not args.start and not args.stop:
        if args.restore is False and args.backup is False:
            print "Must specific either backup or restore."
            parser.print_help()
            return -1

    if args.nodeDir is None:
        parser.print_help()
        return -1

    if args.manifest is None:
        parser.print_help()
        return -1

    # load backup manifest
    manifest_fh = open(args.manifest, 'ro')
    manifest_json = manifest_fh.read()
    manifest_fh.close()
    manifest = json.loads(manifest_json)

    if args.start:
        # XXX TODO: make idempotent
        createTahoeConfigDir(nodeDir=args.nodeDir, manifest=manifest)

        # XXX
        tahoeStart(nodeDir=args.nodeDir)        
        return 0

    if args.stop:
        # XXX
        tahoeStop(nodeDir=args.nodeDir)        
        return 0

    processTasks(isRestore=args.restore, nodeDir=args.nodeDir, manifest=manifest)

    return 0

if __name__ == '__main__':
    sys.exit(main())
