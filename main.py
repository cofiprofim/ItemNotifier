import logging; logging.basicConfig(format="[%(asctime)s] %(message)s", level=logging.INFO, datefmt="%H:%M:%S")
import os; clear_console = lambda: os.system("cls" if os.name == "nt" else "clear")

clear_console()
log = (lambda text: logging.info(text))
try:
    log(f"\x1b[38;5;2mImport required modules...")
    from math import floor
    import requests
    import threading
    import json
    import time
except ModuleNotFoundError:
    install = input("Uninstalled modules found, do you want to install them? Y/n: ").lower() == "y"
    if install:
        log("Installing required modules...")
        os.system("python -m pip install --upgrade pip")
        os.system("pip install requests -q")
        os.system("python -m pip install requests -q")
        os.system("py -m pip install requests -q")
        input("Successfully installed required modules. Reopen the program to continue...")
        exit()
    else:
        input("Installing modules denied. Press \"enter\" to leave...")
        exit()

VERSION = "1.0.7"

BlackListedItems = ("4381832739", "4924609718", "2493718915", "4381828509", "301820310")
ItemTypes = {"8": "Hat", "41": "Hair", "42": "Face", "43": "Neck", "44": "Shoulder",
             "45": "Front", "46": "Back", "47": "Waist", "64": "t-Shirt", "65": "Shirt",
             "66": "Pants", "67": "Jacket", "68": "Sweater", "69": "Shorts", "72": "Skirt"}

def check_for_update():
    otherData = data["auto_update"]
    if not data["auto_update"] or data.get("remind_time", 0) > time.time():
        return
    res = requests.get("https://pastefy.app/ODIA7pbz/raw").content.decode().strip()
    try:
        version = res.split("VERSION = \"")[1].split("\"")[0]
    except IndexError:
        print("Could not get a valid version")
        return
    if version != VERSION:
        update = pick(["Yes", "No", "No, dont remind me again.", "No, remind me in 30 minutes."],
                        "New update found, do you want to update?",
                        indicator=" >> ")[1]
        if update == 1:
            print("Updates was skipped")
            return
        if update == 2:
            data["auto_update"] = False
            with open('data.json', "w") as data_file:
                json.dump(data, data_file, indent=4)
            print("Update was skipped")
            return
        if update == 3:
            data["remind_time"] = floor(time.time()) + 30 * 60
            with open('data.json', "w") as data_file:
                json.dump(data, data_file, indent=4)
            return
        with open("main.py", "w", encoding="utf-8") as main_file:
            main_file.write(res)
        input("Code were updated! Restart the program to use the newest version...\n")
        exit()
    else:
        print("No updates found.")

def load_files():
    log("Checking for required files.")
    if not os.path.exists("config.json"):
        config_template = {
            "user_config": {
                "users_to_check": [
                    "USER_ID_1",
                    "USER_ID_2"
                ],
                "roblox_cookie": "ROBLOX_SECURITY_COKIE",
                "discord_webhook": "DISCORD_WEBHOOK"
            },
            "other_staff": {
                "auto_update": True,
                "update_reminder": time.time()
            }
        }
        with open("config.json", "w") as config_file:
            json.dump(config_template, config_file, indent=4)
        input(f"\x1b[38;5;1mRequired files were created. Fill up \"config.json\" to continue...\n")
        exit()
    with open("config.json", "r") as config_file:
        data = json.load(config_file)
    userConfig = data["user_config"]
    usersToCheck = userConfig["users_to_check"]
    if not userConfig["roblox_cookie"].startswith("_|WARNING:-DO-NOT-SHARE-THIS.--Sharing-this-will-allow-someone-to-log-in-as-you-and-to-steal-your-ROBUX-and-items.|_") or not userConfig["discord_webhook"].startswith("https://discord.com/api/webhooks/") or usersToCheck[0] == "USER_ID_1":
        input(f"\x1b[38;5;1mRequired files were created. Fill up \"config.json\" to continue...\n")
        exit()
    if not os.path.exists("ids.json") or all([userId in json.load(open("ids.json", "r")) for userId in usersToCheck]):
        with open("ids.json", "w") as ids_file:
            data = {str(UserId): {} for UserId in usersToCheck}
            json.dump(data, ids_file, indent=4)
    return data

def main():
    time.sleep(111)

if __name__ == "__main__":
    data = load_files()
    #check_for_update()
    main_thread = threading.Thread(target=main)
    main_thread.start()
    clear_console()
    log("Watching... (press \"enter\" to exit)")
    input()
    os._exit(0)
