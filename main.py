from settings import ROBLOX_COOKIE, WEBHOOK_URL
import time
import os
import json
import requests

usersToCheck = ("2525288738",)
ItemTypes = {"8": "Hat", "47": "Waist", "2": "t-Shirt", "46": "Back", "45": "Front", "44": "Shoulder", "43": "Neck", "42": "Face"}

if not os.path.exists("users.json"):
    with open("users.json", "w") as users_file:
        json.dump({}, users_file, indent=4)

with open('users.json', 'r') as file:
    data = json.load(file)

for userId in usersToCheck:
    if not userId in data:
        data[userId] = list()

with open('users.json', 'w') as file:
    json.dump(data, file, indent=4)

def get_ids(userId):
    arr = list()
    try:
        for typee in ItemTypes.keys():
            for index, item in enumerate(requests.get(f"https://inventory.roblox.com/v2/users/{userId}/inventory/{typee}?limit=10&sortOrder=Desc").json().get("data", ""), 1):
                if index <= 4:
                    arr.append(item["assetId"])
                else:
                    break
            time.sleep(0.1)
        return arr
    except:
        pass

def main():
    session = requests.Session()
    session.cookies['.ROBLOSECURITY'] = ROBLOX_COOKIE
    req = session.post("https://auth.roblox.com/v2/login")
    csrf_token = req.headers["x-csrf-token"]
    while True:
        for userId in usersToCheck:
            with open('users.json', 'r') as file:
                data = json.load(file)
            ids1 = get_ids(userId)
            ids2 = data[userId]
            if data[userId] != []:
                if ids1 != ids2:
                    with open('users.json', 'w') as file:
                        data[userId] = ids1
                        json.dump(data, file, indent=4)
                        for i in range(len(ItemTypes)):
                            for j in range(len(ItemTypes)):
                                id1 = ids1[i * 4  + j]
                                id2 = ids2[i * 4]
                                if id1 != id2:
                                    with open('users.json', 'w') as file:
                                        data[userId] = ids1
                                        json.dump(data, file, indent=4)
                                    image = requests.get(url=f"https://thumbnails.roblox.com/v1/assets?assetIds={id1}&returnPolicy=PlaceHolder&size=42x42&format=Png&isCircular=false").json().get("data", "")[0].get("imageUrl", "")
                                    user = requests.get(url=f"https://users.roblox.com/v1/users/{userId}").json()
                                    ItemInfo = session.post("https://catalog.roblox.com/v1/catalog/items/details", headers={"x-csrf-token": csrf_token}, json={"items": [{"itemType": "1", "id": id1}]}).json()
                                    userImage = requests.get(f"https://thumbnails.roblox.com/v1/users/avatar?userIds={userId}&size=48x48&format=Png&isCircular=false").json().get("data", "")[0].get("imageUrl", "")
                                    try:
                                        UserName = user["displayName"]
                                        UserFirstName = user["name"]
                                        name = ItemInfo["data"][0]["name"]
                                        price = ItemInfo["data"][0]["price"]
                                        itemType = ItemTypes[str(ItemInfo["data"][0]["assetType"])]
                                    except:
                                        time.sleep(30)

                                    requests.post(WEBHOOK_URL, json={
    "content": "<@&1206229607658037248>",
    "tts": False,
    "embeds": [
        {
            "id": 652627557,
            "title": name,
            "description": f"**Name: **`{name}`\n**Type: **`{itemType}`\n**Price: **`{price}`",
            "url": f"https://www.roblox.com/catalog/{id1}",
            "color": 4599499,
            "footer": {
                "text": "V1.0.1",
                "icon_url": "https://images-ext-1.discordapp.net/external/UPINthxiOsxL5lbr8VMwnPe0D7cOfSMWZ4lmhHnD8C4/https/cdn-icons-png.flaticon.com/512/521/521269.png"
            },
            "author": {
                "name": f"{UserName} ({UserFirstName})",
                "url": f"https://www.roblox.com/users/{userId}/profile",
                "icon_url": userImage
            },
            "thumbnail": {
                "url": image
            },
            "fields": []
        }
    ],
    "components": [],
    "actions": {},
})
                                    time.sleep(1)
                                else:
                                    break
                time.sleep(30)
            else:
                with open('users.json', 'w') as file:
                    data[userId] = ids1
                    json.dump(data, file, indent=4)
                time.sleep(1)

if __name__ == "__main__":
    print("Watching...")
    main()