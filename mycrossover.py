#!/usr/bin/python
import json
import os
import subprocess
import time
import shutil
from pathlib import Path

WINE_CREATE_BOTTLE = "/Applications/CrossOver.app/Contents/SharedSupport/CrossOver/bin/cxbottle"
WINE = "/Applications/CrossOver.app/Contents/SharedSupport/CrossOver/bin/wine"
WINE_TEM = "win10_64"

MYWINE = "./wine_bottle.json"
HOME = os.environ['HOME']
BOTTLE_PATH = os.path.join(HOME, "Library", "Application Support", "CrossOver", "Bottles")


class bottles:
    def __init__(self, bottle_json):
        self.bottle_scan = []
        self.scan()

    def scan(self):
        if not os.path.isdir(BOTTLE_PATH):
            os.makedirs(BOTTLE_PATH, exist_ok=True)
        dirs = os.listdir(BOTTLE_PATH)
        bottle_scan = []
        for b in dirs:
            if os.path.isdir(os.path.join(BOTTLE_PATH, b)):
                bottle_scan.append(b)
        self.bottle_scan = bottle_scan

    def remove(self, old_bottle):
        if old_bottle not in self.bottle_scan:
            raise ValueError("Bottle not exist.")
        # os.rmdir(os.path.join(BOTTLE_PATH, old_bottle))
        shutil.rmtree(os.path.join(BOTTLE_PATH, old_bottle))
        print("Remove: {}".format(os.path.join(BOTTLE_PATH, old_bottle)))
        self.scan()

    def bottle_list(self):
        self.scan()
        return self.bottle_scan


def run_create_bottle(bottle_name):
    print("Create bottle: {}".format(bottle_name))
    os.makedirs(BOTTLE_PATH, exist_ok=True)
    print("\n$ {} --bottle {} --create --template {} --install".format(WINE_CREATE_BOTTLE, bottle_name, WINE_TEM))
    proc = subprocess.Popen(
        "{} --bottle {} --create --template {} --install".format(WINE_CREATE_BOTTLE, bottle_name, WINE_TEM), shell=True,
        stdout=subprocess.PIPE)
    proc.wait()
    print("Bottle create at : {}".format(os.path.join(BOTTLE_PATH, bottle_name)))


def run_bottle_cfg(bottle_name):
    print("\n$ {} --bottle {} winecfg".format(WINE, bottle_name))
    proc = subprocess.Popen(
        "{} --bottle {} winecfg".format(WINE, bottle_name),
        shell=True,
        stdout=subprocess.PIPE)
    proc.wait()


def run_bottle_reg(bottle_name, regedit_file=None):

    if regedit_file is None:
        print("\n$ {} --bottle {} regedit".format(WINE, bottle_name))
        proc = subprocess.Popen(
            "{} --bottle {} regedit".format(WINE, bottle_name),
            shell=True,
            stdout=subprocess.PIPE)
    else:
        print("\n$ {} --bottle {} regedit {}".format(WINE, bottle_name, regedit_file))
        proc = subprocess.Popen(
            "{} --bottle {} regedit {}".format(WINE, bottle_name, regedit_file),
            shell=True,
            stdout=subprocess.PIPE)
    proc.wait()


def run_install_exe(bottle_name, install_file):
    print("\n$ {} --bottle {} --wait-children --no-convert --new-console {}".format(WINE, bottle_name, install_file))
    proc = subprocess.Popen(
        "{} --bottle {} --wait-children --no-convert --new-console {}".format(WINE, bottle_name, install_file),
        shell=True,
        stdout=subprocess.PIPE)
    proc.wait()


def run_install_msi(bottle_name, install_file):
    print("\n$ {} --bottle {} --wait-children --no-convert --new-console msiexec.exe /i {}".format(WINE, bottle_name,
                                                                                                   install_file))
    proc = subprocess.Popen(
        "{} --bottle {} --wait-children --no-convert --new-console msiexec.exe /i {}".format(WINE, bottle_name,
                                                                                             install_file),
        shell=True,
        stdout=subprocess.PIPE)
    proc.wait()


