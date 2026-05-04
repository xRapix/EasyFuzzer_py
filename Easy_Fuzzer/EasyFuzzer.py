import requests
import threading
from pathlib import Path


def debug(int):
    return f"!---Error {int}---!"



#Deafult settings
Threads = 5

OrginialUrl = input("URL >>> ")
WordlistPath = input("WORDLIST >>> ")
IgnoreCodes = input("IGNORE CODES (optional) >>> ")
Headers = input("USER-AGENT(deafult: curl/7.68.0) >>> ")

if Headers == "":
    Headers = {'User-Agent': 'curl/7.68.0'}  
    

WordlistPath = Path(__file__).resolve().parent / WordlistPath

if not OrginialUrl.startswith("https://") and not OrginialUrl.startswith("http://"): 
    try:
        OrginialUrl = "https://" + OrginialUrl
    except requests.exceptions.MissingSchema:
        print("Try adding 'http' before the url!")
        debug(99)

print(f"URL: {OrginialUrl}")

IgnoreCodes=IgnoreCodes.replace(" ","")
IgnoreCodes=IgnoreCodes.replace(",","")
ign_codes = []
not_finished_code = ""

#Ignore Codes mechanic
if not IgnoreCodes == "":
    listIgn = list(IgnoreCodes)
    for i in listIgn:
        not_finished_code += i
        if len(not_finished_code) == 3:
            ign_codes.append(int(not_finished_code))
            not_finished_code = ""

def Scan():
    with open(WordlistPath) as f:
        for i in f:
            i = i.strip()
            i.replace("\n","")
            try:
                Url = OrginialUrl + f"/{i}"
                r = requests.get(Url,headers=Headers,timeout=10)
                if not r.status_code in ign_codes:
                    print(f"URL: {Url} || STATUS CODE: {r.status_code}")
                
                Url = ""
            except IndexError:
                break


for i in range(Threads):
    ThreaD = threading.Thread(target=Scan)
    ThreaD.start()

