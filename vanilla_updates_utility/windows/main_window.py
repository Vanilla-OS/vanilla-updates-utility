# main_window.py
#
# Copyright 2023 Mirko Brombin
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# SPDX-License-Identifier: GPL-3.0-or-later

import gettext
from gi.repository import Gtk, Adw
from typing import List

from vanilla_updates_utility.utils.wrapper import VsoSettingsWrapper

_ = gettext.gettext


@Gtk.Template(resource_path="/org/vanillaos/updates-utility/gtk/window-main.ui")
class UpdatesUtilityWindow(Adw.ApplicationWindow):
    __gtype_name__ = "UpdatesUtilityWindow"

    btn_cancel = Gtk.Template.Child()
    toasts = Gtk.Template.Child()
    str_frequencies = Gtk.Template.Child()
    switch_smart_updates = Gtk.Template.Child()
    row_frequency = Gtk.Template.Child()

    __vso_settings: VsoSettingsWrapper = None
    __frequency_values: List = [
        {"daily": _("Daily")},
        {"weekly": _("Weekly")},
        {"monthly": _("Monthly")},
    ]

    def __init__(self, embedded, **kwargs):
        super().__init__(**kwargs)

        self.__vso_settings = VsoSettingsWrapper()
        self.__build_ui()
        if embedded:
            self.__set_embedded()

    def __build_ui(self):
        config = self.__vso_settings.get_config()

        for frequency in self.__frequency_values:
            for k, v in frequency.items():
                self.str_frequencies.append(v)

        if config["updates.smart"] == "true":
            self.switch_smart_updates.set_active(True)

        match config["updates.schedule"]:
            case "daily":
                self.row_frequency.set_selected(0)
            case "weekly":
                self.row_frequency.set_selected(1)
            case "monthly":
                self.row_frequency.set_selected(2)
            case _:
                self.row_frequency.set_selected(0)

        self.btn_cancel.connect("clicked", self.__on_cancel_clicked)
        self.switch_smart_updates.connect("state-set", self.__on_smart_updates_toggled)
        self.row_frequency.connect("notify::selected", self.__on_frequency_changed)

    def __on_smart_updates_toggled(self, widget: Gtk.Switch, state: bool):
        self.__vso_settings.set_config_value_bool("updates.smart", state)
        self.toast(_("Smart updates enabled") if state else _("Smart updates disabled"))

    def __on_frequency_changed(self, widget, *args):
        index = widget.get_selected()
        key: str = None
        translated_value: str = None

        for k, v in self.__frequency_values[index].items():
            key = k
            translated_value = v

        self.__vso_settings.set_config_value("updates.schedule", key)
        self.toast(
            _("Frequency set to {translated_value}").format(
                translated_value=translated_value
            )
        )

    def __set_embedded(self):
        self.btn_cancel.show()
        self.set_deletable(False)

    def __on_cancel_clicked(self, widget):
        self.destroy()

    def toast(self, message, timeout=2):
        toast = Adw.Toast.new(message)
        toast.props.timeout = timeout
        self.toasts.add_toast(toast)
