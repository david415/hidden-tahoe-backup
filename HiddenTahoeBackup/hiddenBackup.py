

# internal modules
from HiddenTahoeBackup.tahoeConfig import createTahoeConfigDir, genTahoeConfig, genStorageConfig, createIntroducers
from HiddenTahoeBackup.tahoeCommands import processTasks, tahoeRestore, tahoeBackup, tahoeStart, tahoeStop, watchTahoeCmd
import HiddenTahoeBackup.secretBox as secretBox

# external modules
import json
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
        assert not self.tahoeStarted
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
