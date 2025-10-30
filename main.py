import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
SERVER_ID = int(os.getenv("SERVER_ID"))
PREFIX = os.getenv("PREFIX", "!")

intents = discord.Intents.all()
bot = commands.Bot(command_prefix=PREFIX, intents=intents)

# Check guild ID before running any command
async def check_guild(ctx):
    if ctx.guild.id != SERVER_ID:
        await ctx.send("⚠️ This bot is exclusive to KR COMMUNITY. You must get approval from KR staff to use it.")
        return False
    return True

# KRHELP command
@bot.command(name="krhelp")
async def help_command(ctx):
    if not await check_guild(ctx): return
    embed = discord.Embed(title="KR COMMUNITY Bot Commands", color=0x00BFFF)
    embed.add_field(name="!krhelp", value="Shows this help message", inline=False)
    embed.add_field(name="!ann <message>", value="Send announcement in the announcement channel", inline=False)
    embed.add_field(name="!voice temp", value="Temporary voice channel for users (admin only)", inline=False)
    embed.add_field(name="!security on/off", value="Enable/disable server security (admin only)", inline=False)
    embed.add_field(name="!whitelist add/remove @user", value="Manage whitelist users", inline=False)
    embed.add_field(name="!welcome", value="Send welcome message to new members", inline=False)
    await ctx.send(embed=embed)

# ANN command
@bot.command(name="ann")
async def ann_command(ctx, *, message=None):
    if not await check_guild(ctx): return
    if not message:
        await ctx.send("📢 Please provide a message: `!ann <message>`")
        return
    # Send embed announcement
    embed = discord.Embed(title="📣 Announcement", description=message, color=0x00FF00)
    embed.set_footer(text=f"By {ctx.author.display_name}")
    await ctx.send(embed=embed)

# VOICE TEMP
@bot.command(name="voice")
@commands.has_permissions(administrator=True)
async def voice_temp(ctx, sub=None):
    if not await check_guild(ctx): return
    if sub != "temp":
        await ctx.send("❗ Usage: !voice temp")
        return
    # Create temporary voice channel for each member joining
    guild = ctx.guild
    member = ctx.author
    overwrites = {guild.default_role: discord.PermissionOverwrite(connect=True)}
    channel = await guild.create_voice_channel(f"{member.display_name}-temp", overwrites=overwrites, reason=f"Temporary VC for {member.display_name}")
    await ctx.send(f"✅ Temporary voice channel created: {channel.name}")

# SECURITY command
@bot.command(name="security")
@commands.has_permissions(administrator=True)
async def security(ctx, option=None):
    if not await check_guild(ctx): return
    if option not in ["on","off"]:
        await ctx.send("❗ Usage: !security on/off")
        return
    # For demonstration, just reply
    await ctx.send(f"✅ Security system turned {'ON' if option=='on' else 'OFF'}")

# WHITELIST command
@bot.command(name="whitelist")
@commands.has_permissions(administrator=True)
async def whitelist(ctx, action=None, member: discord.Member=None):
    if not await check_guild(ctx): return
    if action not in ["add","remove"] or not member:
        await ctx.send("❗ Usage: !whitelist add/remove @user")
        return
    await ctx.send(f"✅ {member.display_name} has been {action}ed to/from the whitelist (simulated)")

# WELCOME message
@bot.command(name="welcome")
async def welcome(ctx):
    if not await check_guild(ctx): return
    embed = discord.Embed(title="👋 Welcome!", description=f"Welcome to KR COMMUNITY, {ctx.author.display_name}!", color=0xFFD700)
    await ctx.send(embed=embed)

bot.run(TOKEN)
