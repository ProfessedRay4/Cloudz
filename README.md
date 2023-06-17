# Cloudz

### Installation:
1) Download zip (or git clone)
2) extract zip
3) ``pip install -r requirements.txt``
4) goto [here](https://discord.com/developers/) and get bot token
5) edit `config.json`
6) run setup.bat OR `python main.py`
7) enjoy!

### Changelog:
- added new commands (admin, channels, rename)
- reworked ``nuke`` command
- cleaned code up a bit and added more comments

### config.json:
- TOKEN - Bots token [discord developers](https://discord.com/developers/)
- PROXIES — Use Proxies (Helps not get rate limited)
- SPAM_PRN - Bot spams porn 
- SERVER_NAME - New server name (bot will change it when raiding)
- AMOUNT_OF_CHANNELS - Amount of channels the bot creates
- PREFIX - Bots prefix
- MESSAGE - Message the bot sends (when raiding)
- CHANNEL_NAMES - Name of channels created
- AUTO_RAID - Bot will automatically raid on join if set to true

### Command Info:
  - nuke - completely nukes server, edits server name, gives everyone admin, deletes all roles, deletes all channels and creates channels (and spams using webhooks)
  - ban_all - bans all members from the server
  - kick_all - kicks all members from the server
  - massdm - dm's all members in server (if they are a bot or have dms off it will pass them)
  - admin - give all users in the server admin
  - channels - creates specified ammount of channels and spams in them (using webhooks)
  - rename - rename the server to name in config

### TODO:
- clean up code
- add KeepOnline.py to host a local webserver
- maybe add a gui (coming next ;3)

### Issues:
- Please contact me on discord: [ProfessedRay4#2985](https://discord.com/users/1091415878156943472)
- Leave a `Issue` and I will help you
