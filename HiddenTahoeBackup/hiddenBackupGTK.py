#!/usr/bin/env python

# external modules
from gi.repository import Gtk, Gio
import os.path
import shutil
import nacl.exceptions

# internal modules
import HiddenTahoeBackup
from HiddenTahoeBackup.tahoeConfig import createTahoeConfigDir, genTahoeConfig, genStorageConfig, createIntroducers
from HiddenTahoeBackup.tahoeCommands import processTasks, tahoeRestore, tahoeBackup, tahoeStart, tahoeStop, watchTahoeCmd
from HiddenTahoeBackup.hiddenBackup import HiddenBackup
import HiddenTahoeBackup.secretBox as secretBox


class ManifestCreationWindow(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="HiddenTahoe Manifest Creation Console")
        self.set_border_width(10)
        self.set_default_size(500,300)


        self.grid = Gtk.Grid()
        self.add(self.grid)

        manifestLabel = Gtk.Label()
        manifestLabel.set_markup("<b>NOTE:</b> An encrypted backup manifest encapsulates the Tahoe-LAFS configuration\n" +
                               "as well as meta data about your backup and restore operations.\n\n")
        self.grid.add(manifestLabel)

        blank = Gtk.Label()
        self.grid.attach_next_to(blank, manifestLabel, Gtk.PositionType.BOTTOM, 1, 1)

        introLabel = Gtk.Label()
        introLabel.set_markup("Tahoe-LAFS Introducer FURL")
        self.grid.attach(introLabel, 0, 1, 1, 1)

        introEntry = Gtk.Entry()
        introEntry.set_editable(True)
        introEntry.set_width_chars(48)
        self.grid.attach(introEntry, 1, 1, 4, 1)

        blank = Gtk.Label()
        self.grid.attach_next_to(blank, introEntry, Gtk.PositionType.BOTTOM, 1, 1)


        self.aliasNum = 0
        self.aliasOffset = 5

        newCapButton = Gtk.Button("Generate New Cryptographic Alias")
        newCapButton.connect("clicked", self.newAliasCap)
        self.grid.attach(newCapButton, 0, 3, 1, 1)

        existingCapButton = Gtk.Button("Specify Existing Cryptographic Alias")
        existingCapButton.connect("clicked", self.existingAliasCap)
        self.grid.attach(existingCapButton, 3, 3, 1, 1)

        blank = Gtk.Label()
        self.grid.attach_next_to(blank, newCapButton, Gtk.PositionType.BOTTOM, 1, 1)


    def existingAliasCap(self, x):
        print "existingAliasCap"
        self.aliasNum += 1
        row = self.aliasOffset + self.aliasNum
        rowPeers = []

        label = Gtk.Label()
        label.set_markup("existing alias name")
        self.grid.attach(label, 0, row, 1, 1)
        rowPeers.append(label)

        aliasNameEntry = Gtk.Entry()
        aliasNameEntry.set_editable(True)
        aliasNameEntry.set_width_chars(16)
        self.grid.attach(aliasNameEntry, 1, row, 1, 1)
        rowPeers.append(aliasNameEntry)

        label = Gtk.Label()
        label.set_markup("existing cryptographic capability")
        self.grid.attach(label, 2, row, 1, 1)
        rowPeers.append(label)

        aliasCap = Gtk.Entry()
        aliasCap.set_editable(True)
        aliasCap.set_width_chars(32)
        self.grid.attach(aliasCap, 3, row, 1, 1)
        rowPeers.append(aliasCap)

        deleteAliasButton = Gtk.Button("delete alias")
        deleteAliasButton.connect("clicked", lambda ign: self.deleteAliasRow(ign, rowPeers))
        self.grid.attach(deleteAliasButton, 4, row, 1, 1)
        rowPeers.append(deleteAliasButton)

        self.show_all()

    def deleteAliasRow(self, x, rowPeers):
        print "deleteAlias"
        for item in rowPeers:
            self.grid.remove(item)

    def newAliasCap(self, x):
        print "newAliasCap"
        self.aliasNum += 1
        row = self.aliasOffset + self.aliasNum
        rowPeers = []

        label = Gtk.Label()
        label.set_markup("new alias name")
        self.grid.attach(label,0,row,1,1)
        rowPeers.append(label)

        aliasNameEntry = Gtk.Entry()
        aliasNameEntry.set_editable(True)
        aliasNameEntry.set_width_chars(16)
        self.grid.attach(aliasNameEntry,1,row,1,1)
        rowPeers.append(aliasNameEntry)

        deleteAliasButton = Gtk.Button("delete alias")
        deleteAliasButton.connect("clicked", lambda ign: self.deleteAliasRow(ign, rowPeers))
        self.grid.attach(deleteAliasButton, 4, row, 1,1)
        rowPeers.append(deleteAliasButton)
        self.show_all()

    def on_button_toggled(self, button, name):
        if name == "newCap" and button.get_active():
            print "newCap"
            return
        if name == "existingCap" and button.get_active():
            print "existingCap"
            capEntry = Gtk.Entry()
            capEntry.set_editable(True)
            capEntry.set_width_chars(32)
            self.box.add(capEntry)
            self.show_all()

