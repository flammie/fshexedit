#!/usr/bin/env -O python3
"""First prototype for an dictionary extension workflow app."""

from sys import argv
import os.path

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import GLib, Gio, Gtk

ASCII = {b'\x00': "00", b'\x01': "01", b'\x02': "02", b'\x03': "03",
         b'\x04': "04",  b'\x05': "05", b'\x06': "06", b'\x07': "\\b",
         b'\x08': "08", b'\x09': "\\t", b'\x0A': "0A", b'\x0B': "0B",
         b'\x0C': "0C", b'\x0D': "0D", b'\x0E': "0E", b'\x0F': "0F",
         b'\x10': "10", b'\x11': "11", b'\x12': "12", b'\x13': "13",
         b'\x14': "14", b'\x15': "15", b'\x16': "16", b'\x17': "17",
         b'\x18': "18", b'\x19': "19", b'\x1A': "1A", b'\x1B': "1B",
         b'\x1C': "1C", b'\x1D': "1D", b'\x1E': "1E", b'\x1F': "1F",
         b'\x20': " ", b'\x21': "!", b'\x22': "\"", b'\x23': "#",
         b'\x24': "$", b'\x25': "%", b'\x26': "&", b'\x27': "'",
         b'\x28': "(", b'\x29': ")", b'\x2A': "*", b'\x2B': "+",
         b'\x2C': ",", b'\x2D': "-", b'\x2E': ".", b'\x2F': "/",
         b'\x30': "0", b'\x31': "1", b'\x32': "2", b'\x33': "3",
         b'\x34': "4", b'\x35': "5", b'\x36': "6", b'\x37': "7",
         b'\x38': "8", b'\x39': "9", b'\x3A': ":", b'\x3B': ";",
         b'\x3C': "<", b'\x3D': "=", b'\x3E': ">", b'\x3F': "?",
         b'\x40': "@", b'\x41': "A", b'\x42': "B", b'\x43': "C",
         b'\x44': "D", b'\x45': "E", b'\x46': "F", b'\x47': "G",
         b'\x48': "H", b'\x49': "I", b'\x4A': "J", b'\x4B': "K",
         b'\x4C': "L", b'\x4D': "M", b'\x4E': "N", b'\x4F': "O",
         b'\x50': "P", b'\x51': "Q", b'\x52': "R", b'\x53': "S",
         b'\x54': "T", b'\x55': "U", b'\x56': "V", b'\x57': "W",
         b'\x58': "X", b'\x59': "Y", b'\x5A': "Z", b'\x5B': "[",
         b'\x5C': "\\", b'\x5D': "]", b'\x5E': "^", b'\x5F': "_",
         b'\x60': "`", b'\x61': "a", b'\x62': "b", b'\x63': "c",
         b'\x64': "d", b'\x65': "e", b'\x66': "f", b'\x67': "g",
         b'\x68': "h", b'\x69': "i", b'\x6A': "j", b'\x6B': "k",
         b'\x6C': "l", b'\x6D': "m", b'\x6E': "n", b'\x6F': "o",
         b'\x70': "p", b'\x71': "q", b'\x72': "r", b'\x73': "s",
         b'\x74': "t", b'\x75': "u", b'\x76': "v", b'\x77': "w",
         b'\x78': "x", b'\x79': "y", b'\x7A': "z", b'\x7B': "{",
         b'\x7C': "|", b'\x7D': "}", b'\x7E': "~", b'\x7F': "7F",
         b'\x80': "80", b'\x81': "81", b'\x82': "82", b'\x83': "83",
         b'\x84': "84", b'\x85': "85", b'\x86': "86", b'\x87': "87",
         b'\x88': "88", b'\x89': "89", b'\x8A': "8A", b'\x8B': "8B",
         b'\x8C': "8C", b'\x8D': "8D", b'\x8E': "8E", b'\x8F': "8F",
         b'\x90': "90", b'\x91': "91", b'\x92': "92", b'\x93': "93",
         b'\x94': "94", b'\x95': "95", b'\x96': "96", b'\x97': "97",
         b'\x98': "98", b'\x99': "99", b'\x9A': "9A", b'\x9B': "9B",
         b'\x9C': "9C", b'\x9D': "9D", b'\x9E': "9E", b'\x9F': "9F",
         b'\xA0': "A0", b'\xA1': "A1", b'\xA2': "A2", b'\xA3': "A3",
         b'\xA4': "A4", b'\xA5': "A5", b'\xA6': "A6", b'\xA7': "A7",
         b'\xA8': "A8", b'\xA9': "A9", b'\xAA': "AA", b'\xAB': "AB",
         b'\xAC': "AC", b'\xAD': "AD", b'\xAE': "AE", b'\xAF': "AF",
         b'\xB0': "B0", b'\xB1': "B1", b'\xB2': "B2", b'\xB3': "B3",
         b'\xB4': "B4", b'\xB5': "B5", b'\xB6': "B6", b'\xB7': "B7",
         b'\xB8': "B8", b'\xB9': "B9", b'\xBA': "BA", b'\xBB': "BB",
         b'\xBC': "BC", b'\xBD': "BD", b'\xBE': "BE", b'\xBF': "BF",
         b'\xC0': "C0", b'\xC1': "C1", b'\xC2': "C2", b'\xC3': "C3",
         b'\xC4': "C4", b'\xC5': "C5", b'\xC6': "C6", b'\xC7': "C7",
         b'\xC8': "C8", b'\xC9': "C9", b'\xCA': "CA", b'\xCB': "CB",
         b'\xCC': "CC", b'\xCD': "CD", b'\xCE': "CE", b'\xCF': "CF",
         b'\xD0': "D0", b'\xD1': "D1", b'\xD2': "D2", b'\xD3': "D3",
         b'\xD4': "D4", b'\xD5': "D5", b'\xD6': "D6", b'\xD7': "D7",
         b'\xD8': "D8", b'\xD9': "D9", b'\xDA': "DA", b'\xDB': "DB",
         b'\xDC': "DC", b'\xDD': "DD", b'\xDE': "DE", b'\xDF': "DF",
         b'\xE0': "E0", b'\xE1': "E1", b'\xE2': "E2", b'\xE3': "E3",
         b'\xE4': "E4", b'\xE5': "E5", b'\xE6': "E6", b'\xE7': "E7",
         b'\xE8': "E8", b'\xE9': "E9", b'\xEA': "EA", b'\xEB': "EB",
         b'\xEC': "EC", b'\xED': "ED", b'\xEE': "EE", b'\xEF': "EF",
         b'\xF0': "F0", b'\xF1': "F1", b'\xF2': "F2", b'\xF3': "F3",
         b'\xF4': "F4", b'\xF5': "F5", b'\xF6': "F6", b'\xF7': "F7",
         b'\xF8': "F8", b'\xF9': "F9", b'\xFA': "FA", b'\xFB': "FB",
         b'\xFC': "FC", b'\xFD': "FD", b'\xFE': "FE", b'\xFF': "FF"
         }


