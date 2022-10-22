#!/usr/bin/env python3
import os

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

gi.require_version('Vte', '2.91')  # vte-0.38 (gnome-3.4)
from gi.repository import Vte, GLib, GObject

#model view controller(model, view)

class CustomTerminal():
    def __init__(self) -> None:
        VTE_ADDITIONAL_WORDCHARS = "-,./?%&#:_";

        self.term = Vte.Terminal.new()
        self.term.set_size(30, 3)
        self.term.set_mouse_autohide(True)
        self.term.set_scroll_on_output(True)
        self.term.set_audible_bell(True)
        term_pty = self.term.pty_new_sync(Vte.PtyFlags.DEFAULT, None)
        self.term.set_pty(term_pty)
        self.term.set_word_char_exceptions(VTE_ADDITIONAL_WORDCHARS)
        term_fd = Vte.Pty.get_fd(term_pty)
        self.term.spawn_async(
                Vte.PtyFlags.DEFAULT, #default is fine
                os.environ['HOME'], #where to start the command?
                ["/bin/bash"], #where is the emulator?
                [""], #it's ok to leave this list empty
                GLib.SpawnFlags.DO_NOT_REAP_CHILD,
                None, -1, term_fd)

class Handlers():
    def __init__(self, controller) -> None:
        super().__init__()
        self.controller = controller;

    def on_window_main_destroy(self, *args):
        Gtk.main_quit()

    def on_button_woskpace_clicked(self, event):
        pass
        #terminal = self.controller.get_active_terminal()
        #terminal.feed_child_binary(bytes("uptime\n",'utf8'))

class Controller():
    def __init__(self, model, view) -> None:
        self._model = model
        self._view = view
        
        #init first two notebook pages
        notebook = self.get_object("notebook_terminals")
        self.add_terminal(notebook.get_nth_page(0))
        self.add_terminal(notebook.get_nth_page(1))
        
        #pass handlers
        handlers = Handlers(self)
        self._view.builder.connect_signals(handlers)
        self._view.window.show_all()

    def get_object(self, name) -> Gtk.Widget:
        widget = self._view.builder.get_object(name)
        return widget

    def get_active_terminal(self):
        notebook = self.get_object("notebook_terminals")
        page = notebook.get_active_page()
        return page

    def add_terminal(self, page = None):
        term = self._model.add_terminal_model()
        if page is None:
            page = self._view.add_terminal_page()
        Gtk.Container.add(page, term)

class Model():
    def __init__(self) -> None:
        self.terminals = []

    def add_terminal_model(self):
        t = CustomTerminal()
        self.terminals.append(t)

        return t.term

class View():
    def __init__(self) -> None:
        self.builder = Gtk.Builder()                             #GTK init
        self.builder.add_from_file("frost_gui.glade")
        
        self.window = self.builder.get_object("window_main")

    def add_terminal_page(self):
        notebook = self.builder.get_object("notebook_terminals")
        
        new_page_scrolled = Gtk.ScrolledWindow()
        page_number = notebook.get_n_pages()+1
        label = Gtk.Label(f"term{page_number}")

        notebook.append_page(new_page_scrolled, label)
        return notebook.get_nth_page(page_number)

#class WindowMain(Gtk.Window): #View
#    def __init__(self):
#        Gtk.Window.__init__(self, title="FROST == FAST ROS TOOL")        
#       
#        window.set_default_size(800,600)

if __name__ == "__main__":
    model = Model()
    view = View()
    controller = Controller(model, view)

    Gtk.main()