class PassphraseDialog(Gtk.Dialog):

    def __init__(self, parent):
        Gtk.Dialog.__init__(self, "entropic passphrase entry dialog", parent, 0,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
             Gtk.STOCK_OK, Gtk.ResponseType.OK))

        self.set_position(Gtk.WindowPosition.CENTER)
        self.set_default_size(600, 75)

        box = self.get_content_area()
        box.set_orientation (Gtk.Orientation.HORIZONTAL)

        img = Gtk.Image(stock=Gtk.STOCK_DIALOG_AUTHENTICATION)
        box.add(img)

        label = Gtk.Label("passphrase> ")
        label.set_justify(Gtk.Justification.LEFT)
        box.add(label)

        self.passphraseEntry = Gtk.Entry()
        self.passphraseEntry.set_editable(True)
        self.passphraseEntry.set_visibility(False)
        self.passphraseEntry.set_width_chars(64)
        box.add(self.passphraseEntry)
        self.set_keep_above(True)
        self.show_all()
        self.present()

class DestroyDirectoryDialog(Gtk.Dialog):

    def __init__(self, parent):
        Gtk.Dialog.__init__(self, "My Dialog", parent, 0,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
             Gtk.STOCK_OK, Gtk.ResponseType.OK))

        self.set_default_size(150, 100)
        box = self.get_content_area()

        img = Gtk.Image(stock=Gtk.STOCK_DELETE)
        box.add(img)

        label = Gtk.Label("Overwrite existing hiddenTahoe nodeDir %s ?" % parent.nodeDir)
        box.add(label)
        self.show_all()

class BackupRestoreWindow(Gtk.Window):

    def __init__(self, hiddenBackup=None):
        Gtk.Window.__init__(self, title="backup / restore")

        self.hiddenBackup = hiddenBackup

        self.set_position(Gtk.WindowPosition.CENTER)
        self.set_default_size(400, 200)
        self.set_border_width(10)
        self.set_keep_above(True)

        box = Gtk.Box(spacing=10)
        box.set_orientation (Gtk.Orientation.VERTICAL)
        box.set_homogeneous(False)

        self.add(box)

        label = Gtk.Label()
        label.set_markup("Go to <a href=\"http://127.0.0.1:7657\" title=\"Tahoe-LAFS gateway\">Tahoe-LAFS local gateway status page</a>\n" +
                         "to see when your Tahoe-LAFS client is fully connected to the onion grid.")
        box.pack_start(label, False, False, 0)


        backupButton = Gtk.Button("backup")
        backupButton.connect("clicked", self.backup_clicked)
        box.pack_start(backupButton, False, False, 0)

        restoreButton = Gtk.Button("restore")
        restoreButton.connect("clicked", self.restore_clicked)
        box.pack_start(restoreButton, False, False, 0)

    def backup_clicked(self, widget):
        self.hiddenBackup.backup()

    def restore_clicked(self, widget):
        self.hiddenBackup.restore()