def bytes2text(rawdata, table=ASCII):
    text = ''
    rawcopy = rawdata
    while rawcopy:
        # table in LRLM order
        found = False
        for b, s in table.items():
            if rawcopy.startswith(b):
                found = True
                text = text + table[b] + '\t'
                rawcopy = rawcopy.replace(b, b'', 1)
                break  # don't even bother break 2
        if not found:
            text = text + hex(rawcopy[0]) + '\t'
            rawcopy = rawcopy.replace(rawcopy[0], b'', 1)
    return text


def wrap(s):
    rv = ''
    blips = s.split('\t')
    for i, blip in enumerate(blips):
        rv += blip
        if i % 10:
            rv += ' '
        else:
            rv += '\n'
    return rv

class HexEditorWindow(Gtk.ApplicationWindow):
    """Main window of the app."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.header = Gtk.HeaderBar()
        self.header.set_show_close_button(True)
        self.header.props.title = "Flammie’s Hex Editor: (Untitled)"
        self.open = Gtk.Button()
        icon = Gio.ThemedIcon(name="document-open")
        image = Gtk.Image.new_from_gicon(icon, Gtk.IconSize.BUTTON)
        self.open.add(image)
        self.open.connect("clicked", self.on_open)
        self.header.pack_end(self.open)
        self.set_titlebar(self.header)
        self.box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        self.add(self.box)
        self.input_scroll = Gtk.ScrolledWindow()
        self.input_scroll.set_border_width(5)
        self.input_scroll.set_policy(Gtk.PolicyType.AUTOMATIC,
                                     Gtk.PolicyType.AUTOMATIC)
        self.hext = Gtk.TextView(overwrite=True)
        self.hext.set_monospace(True)
        self.input_scroll.add(self.hext)
        self.box.pack_start(self.input_scroll, True, True, 0)
        self.rawdata = bytes()
        self.hexbuffer = self.hext.get_buffer()
        self.output_scroll = Gtk.ScrolledWindow()
        self.output_scroll.set_border_width(5)
        self.output_scroll.set_policy(Gtk.PolicyType.AUTOMATIC,
                                      Gtk.PolicyType.AUTOMATIC)
        self.text = Gtk.TextView(overwrite=True)
        self.text.set_monospace(True)
        self.text.connect("move-cursor", self.on_textupdate)
        self.output_scroll.add(self.text)
        self.box.pack_start(self.output_scroll, True, True, 0)
        self.textbuffer = self.text.get_buffer()

    def on_open(self, button):
        dialog = Gtk.FileChooserDialog(title="Please choose a file",
                                       parent=self,
                                       action=Gtk.FileChooserAction.OPEN)
        dialog.add_buttons(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                           Gtk.STOCK_OK, Gtk.ResponseType.OK)

        dialog.set_current_folder(os.path.abspath('.'))
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            with open(dialog.get_filename(), 'rb') as binfile:
                self.rawdata = binfile.read()
                hexdata = '\t'.join([hex(c)[2:] for c in self.rawdata])
                textdata = bytes2text(self.rawdata)
                textdata = wrap(textdata)
                hexdata = wrap(hexdata)
                self.textbuffer.set_text(textdata)
                self.hexbuffer.set_text(hexdata)
                self.header.props.title = "Flammie’s Hex Editor: " +\
                    dialog.get_filename()
        elif response == Gtk.ResponseType.CANCEL:
            print("Cancel clicked")
        else:
            print("??? response", response)
        dialog.destroy()

    def on_textupdate(self, textview, step, count, extend):
        if self.textbuffer.get_has_selection():
            start, end = self.textbuffer.get_selection_bounds()
        else:
            start = self.textbuffer.get_iter_at_mark(
                    self.textbuffer.get_insert())
            end = start
            end.forward_cursor_position()
        startoff = start.get_offset()
        endoff = end.get_offset()
        hexstart = self.hexbuffer.get_iter_at_offset(startoff)
        hexend = self.hexbuffer.get_iter_at_offset(endoff)
        self.hexbuffer.select_range(hexstart, hexend)


class HexEditorApplication(Gtk.Application):
    """Application container stuff."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args,
                         application_id="com.flammie.github.hexeditor",
                         **kwargs)
        self.window = None

    def do_startup(self):
        Gtk.Application.do_startup(self)
        action = Gio.SimpleAction.new("about", None)
        action.connect("activate", self.on_about)
        self.add_action(action)
        action = Gio.SimpleAction.new("quit", None)
        action.connect("activate", self.on_quit)
        self.add_action(action)

    def do_activate(self):
        # We only allow a single window and raise any existing ones
        if not self.window:
            # Windows are associated with the application
            # when the last one is closed the application shuts down
            self.window = HexEditorWindow(application=self,
                                            title="HexEditor")
            self.window.show_all()
        self.window.present()

    def on_about(self, action, param):
        about_dialog = Gtk.AboutDialog(transient_for=self.window, modal=True)
        about_dialog.present()

    def on_quit(self, action, param):
        self.quit()


if __name__ == "__main__":
    app = HexEditorApplication()
    app.run(argv)
