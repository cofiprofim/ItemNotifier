<p align=center>
  <br>
  <a href="https://github.com/cofiprofim/ItemBoughtNotifier/tree/main" target="_blank"><img src="https://github.com/cofiprofim/ItemBoughtNotifier/assets/121694687/32c122de-3c84-46a0-95e6-70e707d1a24f"/></a>
</p>

<p align="center">
  <a href="#installation">Installation</a>
  &nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;
  <a href="#usage">Usage</a>
  &nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;
  <a href="#faq">FAQ</a>
  &nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;
  <a href="#preview">Preview</a>
</p>

# Installation

```bash
# clone the repository
$ git clone https://github.com/cofiprofim/ItemNotifier.git

# go to bot directory
$ cd ItemNotifier

# install the requirements
$ python -m pip install -r requirements.txt
```

# Usage

## Hosting

To use bot you need host so bot can work 24/7. You can use [pythonanywhere](https://www.pythonanywhere.com/login/) for example.

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

# Preview

<img width="40%" height="40%" src="https://github.com/cofiprofim/ItemBoughtNotifier/assets/121694687/8946e121-747d-48d2-9731-6754306cae12"/>

# FAQ

<details>
<summary><strong>How to get .ROBLOSECURITY cookie (Click to expand) </strong></summary>

#### Go to [roblox web](https://www.roblox.com/home) and register if you didn't yet.
#### After you done with it open developer tools by pressing `Ctrl + Shift + I` or `F12`.
#### And press `Application` on the top.

![image](https://github.com/cofiprofim/ItemBoughtNotifier/assets/121694687/c74151cf-5ce4-4a1d-a23b-60c9bfe6d721)

#### Expand `Cookies` section and click on `https://www.roblox.com`

![image](https://github.com/cofiprofim/ItemBoughtNotifier/assets/121694687/9971f1e4-9ef8-4da6-aec5-2622dc291dba)

##### Doubleclick on .ROBLOSECURITY value and copy value from it

![image](https://github.com/cofiprofim/ItemBoughtNotifier/assets/121694687/5755fc32-397b-4272-8a21-4c7695a63009)

##### That what you copied is .ROBLOSECURITY cookie
</details>

<details>
<summary><strong>How to get discord webhook </strong></summary>



#### Click on settings of this channel

![image](https://github.com/cofiprofim/ItemBoughtNotifier/assets/121694687/8f12820b-439f-4822-a409-ca640ac91ce0)

#### After click on `Integrations`

![image](https://github.com/cofiprofim/ItemBoughtNotifier/assets/121694687/1853c72c-042e-4cd4-a3db-2668bb97cde3)

#### Click on `Webhooks` and after on `Copy Webhook URL`

![image](https://github.com/cofiprofim/ItemBoughtNotifier/assets/121694687/130a1086-c1df-47c2-a1f9-c8218b7d0cfe)
![image](https://github.com/cofiprofim/ItemBoughtNotifier/assets/121694687/0813bb4f-d429-46ae-a194-3aed8cc888e1)

#### And that you just copied is webhook url

</details>

<details>
<summary><strong>How to create and get role id </strong></summary>

#### First create your own serve if you haven't yet.
#### After when you done with it click on `settings` button

![image](https://github.com/cofiprofim/ItemBoughtNotifier/assets/121694687/6e30beae-6a3f-4ed1-a3a5-60988e3750a1)

#### Click on ``

</details>

<details>
<summary><strong>How to create your own discord server </strong></summary>

#### On the bottom left click on `+` button

![image](https://github.com/cofiprofim/ItemBoughtNotifier/assets/121694687/0fb79498-ca72-46f6-a3d0-484bb993ce77)

#### Click on `Create My Own`

![image](https://github.com/cofiprofim/ItemBoughtNotifier/assets/121694687/7724fafe-6915-493c-bb56-c293f0fdc9e4)

#### And on `For me and my friends`

![image](https://github.com/cofiprofim/ItemBoughtNotifier/assets/121694687/8172d44b-3551-47b2-9a0f-5282e12dcbdd)

#### Click on `Create` button

![image](https://github.com/cofiprofim/ItemBoughtNotifier/assets/121694687/8d42dd65-7d6b-4a3b-9d67-213188617934)

#### And now you have your own server!

</details>