class MainWindow(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="hidden Tahoe-LAFS backup")

        self.hiddenBackup = None

        self.set_position(Gtk.WindowPosition.CENTER)
        self.set_default_size(400, 100)
        self.set_border_width(10)
        self.box = box = Gtk.Box(spacing=10)
        box.set_orientation (Gtk.Orientation.VERTICAL)
        box.set_homogeneous(False)
        self.add(box)

        label = Gtk.Label()
        label.set_markup("<b>disclaimer: this is a very early development version with no peer review\n\n\n" +
                         "You must either use an existing backup-manifest or create a new one:</b>")
        box.pack_start(label, False, False, 0)

        manifestButton = Gtk.Button("start Tahoe-LAFS client with existing backup manifest file")
        manifestButton.connect("clicked", self.chooseManifest)
        box.pack_start(manifestButton, False, False, 0)

        manifestButton = Gtk.Button("create new backup manifest file")
        manifestButton.connect("clicked", self.createManifest)
        box.pack_start(manifestButton, False, False, 0)



    def quit(self):
        self.stopTahoeInstance()
        reactor.stop()

    def stopTahoeInstance(self):
        if self.hiddenBackup is not None:
            self.hiddenBackup.stopTahoe()
            self.hiddenBackup.destroyNodeDir()
            self.hiddenBackup = None

    def getPassphrase(self):
        """
        Display a passphrase dialog window.
        returns the user entered passphrase string
        """

        passDialog = PassphraseDialog(self)
        response = passDialog.run()

        if response == Gtk.ResponseType.OK:
            passphrase = passDialog.passphraseEntry.get_text()
            passDialog.destroy()
            return passphrase

        passDialog.destroy()
        return None

    def createManifest(self, widget):
        win = ManifestCreationWindow()
        win.show_all()

    def existingCap(self, x):
        print "existingCap"

    def createNewCapAlias(self, x):
        print "radio"

    def commitManifest(self, x, y):
        print "commiting new manifest to a secretBox file..."

    def chooseManifest(self, widget):
        print "chooseManifest"
        self.fileDialog = Gtk.FileChooserDialog("Please choose an encrypted manifest file", self,
                                           Gtk.FileChooserAction.OPEN,
                                           (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                                            Gtk.STOCK_OPEN, Gtk.ResponseType.OK))

        response = self.fileDialog.run()
        if response == Gtk.ResponseType.OK:
            self.manifest_file = self.fileDialog.get_filename()
            passphrase = self.getPassphrase()
            self.fileDialog.destroy()
            if passphrase is not None:
                self.configAndStartTahoe(self.manifest_file, passphrase)
                return
        self.fileDialog.destroy()

    def configAndStartTahoe(self, manifestFile, passphrase):

        try:
            self.hiddenBackup = HiddenBackup(self.manifest_file, passphrase)
        except nacl.exceptions.CryptoError:
            self.failedVerification(self.manifest_file)
            return

        home = os.path.expanduser('~')
        self.nodeDir = os.path.join(home,'.hiddenTahoe')

        if os.path.exists(self.nodeDir):
            print "nodeDir %s already exists" % self.nodeDir

            destroyDialog = DestroyDirectoryDialog(self)
            response = destroyDialog.run()
            destroyDialog.destroy()

            if response == Gtk.ResponseType.OK:
                shutil.rmtree(self.nodeDir)
                self.hiddenBackup.createNodeDir(self.nodeDir)
            elif response == Gtk.ResponseType.CANCEL:
                print "cancelled destroying old nodeDir %s" % (self.nodeDir,)
                return
        else:
            self.hiddenBackup.createNodeDir(self.nodeDir)

        self.hiddenBackup.startTahoe()

        # after Tahoe starts then prompt for backup/restore operation
        backupRestoreWindow = BackupRestoreWindow(hiddenBackup=self.hiddenBackup)
        backupRestoreWindow.show_all()
        backupRestoreWindow.connect("delete-event", lambda x,y: self.stopTahoeInstance())

    def failedVerification(self, manifestFile):
        print "encrypted backup-manifest (NaCl SecretBox) failed to decrypt %s" % (manifestFile,)
        print "Either you entered an incorrect passphrase or the ciphertext has been tampered with."

        dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.INFO,
                                   Gtk.ButtonsType.OK, "ciphertext VERIFICATION failure")
        dialog.format_secondary_text("encrypted backup-manifest (NaCl SecretBox) failed to decrypt\n" +
                                     "incorrect passphrase or ciphertext/nonce has been tampered with")
        dialog.run()
        dialog.destroy()


class HiddenBackupApp(Gtk.Application):
    def __init__(self):
        Gtk.Application.__init__(self, application_id="apps.devel.HiddenTahoeBackup",
                                 flags=Gio.ApplicationFlags.FLAGS_NONE)
        self.connect("activate", self.on_activate)
        
    def on_activate(self, data=None):
        mainWindow = MainWindow()
        mainWindow.show_all()
        mainWindow.connect("delete-event", lambda x,y: mainWindow.quit())
        self.add_window(mainWindow)

from twisted.internet import gtk3reactor
gtk3reactor.install()

from gi.repository import Gtk
app = HiddenBackupApp()
from twisted.internet import reactor
reactor.registerGApplication(app)
reactor.run()
