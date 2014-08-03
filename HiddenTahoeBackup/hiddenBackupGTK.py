#!/usr/bin/env python

from gi.repository import Gtk, Gio

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

        self.set_default_size(300, 200)

        label = Gtk.Label("enter passphrase")

        box = self.get_content_area()
        box.add(label)

        self.passphraseEntry = Gtk.Entry()
        self.passphraseEntry.set_editable(True)
        self.passphraseEntry.set_visibility(False)
        box.add(self.passphraseEntry)

        self.show_all()


class MainWindow(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="hidden Tahoe-LAFS backup")

        self.hiddenBackup = None

        self.set_position(Gtk.WindowPosition.CENTER)
        self.set_default_size(400, 250)
        self.set_border_width(24)

        self.box = box = Gtk.Box(spacing=20)
        box.set_spacing (5)
        box.set_orientation (Gtk.Orientation.VERTICAL)
        box.set_homogeneous(False)

        self.add(box)

        manifestButton = Gtk.Button("choose backup manifest file")
        manifestButton.connect("clicked", self.on_file_clicked)
        box.pack_start(manifestButton, False, False, 0)

        startButton = Gtk.Button("start Tahoe-LAFS client")
        startButton.connect("clicked", self.start_clicked)
        box.pack_start(startButton, False, False, 0)

        stopButton = Gtk.Button("stop Tahoe-LAFS client")
        stopButton.connect("clicked", self.stop_clicked)
        box.pack_start(stopButton, False, False, 0)

        backupButton = Gtk.Button("backup")
        backupButton.connect("clicked", self.backup_clicked)
        box.pack_start(backupButton, False, False, 0)

        restoreButton = Gtk.Button("restore")
        restoreButton.connect("clicked", self.restore_clicked)
        box.pack_start(restoreButton, False, False, 0)


    def quit(self):
        if self.hiddenBackup.tahoeStarted:
            self.hiddenBackup.stopTahoe()
            self.hiddenBackup.destroyNodeDir()
        reactor.stop()

    def start_clicked(self, widget):
        if self.hiddenBackup is not None:
            self.hiddenBackup.startTahoe()
        else:
            print "hiddenBackup is not initialized"

    def stop_clicked(self, widget):
        self.hiddenBackup.stopTahoe()

    def backup_clicked(self, widget):
        self.hiddenBackup.backup()

    def restore_clicked(self, widget):
        self.hiddenBackup.restore()

    def getPassphrase(self):
        """
        Display a passphrase dialog window.
        returns the user entered passphrase string
        """
        self.fileEntry = Gtk.Entry()
        self.box.pack_start(self.fileEntry, True, True, 0)       
        passDialog = PassphraseDialog(self)
        response = passDialog.run()

        if response == Gtk.ResponseType.OK:
            passphrase = passDialog.passphraseEntry.get_text()
            passDialog.destroy()
            return passphrase

        passDialog.destroy()
        return None

    def on_file_clicked(self, widget):
        self.fileDialog = Gtk.FileChooserDialog("Please choose a file", self,
                                           Gtk.FileChooserAction.OPEN,
                                           (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                                            Gtk.STOCK_OPEN, Gtk.ResponseType.OK))

        self.add_filters(self.fileDialog)

        response = self.fileDialog.run()
        if response == Gtk.ResponseType.OK:
            self.manifest_file = self.fileDialog.get_filename()
            passphrase = self.getPassphrase()
            if passphrase is not None:

                self.hiddenBackup = HiddenBackup(self.manifest_file, passphrase)
                # temporarily hard coded for Tails =-)
                nodeDir = "/home/amnesia/.hiddenTahoe"
                self.hiddenBackup.createNodeDir(nodeDir)

        self.fileDialog.destroy()

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
