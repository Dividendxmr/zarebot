import discord, requests
from discord.ext import commands, tasks
from discord.ext.commands import CommandNotFound

client = commands.Bot(command_prefix = ".")
client.remove_command("help")

checks = None

@client.event
async def on_ready():
    API_request.start()
    activity = discord.Game(name="Watching out for attacks", type=3)
    await client.change_presence(status=discord.Status.online, activity=activity)
    print("\033[1;31;40mZareBot now successfully started!")
    print("\033[1;33;40m                   \033[1;30;40mCoded by Dividend.")

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, CommandNotFound):
        await ctx.send("This command doesn't exist!") 
    else:
        raise error

@client.command(aliases=["HELP"], pass_contect=True)
async def help(ctx):
    roleUser = discord.utils.get(ctx.guild.roles, name="ZareBotUser")
    roleDev = discord.utils.get(ctx.guild.roles, name="ZareBotDev")

    if roleUser in ctx.author.roles or roleDev in ctx.author.roles:
        embed = discord.Embed(
            title = "All the possible commands",
            color = discord.Color.green()
        ).add_field(
            name = ".adduser",
            value = "Adding users to the bot (admins only)",
            inline = False
        ).add_field(
            name = ".removeuser",
            value = "Removing users from the bot (admins only)",
            inline = False
        ).add_field(
            name = ".stats",
            value = "See the server statistics",
            inline = False
        ).add_field(
            name = ".powercycle",
            value = "Powercycling the server (admins only)",
            inline = False
        ).add_field(
            name = ".start",
            value = "Starting the server (admins only)",
            inline = False
        ).add_field(
            name = ".shutdown",
            value = "Shutting down the server (admins only)",
            inline = False
        ).set_thumbnail(
            url = "https://images-ext-1.discordapp.net/external/PdPB_vtwsCqKqqI5II7dI72GBTC6eVNbtS6tBhcpWB4/https/image.prntscr.com/image/OlVPfoW3TPWYkUCcc-EBNQ.png"
        ).set_footer(
            text = f"Requested by {ctx.author} -  ZareBot"
        )

        await ctx.send(embed=embed)
    else:
        await ctx.send(f"{ctx.author} you don't have access to this bot!")


@client.command(aliases=["ADDUSER"])
async def adduser(ctx, user: discord.Member, addRole):
    role = discord.utils.get(ctx.guild.roles, name="ZareBotDev")
    if role in ctx.author.roles:
        if addRole == "user":
            userRole = "ZareBotUser"
            await user.add_roles(discord.utils.get(user.guild.roles, name=userRole))
            await ctx.send(f"{user} now has the role {userRole}")
        elif addRole == "admin":
            userRole = "ZareBotDev"
            await user.add_roles(discord.utils.get(user.guild.roles, name=userRole))
            await ctx.send(f"{user} now has the role {userRole}")
    else:
        await ctx.send(f"{ctx.author} you can't use this command!")

@client.command(aliases=["REMOVERUSER"])
async def removeuser(ctx, user: discord.Member, removeRole):
    checkRole = discord.utils.get(ctx.guild.roles, name="ZareBotDev")
    if checkRole in ctx.author.roles:
        if removeRole == "user":
            role = discord.utils.get(ctx.guild.roles, name="ZareBotUser")
            await user.remove_roles(role)
            await ctx.send(f"The role {removeRole} has been removed from {user}")

    else:
        await ctx.send(f"{ctx.author} you can't use this command!")



@client.command(aliases=["STATS"])
async def stats(ctx):
    checkRole = discord.utils.get(ctx.guild.roles, name="ZareBotUser")
    checkRole2 = discord.utils.get(ctx.guild.roles, name="ZareBotDev")
    if checkRole in ctx.author.roles or checkRole2 in ctx.author.roles:
        url = "https://manager.zare.com/api/v1/dedicated"
        headers = {
            'Authorization': "ANr5LIyafLcwhFEmNiIHEqIhcHl96xWd"
        }
        body = {
            'server_id': '1474921336'
        }

        resp = requests.post(url, headers=headers, data=body)
        jsonResponse = resp.json()

        #All the variables needed in the embed
        OS = jsonResponse["OS"]
        cpu = jsonResponse["processor"]
        IP = jsonResponse["IP"]
        RAM = jsonResponse["memory"]

        embed = discord.Embed(
            title = "The server statistics",
            color = discord.Color.green()
        ).add_field(
            name = "Server IP",
            value = {IP},
            inline = False
        ).add_field(
            name = "Server OS",
            value = {OS},
            inline = False
        ).add_field(
            name = "Server CPU",
            value = {cpu},
            inline = False
        ).add_field(
            name = "Server RAM",
            value = f"{RAM}GB",
            inline = False
        )

        await ctx.send(embed=embed)
    else:
        ctx.send(f"{ctx.author} you can't use this command!")


