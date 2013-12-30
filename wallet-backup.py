#!/usr/bin/python
"""
Install gpg first for windows:
http://files.gpg4win.org/gpg4win-vanilla-2.2.1.exe
"""
from __future__ import unicode_literals, absolute_import, print_function
from genericpath import isfile
from os import listdir, environ, access, X_OK
from os.path import expanduser, join, exists, split, pathsep
from zipfile import ZipFile
from subprocess import call


PASSWORD = "test"
ENCRYPT = True


def find_wallets(base_dir):
    for directory in listdir(base_dir):
        dir_path = join(base_dir, directory)
        wallet_path = join(dir_path, "wallet.dat")
        if exists(wallet_path):
            wallet_data = open(wallet_path, 'rb').read()
            yield directory, wallet_data


def which(program):

    def is_exe(file_path):
        return isfile(file_path) and access(file_path, X_OK)

    file_path, file_name = split(program)
    if file_path:
        if is_exe(program):
            return program
    else:
        for path in environ["PATH"].split(pathsep):
            path = path.strip('"')
            exe_file = join(path, program)
            if is_exe(exe_file):
                return exe_file

    return None


def encrypt(passphrase=PASSWORD, filename="backup.zip.gpg"):
    executable = which("gpg.exe")
    cmd = [
        executable, "--output", filename, "--passphrase",
        passphrase, "--batch", "--symmetric", "backup.zip"
    ]
    call(cmd, shell=True)


if __name__ == "__main__":
    zf = ZipFile("backup.zip", "w")
    for name, wallet in find_wallets(join(expanduser("~"), "AppData", "Roaming", )):
        print("Writing: {}".format(name))
        zf.writestr(join(name, "wallet.dat"), wallet)
    zf.close()
    if ENCRYPT:
        encrypt(PASSWORD)