import discord


async def shadowpollvisible(cmd: SigmaCommand, message: discord.Message, args: list):
    if args:
        poll_id = args[0].lower()
        poll_file = await cmd.db[cmd.db.db_cfg.database].ShadowPolls.find_one({'id': poll_id})
        if poll_file:
            author = poll_file['origin']['author']
            if author == message.author.id:
                visible = poll_file['settings']['visible']
                if not visible:
                    poll_file['settings'].update({'visible': True})
                    await cmd.db[cmd.db.db_cfg.database].ShadowPolls.update_one({'id': poll_id}, {'$set': poll_file})
                    response = discord.Embed(color=0xF9F9F9, title=f'👁 Poll {poll_file["id"]} is now visible.')
                else:
                    response = discord.Embed(color=0xBE1931, title=f'❗ Poll {poll_file["id"]} is already visible.')
            else:
                response = discord.Embed(color=0xBE1931, title='⛔ You didn\'t make this poll.')
        else:
            response = discord.Embed(color=0x696969, title='🔍 I couldn\'t find that poll.')
    else:
        response = discord.Embed(color=0xBE1931, title='❗ Missing poll ID.')
    await message.channel.send(embed=response)
