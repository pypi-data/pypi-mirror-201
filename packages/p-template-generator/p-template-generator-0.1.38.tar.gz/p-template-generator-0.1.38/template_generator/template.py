import sys
import os
import subprocess
import json
import random
from pathlib import Path
import shutil
import zipfile
import stat
from template_generator import binary

def getBinary(searchPath):
    binaryPath = ""
    if sys.platform == "win32":
        binaryPath = os.path.join(os.path.join(binary.skymediaPath(searchPath), "win"), "TemplateProcess.exe")
    elif sys.platform == "linux":
        binaryPath = os.path.join(binary.skymediaPath(searchPath), "TemplateProcess.out")
        if os.path.exists(binary):
            cmd = subprocess.Popen(f"chmod 755 {binary}", stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
            while cmd.poll() is None:
                print(cmd.stdout.readline().rstrip().decode('utf-8'))
        #check env
        if os.path.exists("/usr/lib/libskycore.so") == False:
            setupShell = os.path.join(binary.skymediaPath(searchPath), "setup.sh")
            if os.path.join(setupShell):
                print(f"=================== begin Initialize environment : sh {setupShell} ==================")
                try:
                    cmd = subprocess.Popen(f"sh {setupShell}", stdout=subprocess.PIPE,
                                            stderr=subprocess.PIPE, shell=True)
                    while cmd.poll() is None:
                        print(cmd.stdout.readline().rstrip().decode('utf-8'))
                except subprocess.CalledProcessError as e:
                    raise e
                print("===================             end              ==================")
            if os.path.exists("/usr/lib/libskycore.so") == False:
                raise Exception("linux environment error")
    if os.path.exists(binaryPath):
        return binaryPath
    return ""

def executeTemplate(inputFiles, template_path, params, output_path, searchPath):        
    binaryPath = getBinary(searchPath)
    if len(binaryPath) <= 0:
        raise Exception("binary not found")

    inputArgs = os.path.join(os.path.dirname(os.path.abspath(__file__)), f"{random.randint(100,99999999)}.in")
    if os.path.exists(inputArgs):
        os.remove(inputArgs)
    with open(inputArgs, 'w') as f:
        json.dump({
            "input": inputFiles,
            "template": template_path,
            "params": params,
            "output": output_path
        }, f)

    extArgs = ""
    #--adaptiveSize
    templateName = os.path.basename(template_path)
    if "template_" in templateName or templateName == "AIGC_1":
        extArgs += "--adaptiveSize true "
    #--fontDir
    fontPath = binary.fontPath()
    if os.path.exists(fontPath):
        extArgs += f"--fontDir {fontPath} "
    #--subEffectDir
    subPath = binary.subEffectPath()
    if os.path.exists(subPath):
        extArgs += f"--subEffectDir {subPath} "

    command = f'{binaryPath} --config {inputArgs} {extArgs}'
    print(f"=== executeTemplate => {command}")
    cmd = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    while cmd.poll() is None:
        print(cmd.stdout.readline().rstrip().decode('utf-8'))
    if os.path.exists(output_path) == False:
        raise Exception("output file not found")