def run_executor(bottle_name, exec_exe):
    print("\n$ {} --bottle {}  {}".format(WINE, bottle_name, exec_exe))
    proc = subprocess.Popen(
        "{} --bottle {}  {}".format(WINE, bottle_name, exec_exe),
        shell=True,
        stdout=subprocess.PIPE)
    proc.wait()


def run_create_app(bottle_name, app_name, exec_exe, icon_path):
    print("\n$ bash create_app.sh {} {} \"{}\" {}".format(bottle_name, app_name, exec_exe, icon_path))
    # bash create_app.sh bottle_name app_name exe_path icon_path
    proc = subprocess.Popen(
        "bash create_app.sh {} {} \"{}\" {}".format(bottle_name, app_name, exec_exe, icon_path),
        shell=True,
        stdout=subprocess.PIPE)
    proc.wait()


class exe_scanner:
    def __init__(self, this_bottle):
        self.this_bottle = this_bottle
        if not os.path.isfile(os.path.join(BOTTLE_PATH, this_bottle, "exe_result.json")):
            with open(os.path.join(BOTTLE_PATH, this_bottle, "exe_result.json"), "w") as fd:
                json.dump({"EXE": []}, fd, indent=4)
            print("Create: {}".format(os.path.join(BOTTLE_PATH, this_bottle, "exe_result.json")))
            time.sleep(0.5)
        with open(os.path.join(BOTTLE_PATH, this_bottle, "exe_result.json")) as jsonFile:
            result_json = json.load(jsonFile)
            jsonFile.close()
        self.exist_record_exe = result_json["EXE"]
        self.exist_exe = self.exe_scan()

    def exe_scan(self):
        exe_collect = []
        # print(os.path.join(BOTTLE_PATH, self.this_bottle)+"/")
        for dirPath, dirNames, fileNames in os.walk(os.path.join(BOTTLE_PATH, self.this_bottle) + "/"):
            for f in fileNames:
                if ".exe" in os.path.join(dirPath, f):
                    exe_collect.append(os.path.join(dirPath, f))
        # print(exe_collect)
        return exe_collect

    def exe_collection(self):
        exe_collect = []
        print(os.path.join(BOTTLE_PATH, self.this_bottle) + "/")
        for dirPath, dirNames, fileNames in os.walk(os.path.join(BOTTLE_PATH, self.this_bottle) + "/"):
            for f in fileNames:
                if ".exe" in os.path.join(dirPath, f):
                    exe_collect.append(os.path.join(dirPath, f))
        install_exe = list(set(exe_collect) - set(self.exist_exe) - set(self.exist_record_exe))
        self.exist_record_exe += install_exe
        with open(os.path.join(BOTTLE_PATH, self.this_bottle, "exe_result.json"), "w") as fd:
            json.dump({"EXE": self.exist_record_exe}, fd, indent=4)
        return install_exe


