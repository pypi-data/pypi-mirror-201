import os
import sys
import argparse
import json
from pathlib import Path
import subprocess
import urllib3

from template_generator import template
from template_generator import template_test
from template_generator import ffmpeg

parser = argparse.ArgumentParser()
parser.add_argument("--test", type=str, default=None, help="测试")
parser.add_argument("--transcoding", type=str, default=None, help="转码")
parser.add_argument("--input", type=str, default=None, help="输入资源")

def testTemplate():
    searchPath = ""
    if len(sys.argv) > 4 and sys.argv[3] == "--i":
        searchPath = sys.argv[4]

    template_test.test(searchPath)
    
def configTemplate():
    input = sys.argv[2]

    inputFiles = []
    template_path = None
    params = {}
    output_path = None
    searchPath = ""
    try:
        if os.path.isfile(input):
            with open(input, 'r') as f:
                data = json.load(f)
        inputFiles = data["input"]
        template_path = data["template"]
        params = data["params"]
        output_path = data["output"]
        if len(sys.argv) > 4 and sys.argv[3] == "--i":
            searchPath = sys.argv[4]
    except:
        inputFiles = [sys.argv[2]]
        template_path = sys.argv[3]
        params = json.loads(sys.argv[4])
        output_path = sys.argv[5]
        if len(sys.argv) > 7 and sys.argv[6] == "--i":
            searchPath = sys.argv[7]

    if inputFiles == None or len(inputFiles) == 0 or template_path == None or output_path == None:
        raise Exception("args fail!")
    for it in inputFiles:
        if os.path.exists(it) == False:
            raise Exception(f"file {it} not found!")
    if os.path.exists(template_path) == False:
        raise Exception(f"template {template_path} not found!")
    template.executeTemplate(inputFiles, template_path, params, output_path, searchPath)
    
def transcoding():
    file = sys.argv[2]
    if os.path.exists(file) == False:
        raise Exception("transcoding file not exist")
    
    searchPath = ""
    if len(sys.argv) > 4 and sys.argv[3] == "--i":
        searchPath = sys.argv[4]

    w,h,bitrate,fps = ffmpeg.videoInfo(file)
    if w <= 0 or h <= 0 or bitrate <= 0 or fps <= 0:
        raise Exception("file is not video")

    niceBitrate = min(bitrate, (w * h) * (fps / 30.0) / (540.0 * 960.0 / 4000))

    tmpPath = f"{file}.mp4"
    args_moov = "-movflags faststart"
    args_h264 = "-c:v libx264 -pix_fmt yuv420p"
    args_bitrate = f"-b:v {niceBitrate}k -bufsize {niceBitrate}k"
    command = f'-i {file} {args_moov} {args_h264} {args_bitrate} -y {tmpPath}'
    if ffmpeg.process(command, searchPath):
        os.remove(file)
        os.rename(tmpPath, file)

def doFfmpeg():
    cmd = sys.argv[2]
    if len(cmd) <= 0:
        raise Exception("please set command")
    
    searchPath = ""
    if len(sys.argv) > 4 and sys.argv[3] == "--i":
        searchPath = sys.argv[4]

    if ffmpeg.process(cmd, searchPath):
        print("=== success")
    else:
        print("=== fail")

module_func = {
    "--test": testTemplate,
    "--input": configTemplate,
    "--transcoding": transcoding,
    "--ffmpeg": doFfmpeg
}

def main():
    if len(sys.argv) < 2:
        return
    urllib3.disable_warnings()
    # try:
    module = sys.argv[1]
    if module in module_func:
        module_func[module]()
        sys.exit(0)
    else:
        print("Unknown command:", module)
        sys.exit(-1)
    # except Exception as e:
    #     print(f"uncatch Exception:{e}")
    #     sys.exit(-1)
        
if __name__ == '__main__':
        main()
