<p align="center">
<img width="40%" height="40%" src="https://github.com/cofiprofim/ItemBoughtNotifier/assets/121694687/8946e121-747d-48d2-9731-6754306cae12"/>
</a>
</p>

# Installation
```bash
# clone the repository
$ git clone https://github.com/cofiprofim/ItemBoughtNotifier.git

# go to bot directory
$ cd ItemBoughtNotifier

# install the requirements
$ python -m pip install -r requirements.txt
```
### or
```bash
# clone the repository
$ git clone https://github.com/cofiprofim/ItemBoughtNotifier.git

# go to bot directory
$ cd ItemBoughtNotifier

# opens main.py file, choose "Yes" to install
$ python main.py
```

# Usage

## Hosting
To use bot you need host. You can you [pythonanywhere](https://www.pythonanywhere.com/login/) for example.

## Setup config
Before running code you must fill up `config.json`.
This is a template of config:
```json
{
    "user_config": {
        "users_to_check": [ place there ids of users which you want to watch (!WARNING! 1 id = 20 seconds delay)
            "USER_ID_1", 
            "USER_ID_2"
        ],
        "roblox_cookie": "ROBLOX_SECURITY_COKIE", .ROBLOSECURITY cookie
        "role_id": "DISCORD_ROLE_ID", role id to ping with it
        "ping_with_role": true, flag to ping or not
        "discord_webhook": "DISCORD_WEBHOOK" discord webhook url to send embeds
    },
    "other_staff": { data for program
        "auto_update": true, when there is placed true program will check for updates
        "update_reminder": 1709562018.3200455 time when program can remind you for update
    }
}
```

<details>
<summary><strong>How to get .ROBLOSECURITY cookie (Click to expand) </strong></summary>
#### Create a new server if you didn't

![image](https://github.com/cofiprofim/ItemBoughtNotifier/assets/121694687/0fb79498-ca72-46f6-a3d0-484bb993ce77)

</details>
