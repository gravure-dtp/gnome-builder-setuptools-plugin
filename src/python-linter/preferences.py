# -*- coding: utf-8 -*-
#
#       Copyright (c) Gilles Coissac 2022 <info@gillescoissac.fr>
#
#       This program is free software; you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation; either version 3 of the License, or
#       (at your option) any later version.
#
#       This program is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
#
#       You should have received a copy of the GNU General Public License
#       along with this program; if not, write to the Free Software
#       Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#       MA 02110-1301, USA.
#
# pylint: disable=too-many-arguments, attribute-defined-outside-init
#
import pylint
import gi

from gi.repository import GObject, Ide

from preferences_entry import PreferencesEntry


_ = Ide.gettext

# FIXME: meson.build:glib-compile-schemas need
#        to handle flatpack install


class PythonLinterPreferencesAddin(GObject.Object, Ide.PreferencesAddin):
    """PythonLinterPreferencesAddin."""

    def do_load(self, prefs):
        """
        This interface method is called when a preferences addin is initialized.
        It could be initialized from multiple preferences implementations,
        so consumers should use the #DzlPreferences interface to add their
        preferences controls to the container.
        Such implementations might include a preferences dialog window,
        or a preferences widget which could be rendered as a perspective.
        """
        self.enable_linter = prefs.add_switch(
            # to the code-insight page
            "code-insight",
            # in the diagnostics group
            "diagnostics",
            # mapping to the gsettings schema
            "org.gnome.builder.plugins.python-linter",
            # with the gsettings schema key
            "enable-python-linter",
            # And the gsettings path
            None,
            # The target GVariant value if necessary (usually not)
            "false",
            # title
            "Python Linter",
            # subtitle
            _("Enable the use of PyLint, which may execute code in your project"),
            # these are keywords used to search for preferences
            _("pylint python lint code execute execution"),
            # with sort priority
            500)

        prefs.add_group(
            "code-insight", "python-linter",
            f"Python Linter : (pylint-{pylint.version})", 3000
        )

        self.ext_mod = prefs.add_custom(
            "code-insight",
            "python-linter",
            PreferencesEntry(
                "org.gnome.builder.plugins.python-linter",
                "ext-modules",
                None,
                "extension modules",
                _("A comma-separated list of package or module names from where"
                  " C extensions may be loaded. Extensions are loading into the"
                  " active Python interpreter and may run arbitrary code."),
                0,
            ),
            _("pylint python lint"),
            10
        )


    def do_unload(self, preferences):
        """This interface method is called when the preferences addin
        should remove all controls added to preferences. This could
        happen during desctruction of preferences, or when the plugin
        is unloaded.preferences.remove_id(self.python_linter_id)
        """
        preferences.remove_id(self.enable_linter)
        #preferences.remove_id(self.ext_mod)
