import discord


async def removeresponder(cmd, message, args):
    if message.author.permissions_in(message.channel).manage_guild:
        if args:
            trigger = args[0].lower()
            if trigger not in cmd.bot.modules.commands and trigger not in cmd.bot.modules.alts:
                auto_respones = await cmd.db.get_guild_settings(message.guild.id, 'ResponderTriggers')
                if auto_respones is None:
                    auto_respones = {}
                del auto_respones[trigger]
                await cmd.db.set_guild_settings(message.guild.id, 'ResponderTriggers', auto_respones)
                response = discord.Embed(title=f'✅ {trigger} has been removed.', color=0x66CC66)
            else:
                response = discord.Embed(title='❗ Can\'t have the same name as a core command.', color=0xBE1931)
        else:
            response = discord.Embed(title='❗ Nothing was inputted.', color=0xBE1931)
    else:
        response = discord.Embed(title='⛔ Access Denied. Manage Server needed.', color=0xBE1931)
    await message.channel.send(embed=response)