@client.command(aliases=["POWERCYCLE"])
async def powercycle(ctx):
    checkRole = discord.utils.get(ctx.guild.roles, name="ZareBotDev")
    if checkRole in ctx.author.roles:
        url = "https://manager.zare.com/api/v1/dedicated/powercycle"
        headers = {
        'Authorization': "ANr5LIyafLcwhFEmNiIHEqIhcHl96xWd"
        }
        body = {
            'server_id': '1474921336'
        }

        requests.post(url, headers=headers, data=body)
        await ctx.send(f"{ctx.author} your server was successfully powercycled!")
    else:
        await ctx.send(f"{ctx.author} you can't use this command!")


@client.command(aliases=["SHUTDOWN"])
async def shutdown(ctx):
    checkRole = discord.utils.get(ctx.guild.roles, name="ZareBotDev")
    if checkRole in ctx.author.roles:
        url = "https://manager.zare.com/api/v1/dedicated/poweroff"
        headers = {
        'Authorization': "ANr5LIyafLcwhFEmNiIHEqIhcHl96xWd"
        }
        body = {
            'server_id': '1474921336'
        }
        
        requests.post(url, headers=headers, data=body)
        await ctx.send(f"{ctx.author} just took down the server!")
    else:
        await ctx.send(f"{ctx.author} you can't use this command!")


@client.command(aliases=["START"])
async def start(ctx):
    checkRole = discord.utils.get(ctx.guild.roles, name="ZareBotDev")
    if checkRole in ctx.author.roles:
        url = "https://manager.zare.com/api/v1/dedicated/poweroff"
        headers = {
            'Authorization': 'ANr5LIyafLcwhFEmNiIHEqIhcHl96xWd'
        }
        body = {
            'server_id': '1474921336'
        }

        requests.post(url, headers=headers, data=body)
        await ctx.send(f"{ctx.author} turned on the server!")
    else:
        await ctx.send(f"{ctx.author} you can't use this command!")


@tasks.loop(seconds=10)
async def API_request():
    channel = client.get_channel(id=767443353977225247)

    url = "https://manager.zare.com/api/v1/dedicated/firewall"
    headers = {
    'Authorization': "ANr5LIyafLcwhFEmNiIHEqIhcHl96xWd"
    }
    body = {
        'server_id': '1474921336',
        'scale': 'hour'
    }

    resp = requests.post(url, headers=headers, data=body)
    jsonResponse = resp.json()

    f = open("attacks.txt", "r")
    fLines = f.readlines()
    f.close()

    if checks == 0:
        checks == checks + 1
    else:
       for lines in fLines:
           if len(jsonResponse["firewall"]) == 0:
               pass
           else:
               if jsonResponse["firewall"][0]["id"] in lines:
                pass
               else:
                    #API values have to be stored in variables cuz of embeds...
                    ID = jsonResponse["firewall"][0]["id"]
                    IP = jsonResponse["firewall"][0]["ip"]
                    stats = jsonResponse["firewall"][0]["raw"]

                    writer = open("attacks.txt", "w")
                    writer.write(ID)
                    writer.close()

                    embed = discord.Embed(
                        title = "New attack detected!",
                        color = discord.Color.red()
                    ).add_field(
                        name = "Attack ID",
                        value = f"ID: {ID}",
                        inline = False
                    ).add_field(
                        name = "IP under attack",
                        value = f"IP: {IP}",
                        inline = False
                    ).add_field(
                        name = "Statistics",
                        value = f"{stats}",
                        inline = False
                    ).set_footer(
                        text = " - Attack detected by ZareBot - "
                    ).set_thumbnail(
                        url = "https://images-ext-1.discordapp.net/external/PdPB_vtwsCqKqqI5II7dI72GBTC6eVNbtS6tBhcpWB4/https/image.prntscr.com/image/OlVPfoW3TPWYkUCcc-EBNQ.png"
                    )

                    await channel.send(embed=embed)



client.run("NzY3NDA3NDI3NTQ0ODA5NDcy.X4xd3A.tFYukxGNx8SiWHv2VR2bpuS4tgQ")
