import logging; logging.basicConfig(format="[%(asctime)s] %(message)s", level=logging.INFO, datefmt="%H:%M:%S")
import os; clear_console = lambda: os.system("cls" if os.name == "nt" else "clear")

clear_console()
print(f"\x1b[38;5;2m", end=" ")
log = (lambda text: logging.info(text))
try:
    log("Import required modules...")
    from math import floor
    import requests
    from pick import pick
    import threading
    import json
    import time
except ModuleNotFoundError:
    try:
        from pick import pick
        install = pick(["Yes", "No"], "Uninstalled modules found, do you want to install them?", indicator=" >> ")[1] == 0
    except ModuleNotFoundError:
        install = input("Uninstalled modules found, do you want to install them? Y/n: ").lower() == "y"

    if install:
        log("Installing required modules...")
        os.system("python -m pip install --upgrade pip")
        os.system("pip install requests -q"); os.system("python -m pip install requests -q"); os.system("py -m pip install requests -q")
        os.system("pip install pick -q"); os.system("python -m pip install pick -q"); os.system("py -m pip install pick -q")
        input("Successfully installed required modules. Reopen the program to continue...")
        exit()
    else:
        input("Installing modules denied. Press \"enter\" to leave...")
        exit()

VERSION = "1.0.8"

BlackListedItems = ("4381832739", "4924609718", "2493718915", "4381828509", "301820310", "4637254498")
ItemTypes = {"8": "Hat", "41": "Hair", "42": "Face", "43": "Neck", "44": "Shoulder",
             "45": "Front", "46": "Back", "47": "Waist", "64": "t-Shirt", "65": "Shirt",
             "66": "Pants", "67": "Jacket", "68": "Sweater", "69": "Shorts", "72": "Skirt"}

def check_for_update() -> None:
    log("Checking for an updates")
    otherData = data["other_staff"]
    if not otherData["auto_update"] or otherData.get("remind_time", 0) > time.time():
        return
    res = requests.get("https://raw.githubusercontent.com/cofiprofim/ItemNotifier/main/main.py").content
    try:
        version = res.decode().strip().split("VERSION = \"")[1].split("\"")[0]
    except IndexError:
        log("Could not get a valid version")
        return
    if version != VERSION:
        update = pick(["Yes", "No", "No, dont remind again", "No, dont remind me in 30 minutes"],
                      "Uninstalled modules found, do you want to install them?",
                      indicator=" >> ")[1]
        if update == 1:
            return
        if update == 2:
            data["other_staff"]["auto_update"] = False
            with open('config.json', "w") as data_file:
                json.dump(data, data_file, indent=4)
            return
        if update == 3:
            data["other_staff"]["remind_time"] = floor(time.time()) + 30 * 60
            with open('config.json', "w") as data_file:
                json.dump(data, data_file, indent=4)
            return
        with open("main.py", "wb") as main_file:
            main_file.write(res)
        log("Restart the program to use the newest version...\n")
        input()
        exit()
    else:
        log("No updates found.")

