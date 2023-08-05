import zipfile
import platform
import subprocess
import json
import os
from pathlib import Path
import shutil
import stat
import requests
import hashlib

def getOssResource(rootDir, url, md5, name):
    localFile = os.path.join(rootDir, name)
    localFileIsRemote = False
    if os.path.exists(localFile):
        with open(localFile, 'rb') as fp:
                file_data = fp.read()
        file_md5 = hashlib.md5(file_data).hexdigest()
        if file_md5 == md5:
            localFileIsRemote = True

    if localFileIsRemote == False: #download
        if os.path.exists(localFile):
            os.remove(localFile)
        s = requests.session()
        s.keep_alive = False
        file = s.get(url, verify=False)
        with open(localFile, "wb") as c:
            c.write(file.content)
        s.close()
        
def updateNewTempalte(rootDir):
    getOssResource(rootDir, "http://mecord-m.2tianxin.com/res/template-res_20230404.zip", "92a3a8c2ab4b03bcfebe909ff086cc7d", "template_res.zip.py")
    for root,dirs,files in os.walk(rootDir):
        for dir in dirs:
            shutil.rmtree(os.path.join(root, dir))

    for root,dirs,files in os.walk(rootDir):
        for file in files:
            name = file[0:file.index(".")]
            ext = file[file.index("."):]
            if ext == ".zip.py" and os.path.exists(os.path.join(root, name)) == False:
                with zipfile.ZipFile(os.path.join(root, file), "r") as zipf:
                    zipf.extractall(os.path.join(root, name))
                return
        if root != files:
            break
        
def templateDir(rootDir):
    for root,dirs,files in os.walk(rootDir):
        for dir in dirs:
            return os.path.join(root, dir)
        if root != files:
            break
    return ""

def savePut(src, dst, name):
    if name in src:
        dst[name] = src[name]

def saveGet(src, name):
    if name in src:
        return src[name]
    return ""

def saveGetI(src, name):
    if name in src:
        return src[name]
    return -1

def inputConfig(data):
    videoCount = 0
    imageCount = 0
    audioCount = 0
    textCount = 0
    list = []
    otherParam = []
    for it in data:
        try:
            if it["type"].lower() == "image":
                imageCount += 1
                list.append({
                    "type": "image",
                    "width": saveGetI(it, "width"),
                    "height": saveGetI(it, "height")
                })
            elif it["type"].lower() == "video":
                videoCount += 1
                list.append({
                    "type": "video",
                    "width": saveGetI(it, "width"),
                    "height": saveGetI(it, "height"),
                    "name": saveGet(it, "name"),
                    "group": saveGet(it, "group")
                })
            elif it["type"].lower() == "audio":
                audioCount += 1
                list.append({
                    "type": "audio",
                    "name": saveGet(it, "name"),
                    "group": saveGet(it, "group")
                })
            elif it["type"].lower() == "text":
                textCount += 1
                list.append({
                    "type": "text",
                    "value": it["value"],
                    "name": saveGet(it, "name"),
                    "group": saveGet(it, "group")
                })
            else:
                dd = {
                    "type": it["type"],
                    "name": saveGet(it, "name"),
                    "group": saveGet(it, "group")
                    }
                savePut(it, dd, "minValue")
                savePut(it, dd, "maxValue")
                if "paramSettingInfo" in it:
                    filterIndex = it["paramSettingInfo"][0]["filterIndex"]
                    paramName = it["paramSettingInfo"][0]["paramName"]
                    objName = it["paramSettingInfo"][0]["paramName"]
                    valueType = it["paramSettingInfo"][0]["valueType"]
                    dd["paramKey"] = f"{filterIndex}:{paramName}"
                    dd["obj"] = objName
                    dd["valueType"] = valueType
                otherParam.append(dd)
        except Exception as e:
            list = []
    return {
        "videoCount":videoCount,
        "imageCount":imageCount,
        "audioCount":audioCount,
        "textCount":textCount,
        "list":list,
        "otherParams":list
    }

def listTemplate(searchPath):
    tpDir = ""
    if len(searchPath) <= 0 or os.path.exists(searchPath) == False:
        rootDir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "res")
        updateNewTempalte(rootDir)
        tpDir = templateDir(rootDir)
    else:
        tpDir = searchPath
    if len(tpDir) <= 0 or os.path.exists(tpDir) == False:
        print("template resource not found")
        return
    result = []
    for root,dirs,files in os.walk(tpDir):
        for dir in dirs:
            projFile = os.path.join(root, dir, "template.proj")
            if os.path.exists(projFile) == False:
                for root,dirs,files in os.walk(os.path.join(root, dir)):
                    for file in files:
                        name, ext = os.path.splitext(file)
                        if ext == ".proj":
                            projFile = os.path.join(root, file)
            with open(projFile, 'r', encoding='utf-8') as f:
                projConfig = json.load(f)
            inputListPath = os.path.join(root, dir, "inputList.conf")
            if "inputList" in projConfig:
                inputListPath = os.path.join(root, dir, projConfig["inputList"])
            if "type" not in projConfig:
                continue
            if os.path.exists(inputListPath) == False:
                continue
            inputList = []
            with open(inputListPath, 'r', encoding='utf-8') as f:
                inputList = json.load(f)
            data = inputConfig(inputList)
            data["name"] = dir
            data["path"] = os.path.join(root, dir)
            result.append(data)
        if root != files:
            break
    print(json.dumps(result))
    return
