required_modules = [
    "ctypes",
    "colorama",
    "requests",
]

for module in required_modules:
    try:
        import importlib
        importlib.import_module(module)    
    except ModuleNotFoundError:
        print(f"Модуль '{module}' не установлен. Пожалуйста, установите его.")

import colorama
import ctypes
import requests
import getpass
import os
import webbrowser

colorama.init()

cyan = colorama.Fore.CYAN


def clear():
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")
def search(query):
    proxynov = f"https://api.proxynova.com/comb?query={query}&start=0&limit=100"
    intelex = f"https://data.intelx.io/saverudata/db2/dbpn/{query[:2]}/{query[2:4]}/{query[4:6]}/{query[6:8]}.csv"
    def searchProxynov(url):
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()

            data = response.json()
            if not data:
                print(cyan, "Proxynov: empty answer")
                return
            
            print(cyan, "─" * 40)

            if "lines" in data:
                for line in data["lines"]:
                    print(cyan, line)
                    print(cyan, "─" * 40)
        except Exception as e:
            print(cyan, f"Proxynov Error: {e}")
    def searchIntelex(url):
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            lines = response.text.splitlines()
            if not lines:
                print(cyan, "Intelx: empty answer")
                return
                
            headers = lines[0].strip('"').split('","')
            print(cyan, f"\nIntelx Results ({len(lines)-1} entries):")
            
            for line in lines[1:]:
                values = line.strip('"').split('","')
                print("─" * 40)
                for header, value in zip(headers, values):
                    if value:
                        print(cyan, f"{header}: {value}")
                        
        except requests.exceptions.RequestException:
            print(cyan, "Intelx: query failed (data may not be found)")
        except Exception as e:
            print(cyan, f"Intelx Error: {str(e)}")

    searchIntelex(intelex)
    searchProxynov(proxynov)
    print(cyan, "Enter to continue...")
    getpass.getpass("")
    main()

def dos(url):
    lib = ctypes.CDLL("./libdoser.so")
    
    lib.StartDos.argtypes = [ctypes.c_char_p]
    lib.GetCount.restype = ctypes.c_ulong
    
    url_bytes = url.encode('utf-8')
    
    lib.StartDos(url_bytes)
    
    try:
        while True:
            lib.GetCount()
            print(f"Requests sent")
    except KeyboardInterrupt:
        lib.StopDos()
        print("Attack stopped")
        print(cyan, "Enter to continue...")
        getpass.getpass("")
        main()


def info():
    print(cyan, """
Welcome to HAPPY TOOL!

HAPPY TOOL is a simple, free, and open-source utility designed with beginners in mind. Whether you're learning or just need a handy tool, we've got you covered!

Our Channel: t.me/crazysofts_4
Developer: t.me/sharpovv
GitHub: 

A Small Request
We encourage customization and sharing, but if you fork or modify this project, please credit the original developer (@sharpovv) in your "Info" section. Good tools thrive when the community respects their origins.

Enjoy using HAPPY TOOL!""")
    print(cyan, "Enter to continue...")
    getpass.getpass("")
    main()

def start():
    clear()
    print(cyan, "Убедительная просьба подать заявку на вступления в наш telegram канал")
    webbrowser.open("https://t.me/+4eamzwNt_0hiMjE0")
    main()

def main():
    clear()
    print(cyan, """
 __   __  _______  _______  _______  __   __   _______  _______  _______  ___     
|  | |  ||   _   ||       ||       ||  | |  | |       ||       ||       ||   |    
|  |_|  ||  |_|  ||    _  ||    _  ||  |_|  | |_     _||   _   ||   _   ||   |    
|       ||       ||   |_| ||   |_| ||       |   |   |  |  | |  ||  | |  ||   |    
|       ||       ||    ___||    ___||_     _|   |   |  |  |_|  ||  |_|  ||   |___ 
|   _   ||   _   ||   |    |   |      |   |     |   |  |       ||       ||       |
|__| |__||__| |__||___|    |___|      |___|     |___|  |_______||_______||_______|
|                                                   |
| dev t.me/sharpovv || channel: t.me/crazysofts_4   |
|___________________________________________________|
[1] Search
[2] DoS
[3] Info
[4] Exit""")
    choice = input("choice > ")
    match choice:
        case "1":
            query = input("query > ")
            search(query)
        case "2":
            url = input("URL > ")
            dos(url)
        case "3":
            info()
        case "4":
            print(cyan, "Bye bye")
            exit()
            
if __name__ == "__main__":
    start()