def load_files() -> dict:
    log("Checking for required files")
    if not os.path.exists("config.json"):
        config_template = {
            "user_config": {
                "users_to_check": [
                    "USER_ID_1",
                    "USER_ID_2"
                ],
                "roblox_cookie": "ROBLOX_SECURITY_COKIE",
                "role_id": "DISCORD_ROLE_ID",
                "ping_with_role": True,
                "discord_webhook": "DISCORD_WEBHOOK"
            },
            "other_staff": {
                "auto_update": True,
                "remind_time": time.time()
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
    if not os.path.exists("ids.json") or not all([userId in json.load(open("ids.json", "r")) for userId in usersToCheck]):
        with open("ids.json", "w") as ids_file:
            json.dump({str(userId): {} for userId in usersToCheck}, ids_file, indent=4)
    return data

def get_csrf_token(roblox_cookie: str) -> str:
    session = requests.Session()
    session.cookies['.ROBLOSECURITY'] = roblox_cookie
    req = session.post("https://auth.roblox.com/v2/login")
    return req.headers["x-csrf-token"], session

def send_info(ItemId: str, userId: str) -> None:
    userConfig = data["user_config"]
    ItemInfo = requests.get(f"https://economy.roblox.com/v2/assets/{ItemId}/details").json()
    if ItemInfo.get("errors", None):
        time.sleep(20)
        send_info(ItemId, userId)
        return
    UserImage = requests.get(f"https://thumbnails.roblox.com/v1/users/avatar?userIds={userId}&size=48x48&format=Png&isCircular=false").json()["data"][0]["imageUrl"]
    ItemImage = requests.get(url=f"https://thumbnails.roblox.com/v1/assets?assetIds={ItemId}&returnPolicy=PlaceHolder&size=42x42&format=Png&isCircular=false").json()["data"][0]["imageUrl"]
    UserInfo = requests.get(url=f"https://users.roblox.com/v1/users/{userId}").json()
    UserDisplayName = UserInfo["displayName"]
    UserUsername = UserInfo["name"]
    ItemName = ItemInfo["Name"]
    ItemId = ItemInfo["AssetId"]
    if not ItemInfo["PriceInRobux"] and ItemInfo["IsLimitedUnique"] or ItemInfo["IsLimited"]:
        csrf_token, session = get_csrf_token(userConfig["roblox_cookie"])
        ItemInfo2 = session.post("https://catalog.roblox.com/v1/catalog/items/details", headers={"x-csrf-token": csrf_token}, json={"items": [{"itemType": "1", "id": ItemId}]}).json()["data"][0]
        ItemPrice = ItemInfo2["lowestResalePrice"]
        PriceNameEmbed = "LowestPrice"
    else:
        PriceNameEmbed = "Price"
        ItemPrice = ItemInfo.get("PriceInRobux", None)
    if not ItemPrice:
        ItemPrice = "0"
    ItemCreatorInfo = ItemInfo["Creator"]
    ItemCreatorName = ItemCreatorInfo["Name"]
    ItemCreatorId = ItemCreatorInfo["CreatorTargetId"]
    ItemSaleLocationInfo = ItemInfo["SaleLocation"]
    ItemSaleLocationType = ItemSaleLocationInfo["SaleLocationType"] if ItemSaleLocationInfo else None
    ItemType = ItemTypes[str(ItemInfo["AssetTypeId"])]
    if ItemInfo["ProductType"] == "Collectible Item":
        CollectiblesItemDetails = ItemInfo["CollectiblesItemDetails"]
        ItemLimit = CollectiblesItemDetails.get("CollectibleQuantityLimitPerUser",  "No limit") if CollectiblesItemDetails.get("CollectibleQuantityLimitPerUser",  "No limit") else "No limit"
        ItemLimitPerUser = f"**Limit**: `{ItemLimit}`"
        ItemUnitsLeft = ItemInfo["Remaining"]
        ItemTotalUnits = CollectiblesItemDetails["TotalQuantity"]
        ItemQuantityEmbed = {
            "id": 482624925,
            "name": "Quantity",
            "value": f"{ItemUnitsLeft}/{ItemTotalUnits}",
            "inline": True
        }
    else:
        ItemQuantityEmbed = None
        ItemLimitPerUser = ""
        SaleLocationEmbed = None
    if ItemSaleLocationType == 6:
        ItemSaleLocationGames = ItemSaleLocationInfo["UniverseIds"]
        while True:
            SaleLocationGamesInfo = [requests.get(f"https://games.roblox.com/v1/games?universeIds={str(UsiverseGameId)}").json().get("data", [{"id": None}])[0] for UsiverseGameId in ItemSaleLocationGames]
            if None not in SaleLocationGamesInfo:
                SaleLocationGames = [(GameInfo["name"], GameInfo["rootPlaceId"]) for GameInfo in SaleLocationGamesInfo]
                SaleLocationsTitle = "Sale Locations" if len(SaleLocationGames) >= 2 else "Sale Location"
                SaleLocations = ""
                for name, idd in SaleLocationGames:
                    SaleLocations += f"- [{name}](https://www.roblox.com/games/{idd})\n"
                break
            else:
                time.sleep(20)
        SaleLocationEmbed = {
            "id": 515061306,
            "name": SaleLocationsTitle,
            "value": SaleLocations,
            "inline": False
        }
    else:
        SaleLocationEmbed = None
    roleId = data["user_config"]["role_id"]
    pingFlag = data["user_config"]["ping_with_role"]
    embed = {
        "content": f"<@&{roleId}>" if pingFlag else "",
        "tts": False,
        "embeds": [
            {
                "id": 652627557,
                "title": ItemName,
                "description": f"**Name: **`{ItemName}`\n**Type: **`{ItemType}`\n{ItemLimitPerUser}",
                "url": f"https://www.roblox.com/catalog/{ItemId}/",
                "color": 43260,
                "footer": {
                    "text": f"v{VERSION}",
                    "icon_url": "https://images-ext-1.discordapp.net/external/UPINthxiOsxL5lbr8VMwnPe0D7cOfSMWZ4lmhHnD8C4/https/cdn-icons-png.flaticon.com/512/521/521269.png"
                },
                "author": {
                    "name": f"{UserDisplayName} ({UserUsername})",
                    "url": f"https://www.roblox.com/users/{userId}/profile",
                    "icon_url": UserImage
                },
                "thumbnail": {
                    "url": ItemImage
                },
                "fields": [
                    *([SaleLocationEmbed] if SaleLocationEmbed else []),
                    {
                        "id": 69386032,
                        "name":PriceNameEmbed,
                        "value": ItemPrice,
                        "inline": True
                    },
                    *([ItemQuantityEmbed] if ItemQuantityEmbed else []),
                    {
                        "id": 37962583,
                        "name": "Creator",
                        "value": f"[{ItemCreatorName}](https://www.roblox.com/groups/{ItemCreatorId})",
                        "inline": True
                    }
                ]
            }
        ],
        "components": [],
        "actions": {},
        }
    response = requests.post(userConfig["discord_webhook"], json=embed)
    if response.status_code == 429:
        retry_after = response.headers.get("Retry-After", None)
        if retry_after:
            time.sleep(int(retry_after))
        send_info(ItemId, userId)
        return
    else:
        time.sleep(2)

def get_ids(userId: str) -> dict:
    arr = {'1': [], '2': [], '3': [], '4': [], '5': [], '6': [], '7': [], '8': [], '9': [], '10': [], '11': [], '12': [], '13': [], '14': [], '15': []}
    for index, value in enumerate(arr.values()):
        response = requests.get(f"https://inventory.roblox.com/v2/users/{userId}/inventory/{list(ItemTypes.keys())[index]}?limit=10&sortOrder=Desc")
        if response.status_code  == 502:
            return get_ids(userId)
        Items = response.json().get("data", None)
        if not Items:
            time.sleep(10)
            return get_ids(userId)
        for Item in Items:
            ItemId = str(Item["assetId"])
            if ItemId not in BlackListedItems:
                value.append(ItemId)
        value.extend("" * (10 - len(value)))
    return arr

def get_data() -> dict:
    with open('ids.json', 'r') as file:
        return json.load(file)

def write_data(data: dict, ids1: str, userId: str) -> None:
    with open('ids.json', 'w') as ids_file:
        data[userId] = ids1
        json.dump(data, ids_file, indent=4)

def get_boughts(ids1: dict, ids2: dict, userId: str) -> int:
    if ids1 == ids2:
        return
    for count, idd1 in enumerate(ids1.values(), 1):
        for id1 in idd1:
            if idd1.count(id1) <= 1 and id1 != str():
                try:
                    ItemsAdded = abs(ids2[str(count)].index(id1) - idd1.index(id1))
                except ValueError:
                    continue
                if ItemsAdded >= 1:
                    for ItemId in idd1[:ItemsAdded]:
                        send_info(ItemId, userId)
                    break

def main() -> None:
    while True:
        for userId in data["user_config"]["users_to_check"]:
            allIds = get_data()
            ids1 = get_ids(userId)
            ids2 = allIds[userId]
            if ids2 == dict():
                write_data(allIds, ids1, userId)
                allIds = get_data()
                ids2 = allIds[userId]
                time.sleep(3)
            get_boughts(ids1, ids2, userId)
            write_data(allIds, ids1, userId)
            time.sleep(15)

if __name__ == "__main__":
    data = load_files()
    check_for_update()
    clear_console()
    main_thread = threading.Thread(target=main, daemon=True)
    main_thread.start()
    log("Watching... (press \"enter\" to exit)")
    input()
