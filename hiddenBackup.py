#!/usr/bin/env python

# internal modules
from tahoeConfig import createTahoeConfigDir, genTahoeConfig, genStorageConfig, createIntroducers
from tahoeCommands import processTasks, tahoeRestore, tahoeBackup, tahoeStart, tahoeStop, watchTahoeCmd
import secretBox

# external modules
import argparse
import json
import sys
import shutil


class HiddenBackup(object):

    def __init__(self, filename, passphrase):
        key = secretBox.hashPassphrase(passphrase)
        self.manifest = json.loads(secretBox.decryptFile(filename, key))
        self.nodeDir = None
        self.tahoeStarted = False

    def createNodeDir(self, nodeDir):
        print "creating temporary Tahoe-LAFS nodeDir %s" % nodeDir
        self.nodeDir = nodeDir
        createTahoeConfigDir(nodeDir=self.nodeDir, manifest=self.manifest)

    def destroyNodeDir(self):
        assert self.nodeDir is not None
        print "destroying temporary Tahoe-LAFS nodeDir %s" % self.nodeDir
        shutil.rmtree(self.nodeDir)

    def startTahoe(self):
        tahoeStart(nodeDir=self.nodeDir)
        self.tahoeStarted = True

    def stopTahoe(self):
        assert self.tahoeStarted
        tahoeStop(nodeDir=self.nodeDir)
        self.tahoeStarted = False

    def restore(self):
        assert self.tahoeStarted
        processTasks(isRestore=True, nodeDir=self.nodeDir, manifest=self.manifest)
    def backup(self):
        assert self.tahoeStarted
        processTasks(isRestore=False, nodeDir=self.nodeDir, manifest=self.manifest)


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('--start', dest='start', default=False, action="store_true", help="start Tahoe-LAFS client")
    parser.add_argument('--stop', dest='stop', default=False, action="store_true", help="stop Tahoe-LAFS client")
    parser.add_argument('--restore', dest='restore', default=False, action="store_true", help="restore")
    parser.add_argument('--backup', dest='backup', default=False, action="store_true", help="backup")
    parser.add_argument('--manifest', dest='manifest', help="Backup manifest", default=None)
    parser.add_argument('--node-directory', dest='nodeDir', help="Specify which Tahoe node directory should be used.", default=None)
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

    #
    ## decrypt and load backup manifest
    #

    manifest_json = secretBox.promptlyDecryptFile(args.manifest)
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
