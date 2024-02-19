import requests
import threading
from settings import ROBLOX_COOKIE, WEBHOOK_URL
import time
import json
import os

VERSION = "V1.0.4"

ErrorImage = "data:image/png;base64,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"

usersToCheck = ("", "")
ItemTypes = {"8": "Hat", "2": "t-Shirt", "47": "Waist", "2": "t-Shirt", "46": "Back", "45": "Front", "44": "Shoulder", "43": "Neck", "42": "Face"}
BlackListedItems = ("4381832739", "4924609718", "2493718915", "4381828509", "301820310")

session = requests.Session()
session.cookies['.ROBLOSECURITY'] = ROBLOX_COOKIE
req = session.post("https://auth.roblox.com/v2/login")
csrf_token = req.headers["x-csrf-token"]

def check_for_json() -> None:
    if not os.path.exists("users.json"):
        with open("users.json", "w") as file:
            json.dump({}, file, indent=4)

    with open('users.json', 'r') as file:
        data = json.load(file)

    for UserId in usersToCheck:
        if not UserId in data:
            data[UserId] = dict()

    with open('users.json', 'w') as file:
        json.dump(data, file, indent=4)

def send_info(ItemId: str, UserId: str) -> None:
    session = requests.Session()
    session.cookies['.ROBLOSECURITY'] = ROBLOX_COOKIE
    req = session.post("https://auth.roblox.com/v2/login")
    csrf_token = req.headers["x-csrf-token"]
    ItemResponse = session.post("https://catalog.roblox.com/v1/catalog/items/details", headers={"x-csrf-token": csrf_token}, json={"items": [{"itemType": "1", "id": ItemId}]}).json()
    if ItemResponse.get("data", None):
        ItemInfo = ItemResponse["data"][0]
        itemRestrictions = ItemInfo["itemRestrictions"]
        UserImage = session.get(f"https://thumbnails.roblox.com/v1/users/avatar?UserIds={UserId}&size=48x48&format=Png&isCircular=false").json().get("data", [{"imageUrl", ErrorImage}])[0].get("imageUrl", "")
        ItemImage = session.get(url=f"https://thumbnails.roblox.com/v1/assets?assetIds={ItemId}&returnPolicy=PlaceHolder&size=42x42&format=Png&isCircular=false").json().get("data", [{"imageUrl", ErrorImage}])[0].get("imageUrl", "")
        UserInfo = session.get(url=f"https://users.roblox.com/v1/users/{UserId}").json()
        ItemName = ItemInfo["name"]
        ItemCreatorName = ItemInfo["creatorName"]
        ItemCreatorId = ItemInfo["creatorTargetId"]
        UserDisplayName = UserInfo["displayName"]
        UserUsername = UserInfo["name"]
        ItemType = ItemTypes[str(ItemInfo["assetType"])]
        if len(itemRestrictions) == 1 and itemRestrictions[0] == "Collectible":
            ItemUnitsLeft = ItemInfo["unitsAvailableForConsumption"]
            ItemLimitPerUser = ItemInfo.get("quantityLimitPerUser",  "No limit")
            ItemTotalUnits = ItemInfo["totalQuantity"]
            embed = {
                "content": "<@&1206229607658037248>",
                "tts": False,
                "embeds": [
                    {
                        "id": 652627557,
                        "title": ItemName,
                        "description": f"**Name: **`{ItemName}`\n**Limit: **`{ItemLimitPerUser}`",
                        "url": f"https://www.roblox.com/catalog/{ItemId}",
                        "color": 3480022,
                        "footer": {
                            "text": VERSION,
                            "icon_url": "https://images-ext-1.discordapp.net/external/UPINthxiOsxL5lbr8VMwnPe0D7cOfSMWZ4lmhHnD8C4/https/cdn-icons-png.flaticon.com/512/521/521269.png"
                        },
                        "author": {
                            "name": f"{UserDisplayName} ({UserUsername})",
                            "url": f"https://www.roblox.com/users/{UserId}/profile",
                            "icon_url": UserImage
                        },
                        "thumbnail": {
                            "url": ItemImage
                        },
                        "fields": [
                            {
                                "id": 327523145,
                                "name": "Price",
                                "value": ItemInfo["price"],
                                "inline": True
                            },
                            {
                                "id": 867853309,
                                "name": "Quantity",
                                "value": f"{ItemUnitsLeft}/{ItemTotalUnits}",
                                "inline": True
                            },
                            {
                                "id": 230240606,
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
        elif itemRestrictions == list():
            ItemPrice = ItemInfo.get("price", None)
            if not ItemPrice:
                ItemPrice = "0"
            embed = {
                "content": "<@&1206229607658037248>",
                "tts": True,
                "embeds": [
                    {
                        "id": 652627557,
                        "title": ItemName,
                        "description": f"**Name: **`{ItemName}`\n**Type: **`{ItemType}`",
                        "url": f"https://www.roblox.com/catalog/{ItemId}/",
                        "color": 3480022,
                        "footer": {
                            "text": VERSION,
                            "icon_url": "https://images-ext-1.discordapp.net/external/UPINthxiOsxL5lbr8VMwnPe0D7cOfSMWZ4lmhHnD8C4/https/cdn-icons-png.flaticon.com/512/521/521269.png"
                        },
                        "author": {
                            "name": f"{UserDisplayName} ({UserUsername})",
                            "url": f"https://www.roblox.com/users/{UserId}/profile",
                            "icon_url": UserImage
                        },
                        "thumbnail": {
                            "url": ItemImage
                        },
                        "fields": [
                            {
                                "id": 327523145,
                                "name": "Price",
                                "value": ItemPrice,
                                "inline": True
                            },
                            {
                                "id": 230240606,
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
        elif len(itemRestrictions) == 1 and itemRestrictions[0] == "Limited":
            ItemLowestPrice = ItemInfo["lowestResalePrice"]
            embed = {
                "content": "<@&1206229607658037248>",
                "tts": True,
                "embeds": [
                    {
                        "id": 652627557,
                        "title": ItemName,
                        "description": f"**Name: **`{ItemName}`\n**Type: **`{ItemType}`",
                        "url": f"https://www.roblox.com/catalog/{ItemId}/",
                        "color": 3480022,
                        "footer": {
                            "text": VERSION,
                            "icon_url": "https://images-ext-1.discordapp.net/external/UPINthxiOsxL5lbr8VMwnPe0D7cOfSMWZ4lmhHnD8C4/https/cdn-icons-png.flaticon.com/512/521/521269.png"
                        },
                        "author": {
                            "name": f"{UserDisplayName} ({UserUsername})",
                            "url": f"https://www.roblox.com/users/{UserId}/profile",
                            "icon_url": UserImage
                        },
                        "thumbnail": {
                            "url": ItemImage
                        },
                        "fields": [
                            {
                                "id": 327523145,
                                "name": "LowestPrice",
                                "value": ItemLowestPrice,
                                "inline": True
                            },
                            {
                                "id": 230240606,
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
        response = session.post(WEBHOOK_URL, json=embed)
        if response.status_code == 429:
            retry_after = response.headers.get("Retry-After", None)
            if retry_after:
                time.sleep(int(retry_after))
    else:
        time.sleep(20)

def get_data() -> object:
    with open('users.json', 'r') as file:
        return json.load(file)

def write_data(data: object, ids1: str, UserId: str) -> None:
    with open('users.json', 'w') as file:
        data[UserId] = ids1
        json.dump(data, file, indent=4)

def get_boughts(ids1: dict, ids2: dict, UserId: str) -> int:
    if ids1 != ids2:
        for countt, idd1 in enumerate(ids1.values(), 1):
            for id1 in idd1:
                if idd1.count(id1) <= 1 and id1 != str():
                    try:
                        ItemsAdded = abs(ids2[str(countt)].index(id1) - idd1.index(id1))
                    except ValueError:
                        continue
                    if ItemsAdded >= 1:
                        for ItemId in idd1[:ItemsAdded]:
                            send_info(ItemId, UserId)
                        break

def get_ids(UserId: str) -> list:
    arr = {'1': [], '2': [], '3': [], '4': [], '5': [], '6': [], '7': [], '8': []}
    for index, tple in enumerate(arr.values()):
        Items = session.get(f"https://inventory.roblox.com/v2/users/{UserId}/inventory/{list(ItemTypes.keys())[index]}?limit=10&sortOrder=Desc", headers={"x-csrf-token": csrf_token}).json().get("data", None)
        if Items:
            for Item in Items:
                ItemId = str(Item["assetId"])
                if ItemId not in BlackListedItems:
                    tple.append(ItemId)
        tple.extend("" * (10 - len(tple)))
    return arr

def main():
    check_for_json()
    while True:
        for UserId in usersToCheck:
            data = get_data()
            ids1 = get_ids(UserId)
            ids2 = data[UserId]
            if ids2 != dict():
                get_boughts(ids1, ids2, UserId)
                write_data(data, ids1, UserId)
                time.sleep(30)
            else:
                write_data(data, ids1, UserId)
                time.sleep(3)

if __name__ == "__main__":
    main_thread = threading.Thread(target=main)
    main_thread.start()
    input("Watching...\n")
    os._exit(0)
