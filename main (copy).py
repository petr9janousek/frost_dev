#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  miniTerm.py

# Importing the libraries
import os
from tkinter import HORIZONTAL, VERTICAL
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
gi.require_version('Vte', '2.91')  # vte-0.38 (gnome-3.4)
from gi.repository import Vte, GLib, GObject

class Handlers():
    """[summary] GTK builder connects contained methods with signals"""
    def on_appWindow_destroy(self, *args):
        Gtk.main_quit()

class Terminal(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="FROST >> FAST ROS TOOL")
        self.set_default_size(800, 600)
        self.set_border_width(3)

        self.vbox = Gtk.Box(orientation=1, spacing=3)
        self.add(self.vbox)
        
        self.button1 = Gtk.Button(label="Hello")
        self.button1.connect("clicked", self.on_button1_clicked)
        self.vbox.pack_start(self.button1, True, True, 0)

        self.notebook = Gtk.Notebook()
        self.vbox.pack_end(self.notebook, True, True, 0)
        VTE_ADDITIONAL_WORDCHARS = "-,./?%&#:_";

        self.term1 = Vte.Terminal.new()
        self.term1.set_size(30, 3)
        self.term1.set_mouse_autohide(True)
        self.term1.set_scroll_on_output(True)
        self.term1.set_audible_bell(True)
        self.term1_pty = self.term1.pty_new_sync(Vte.PtyFlags.DEFAULT, None)
        self.term1.set_pty(self.term1_pty)
        self.term1.set_word_char_exceptions(VTE_ADDITIONAL_WORDCHARS)
        self.term1_fd = Vte.Pty.get_fd(self.term1_pty)
        self.term1.spawn_async(
                Vte.PtyFlags.DEFAULT, #default is fine
                os.environ['HOME'], #where to start the command?
                ["/bin/bash"], #where is the emulator?
                [""], #it's ok to leave this list empty
                GLib.SpawnFlags.DO_NOT_REAP_CHILD,
                None, -1, self.term1_fd)

        term2 = Vte.Terminal.new()
        term2.set_size(30, 3)
        term2.set_mouse_autohide(True)
        term2.set_scroll_on_output(True)
        term2_pty = term2.pty_new_sync(Vte.PtyFlags.DEFAULT, None)
        term2.set_pty(term2_pty)
        term2.set_word_char_exceptions(VTE_ADDITIONAL_WORDCHARS)
        term2_fd = Vte.Pty.get_fd(term2_pty)
        term2.spawn_async(
                Vte.PtyFlags.DEFAULT, #default is fine
                os.environ['HOME'], #where to start the command?
                ["/bin/bash"], #where is the emulator?
                [""], #it's ok to leave this list empty
                GLib.SpawnFlags.DO_NOT_REAP_CHILD,
                None, -1, term2_fd)

        scrollWin1 = Gtk.ScrolledWindow()
        scrollWin1.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        scrollWin1.set_border_width(1)
        Gtk.Container.add(scrollWin1, self.term1)
        self.notebook.append_page(scrollWin1, Gtk.Label(label="Terminal 1"))

        scrollWin2 = Gtk.ScrolledWindow()
        scrollWin2.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        scrollWin2.set_border_width(1)
        Gtk.Container.add(scrollWin2, term2)
        self.notebook.append_page(scrollWin2, Gtk.Label(label="Terminal 2"))

    def on_button1_clicked(self, event):
        self.term1.feed_child_binary(bytes("uptime\n",'utf8'))

win = Terminal()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()