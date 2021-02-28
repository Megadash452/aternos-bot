import Web_bot, json
from discord.ext import commands


def log(string):
    print(string)


def read_token():
    with open("meta.json", 'r') as f:
        return json.load(f)["token"]


def get_prefix(client, message):
    with open("meta.json") as f:
        return json.load(f)["prefix"], bot_tag
    # try:
    #     with open("prefixes.json", 'r') as f:
    #         return json.load(f)[str(message.guild.id)], bot_tag
    # except KeyError:
    #     with open("prefixes.json", 'r') as f:
    #         prefixes = json.load(f)
    #         prefixes[str(message.guild.id)] = '>'
    #     with open("prefixes.json", 'w') as f:
    #         json.dump(prefixes, f, indent=4)
    #         return prefixes[str(message.guild.id)], bot_tag


# --- Globals ---

client = commands.Bot(command_prefix=get_prefix)
web_bot = Web_bot.Web_bot(visible=True)
with open("meta.json", 'r') as file:
    player_role = json.load(file)["game role"]
    if json.load(file)["account type"] == "google":
        web_bot.aternos_logIn_withGoogle()
    else:
        web_bot.aternos_logIn()

bot_tag = "<@!814882164126253076>"

# --- ---


@client.event
async def on_ready():
    print(f"Logged in to Discord as {client.user}")


@client.event
async def on_guild_join(guild):
    with open("prefixes.json", 'r') as f:
        prefixes = json.load(f)
        prefixes[str(guild.id)] = '>'
    with open("prefixes.json", 'w') as f:
        json.dump(prefixes, f, indent=4)
    print(f"Server <{guild.id}> added this bot.")


@client.event
async def on_guild_remove(guild):
    with open("prefixes.json", 'r') as f:
        prefixes = json.load(f)
        prefixes.pop(str(guild.id))
    with open("prefixes.json", 'w') as f:
        json.dump(prefixes, f, indent=4)


@client.event
async def on_message(msg):
    if bot_tag in msg.content:
        await msg.channel.send(f"My prefix is `{client.command_prefix(msg.guild, msg)[0]}`")

    await client.process_commands(msg)


# --- Commands ---
@client.command()
@commands.has_permissions(administrator=True)
async def setprefix(ctx, prefix: str):
    with open("prefixes.json", 'r') as f:
        prefixes = json.load(f)
        prefixes[str(ctx.guild.id)] = prefix
    with open("prefixes.json", 'w') as f:
        json.dump(prefixes, f, indent=4)

        await ctx.send(f"Changed this server's prefix to `{prefix}`")
        print(f"Changed server <{ctx.guild.id}>'s prefix")


# @client.command(aliases=[""])
# @commands.has_permissions(administrator=True)
# async def setgamerole(ctx, role):
#     with open("roles.json", 'r') as f:
#         roles = json.load(f)
#         roles[str(ctx.guild.id)] = {"gamerole": role}
#         json.dump(roles, f, indent=4)
#     player_role = role
#     await ctx.send()


@client.command()
async def invite(ctx):
    await ctx.send("https://discord.com/api/oauth2/authorize?client_id=814882164126253076&scope=bot")


@client.command(
    aliases=["start-server", "serverstart", "server-start", "openserver", "open-server", "serveropen", "server-open"],
    pass_context=True
)
@commands.has_role("Humans")
async def startserver(ctx):
    web_bot.activate_server()
    await ctx.send("Starting up server... (This may take a while)")
    web_bot.check_when_online()
    await ctx.send("Server is now online!")


@client.command(
    aliases=["stop-server", "serverstop", "server-stop", "closeserver", "close-server", "serverclose", "server-close"]
)
@commands.has_permissions(administrator=True)
async def stopserver(ctx):
    await ctx.send("Stopping Server... (This may take a little while)")
    # do
# --- ---


if __name__ == "__main__":
    client.run(read_token())
