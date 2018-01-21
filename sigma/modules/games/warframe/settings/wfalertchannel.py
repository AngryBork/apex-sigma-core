import discord

from sigma.core.mechanics.command import SigmaCommand

async def wfalertchannel(cmd: SigmaCommand, message: discord.Message, args: list):
    if message.author.permissions_in(message.channel).manage_channels:
        if message.channel_mentions:
            target_channel = message.channel_mentions[0]
        else:
            if args:
                if args[0].lower() == 'disable':
                    await cmd.db.set_guild_settings(message.guild.id, 'WarframeAlertChannel', None)
                    response = discord.Embed(title=f'✅ Warframe Alert Channel Disabled', color=0x66CC66)
                    await message.channel.send(embed=response)
                    return
                else:
                    return
            else:
                target_channel = message.channel
        await cmd.db.set_guild_settings(message.guild.id, 'WarframeAlertChannel', target_channel.id)
        response = discord.Embed(title=f'✅ Warframe Alert Channel set to #{target_channel.name}', color=0x66CC66)
    else:
        response = discord.Embed(title='⛔ Access Denied. Manage Channels needed.', color=0xBE1931)
    await message.channel.send(embed=response)