if __name__ == "__main__":
    bottle = bottles(MYWINE)
    print("Welcome to mywine")

    # select startype
    startype = ["Create bottle", "Remove bottle", "Wine setting", "Install", "Exec", "Create macos app", "Exit"]
    for i, v in enumerate(startype):
        print("({}) {}".format(i, v))
    selected_type = input("? ")

    if int(selected_type) not in list(range(len(startype))):
        raise ValueError("ERROR input value.")

    if selected_type == "0":
        bot_name = input("Bottle name: ")
        run_create_bottle(bot_name)

    elif selected_type == "1":
        exist_bot = bottle.bottle_list()
        print("\nRemove bottle.")
        for i, v in enumerate(exist_bot):
            print("({}) {}".format(i, v))
        selected_bottle = input("? ")
        if int(selected_bottle) not in list(range(len(exist_bot))):
            raise ValueError("ERROR input value.")
        bottle.remove(exist_bot[int(selected_bottle)])

    elif selected_type == "2":

        exist_bot = bottle.bottle_list()
        print("\nOpen bottle cfg.")
        for i, v in enumerate(exist_bot):
            print("({}) {}".format(i, v))
        selected_bottle = input("? ")
        if int(selected_bottle) not in list(range(len(exist_bot))):
            raise ValueError("ERROR input value.")

        setting = ["cfg", "regedit"]
        for i, v in enumerate(setting):
            print("({}) {}".format(i, v))
        selected_setting = input("? ")

        if selected_setting == "0":
            run_bottle_cfg(exist_bot[int(selected_bottle)])
        if selected_setting == "1":
            installation_file = input("\nregedit file (empty to open register): ")
            if installation_file == "":
                run_bottle_reg(exist_bot[int(selected_bottle)])
            else:
                run_bottle_reg(exist_bot[int(selected_bottle)], installation_file)
    elif selected_type == "3":
        exist_bot = bottle.bottle_list()
        print("\nSelect bottle to install.")
        for i, v in enumerate(exist_bot):
            print("({}) {}".format(i, v))
        selected_bottle = input("? ")
        if int(selected_bottle) not in list(range(len(exist_bot))):
            raise ValueError("ERROR input value.")

        installation_file = input("\ninstallation file or folder: ")
        if installation_file[-1] == " ":
            installation_file = installation_file[:-1]

        escaner = exe_scanner(this_bottle=exist_bot[int(selected_bottle)])
        if os.path.isdir(installation_file):
            print("Move {} to {}".format(installation_file, os.path.join(BOTTLE_PATH, exist_bot[int(selected_bottle)], "drive_c", "Program Files", installation_file.split("/")[-1])))
            shutil.copytree(installation_file, os.path.join(BOTTLE_PATH, exist_bot[int(selected_bottle)], "drive_c", "Program Files", installation_file.split("/")[-1]))
        else:
            if "msi" in installation_file:
                run_install_msi(exist_bot[int(selected_bottle)], installation_file)
            else:
                run_install_exe(exist_bot[int(selected_bottle)], installation_file)
        escaner.exe_collection()
        print(escaner.exist_record_exe)

        print("\nSelect exe to run.")
        for i, v in enumerate(escaner.exist_record_exe):
            print("({}) {}".format(i, v))
        selected_exe = input("? ")
        run_path = escaner.exist_record_exe[int(selected_exe)]
        run_executor(exist_bot[int(selected_bottle)], run_path)
    elif selected_type == "4":
        exist_bot = bottle.bottle_list()
        print("\nSelect bottle bottle.")
        for i, v in enumerate(exist_bot):
            print("({}) {}".format(i, v))
        selected_bottle = input("? ")
        cmd = input("command: ")
        run_executor(exist_bot[int(selected_bottle)], cmd)

    elif selected_type == "5":
        exist_bot = bottle.bottle_list()
        print("\nSelect bottle to create macos app.")
        for i, v in enumerate(exist_bot):
            print("({}) {}".format(i, v))
        selected_bottle = input("? ")
        if int(selected_bottle) not in list(range(len(exist_bot))):
            raise ValueError("ERROR input value.")

        escaner = exe_scanner(this_bottle=exist_bot[int(selected_bottle)])
        print("\nSelect exe to run.")
        for i, v in enumerate(escaner.exist_record_exe):
            print("({}) {}".format(i, v))
        selected_exe = input("? ")
        if selected_exe == "":
            run_path = ""
        else:
            run_path = escaner.exist_record_exe[int(selected_exe)]

        app_name = input("\nApp name: ")
        icon_path = input("\nIcon path (app.ico): ")
        run_create_app(bottle_name=exist_bot[int(selected_bottle)],
                       app_name=app_name,
                       exec_exe=run_path,
                       icon_path=icon_path)

        # shutil.move(os.path.join("./", "{}.app".format(app_name)), "/Applications")
        # run_executor(exist_bot[int(selected_exe)], run_path)

    # print("Start ", startype[int(selected_type)])

    # print("Nice to meet you, " + yourName)
    # os.system('ls -l')
