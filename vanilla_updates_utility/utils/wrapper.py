# wrapper.py
#
# Copyright 2024 Mirko Brombin
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

import os
import shutil
import logging
import subprocess
from typing import Text, List
import gettext

_ = gettext.gettext
logger = logging.getLogger("UpdatesUtility:Wrapper")


class VsoSettingsWrapper:
    @staticmethod
    def get_vso_cmd(command: Text, use_pkexec: bool = False) -> Text:
        vso_bin: Text = "vso"
        use_host_spawn: bool = False

        if os.path.exists("/run/.containerenv"):
            use_host_spawn = True

        if os.path.exists(f"{os.getcwd()}/vso"):
            vso_bin = f"{os.getcwd()}/vso"

        if vso_bin is None:
            raise FileNotFoundError("vso binary not found")

        final_command: List[Text] = []
        if use_host_spawn:
            host_spawn_path = shutil.which("host-spawn")
            assert host_spawn_path
            final_command.append(host_spawn_path)
        if use_pkexec:
            final_command.append("pkexec")
        final_command.append(vso_bin)
        final_command.append(command)

        return " ".join(final_command)

    @staticmethod
    def get_config() -> dict:
        config = {}

        try:
            output = subprocess.check_output(
                VsoSettingsWrapper.get_vso_cmd("config show", False),
                stderr=subprocess.STDOUT,
                shell=True,
            ).decode("utf-8")
            for line in output.split("\n"):
                line = " ".join(line.split())
                if line and ":" in line:
                    key, value = line.split(" : ")
                    config[key] = value
        except subprocess.CalledProcessError as e:
            logger.error(e)
            exit(1)

        return config

    @staticmethod
    def set_config_value(key: Text, value: str) -> None:
        try:
            subprocess.check_output(
                VsoSettingsWrapper.get_vso_cmd(f"config set -k {key} -v {value}", True),
                stderr=subprocess.STDOUT,
                shell=True,
            ).decode("utf-8")
            logger.debug(f"Set {key} to {value}")
        except subprocess.CalledProcessError as e:
            logger.error(e.output)

    @staticmethod
    def set_config_value_bool(key: Text, value: bool) -> None:
        try:
            subprocess.check_output(
                VsoSettingsWrapper.get_vso_cmd(
                    f"config set -k {key} -v {'true' if value else 'false'}", True
                ),
                stderr=subprocess.STDOUT,
                shell=True,
            ).decode("utf-8")
            logger.debug(f"Set {key} to {value}")
        except subprocess.CalledProcessError as e:
            logger.error(e.output)
