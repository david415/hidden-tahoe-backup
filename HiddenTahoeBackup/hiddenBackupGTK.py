#!/usr/bin/env python

# external modules
from gi.repository import Gtk, Gio
import os.path
import shutil

# internal modules
from HiddenTahoeBackup.tahoeConfig import createTahoeConfigDir, genTahoeConfig, genStorageConfig, createIntroducers
from HiddenTahoeBackup.tahoeCommands import processTasks, tahoeRestore, tahoeBackup, tahoeStart, tahoeStop, watchTahoeCmd
from HiddenTahoeBackup.hiddenBackup import HiddenBackup
import HiddenTahoeBackup.secretBox as secretBox


class PassphraseDialog(Gtk.Dialog):

    def __init__(self, parent):
        Gtk.Dialog.__init__(self, "dialog", parent, 0,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
             Gtk.STOCK_OK, Gtk.ResponseType.OK))

        self.set_default_size(300, 100)
        label = Gtk.Label("enter passphrase")
        box = self.get_content_area()
        box.add(label)

        self.passphraseEntry = Gtk.Entry()
        self.passphraseEntry.set_editable(True)
        self.passphraseEntry.set_visibility(False)
        box.add(self.passphraseEntry)

        self.show_all()


class DestroyDirectoryDialog(Gtk.Dialog):

    def __init__(self, parent):
        Gtk.Dialog.__init__(self, "My Dialog", parent, 0,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
             Gtk.STOCK_OK, Gtk.ResponseType.OK))

        self.set_default_size(150, 100)

        label = Gtk.Label("Overwrite existing hiddenTahoe nodeDir %s ?" % parent.nodeDir)

        box = self.get_content_area()
        box.add(label)
        self.show_all()


class MainWindow(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="hidden Tahoe-LAFS backup")

        self.hiddenBackup = None

        self.set_position(Gtk.WindowPosition.CENTER)
        self.set_default_size(400, 200)
        self.set_border_width(10)

        self.box = box = Gtk.Box(spacing=10)
        box.set_orientation (Gtk.Orientation.VERTICAL)
        box.set_homogeneous(False)

        self.add(box)

        manifestButton = Gtk.Button("choose backup manifest file")
        manifestButton.connect("clicked", self.on_file_clicked)
        manifestButton.connect("activate", self.on_file_clicked)
        box.pack_start(manifestButton, False, False, 0)

        backupButton = Gtk.Button("backup")
        backupButton.connect("clicked", self.backup_clicked)
        box.pack_start(backupButton, False, False, 0)

        restoreButton = Gtk.Button("restore")
        restoreButton.connect("clicked", self.restore_clicked)
        box.pack_start(restoreButton, False, False, 0)

        self.on_file_clicked(None)


    def quit(self):
        self.stopTahoeInstance()
        reactor.stop()

    def stopTahoeInstance(self):
        if self.hiddenBackup is not None:
            self.hiddenBackup.stopTahoe()
            self.hiddenBackup.destroyNodeDir()
            self.hiddenBackup = None

    def backup_clicked(self, widget):
        self.hiddenBackup.backup()

    def restore_clicked(self, widget):
        self.hiddenBackup.restore()

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

    def on_file_clicked(self, widget):
        self.fileDialog = Gtk.FileChooserDialog("Please choose an encrypted manifest file", self,
                                           Gtk.FileChooserAction.OPEN,
                                           (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                                            Gtk.STOCK_OPEN, Gtk.ResponseType.OK))

        #self.fileDialog.set_default_size(300, 250)

        self.add_filters(self.fileDialog)

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
        self.hiddenBackup = HiddenBackup(self.manifest_file, passphrase)
        home = os.path.expanduser('~')
        self.nodeDir = os.path.join(home,'.hiddenTahoe')

        if os.path.exists(self.nodeDir):
            # XXX must needs prompt user for permission to destroy
            # and recreate or cancel operation

            print "XXX %s already exists" % self.nodeDir

            destroyDialog = DestroyDirectoryDialog(self)
            response = destroyDialog.run()
            destroyDialog.destroy()

            if response == Gtk.ResponseType.OK:
                # XXX destroy
                shutil.rmtree(self.nodeDir)
                self.hiddenBackup.createNodeDir(self.nodeDir)
            elif response == Gtk.ResponseType.CANCEL:
                print "cancelled destroying old nodeDir %s" % (self.nodeDir,)
                return
        else:
            self.hiddenBackup.createNodeDir(self.nodeDir)

        self.hiddenBackup.startTahoe()

    def add_filters(self, dialog):
        filter_text = Gtk.FileFilter()
        filter_text.set_name("Text files")
        filter_text.add_mime_type("text/plain")
        dialog.add_filter(filter_text)

        filter_py = Gtk.FileFilter()
        filter_py.set_name("Python files")
        filter_py.add_mime_type("text/x-python")
        dialog.add_filter(filter_py)

        filter_any = Gtk.FileFilter()
        filter_any.set_name("Any files")
        filter_any.add_pattern("*")
        dialog.add_filter(filter_any)

class HiddenBackupApp(Gtk.Application):
    def __init__(self):
        Gtk.Application.__init__(self, application_id="apps.test.helloworld",
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
