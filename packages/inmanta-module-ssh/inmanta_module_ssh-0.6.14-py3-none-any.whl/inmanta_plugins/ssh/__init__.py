"""
    Copyright 2020 Inmanta

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.

    Contact: code@inmanta.com
"""
import os
import subprocess

from inmanta.plugins import Context, plugin


def get_or_create_key(storage, name):
    priv_key = os.path.join(storage, name)
    pub_key = os.path.join(storage, name + ".pub")
    if not os.path.exists(priv_key):
        subprocess.check_output(
            [
                "ssh-keygen",
                "-t",
                "rsa",
                "-b",
                "4096",
                "-N",
                "",
                "-C",
                name,
                "-f",
                priv_key,
            ]
        )

    with open(priv_key, "r") as fd:
        priv = fd.read()

    with open(pub_key, "r") as fd:
        pub = fd.read()

    return priv, pub


@plugin
def get_private_key(context: Context, name: "string") -> "string":
    """
    Create or return if it already exists a key with the given name. The
    private key is returned.
    """
    priv, pub = get_or_create_key(context.get_data_dir(), name)
    return priv


@plugin
def get_public_key(context: Context, name: "string") -> "string":
    """
    See get_private_key
    """
    priv, pub = get_or_create_key(context.get_data_dir(), name)
    return pub


@plugin
def get_putty_key(context: Context, name: "string") -> "string":
    priv_key = os.path.join(context.get_data_dir(), name)
    if not os.path.exists(priv_key):
        get_private_key(context, name)

    ppk_key = priv_key + ".ppk"
    subprocess.check_output(["puttygen", priv_key, "-o", ppk_key])

    with open(ppk_key, "r") as fd:
        return fd.read()
