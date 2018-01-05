﻿import arrow
import discord


async def givecookie(cmd, message, args):
    if message.mentions:
        target = message.mentions[0]
        sabotage_target = await cmd.db[cmd.db.db_cfg.database].SabotagedUsers.find_one({'UserID': target.id})
        sabotage_author = await cmd.db[cmd.db.db_cfg.database].SabotagedUsers.find_one({'UserID': message.author.id})
        author_stamp = arrow.get(message.author.created_at).float_timestamp
        current_stamp = arrow.utcnow().float_timestamp
        time_diff = current_stamp - author_stamp
        if sabotage_author:
            if sabotage_target:
                if time_diff > 2592000:
                    if message.author.id != target.id:
                        if not target.bot:
                            if not await cmd.bot.cool_down.on_cooldown(cmd.name, message.author):
                                upgrade_file = await cmd.db[cmd.db.db_cfg.database].Upgrades.find_one(
                                    {'UserID': message.author.id})
                                if upgrade_file is None:
                                    insert_data = {'UserID': message.author.id}
                                    await cmd.db[cmd.db.db_cfg.database].Upgrades.insert_one(insert_data)
                                    upgrade_file = {}
                                cookie_coll = cmd.db[cmd.db.db_cfg.database].Cookies
                                base_cooldown = 3600
                                if 'stamina' in upgrade_file:
                                    stamina = upgrade_file['stamina']
                                else:
                                    stamina = 0
                                cooldown = int(base_cooldown - ((base_cooldown / 100) * (stamina * 0.2)))
                                file_check = await cookie_coll.find_one({'UserID': target.id})
                                if not file_check:
                                    cookies = 0
                                    data = {'UserID': target.id, 'Cookies': 0}
                                    await cookie_coll.insert_one(data)
                                else:
                                    cookies = file_check['Cookies']
                                cookies += 1
                                await cookie_coll.update_one({'UserID': target.id}, {'$set': {'Cookies': cookies}})
                                await cmd.bot.cool_down.set_cooldown(cmd.name, message.author, cooldown)
                                title = f'🍪 You gave a cookie to {target.display_name}.'
                                response = discord.Embed(color=0xd99e82, title=title)
                            else:
                                timeout_seconds = await cmd.bot.cool_down.get_cooldown(cmd.name, message.author)
                                if timeout_seconds > 60:
                                    timeout_seconds = arrow.utcnow().timestamp + timeout_seconds
                                    timeout = arrow.get(timeout_seconds).humanize()
                                else:
                                    timeout = f'in {timeout_seconds} seconds'
                                timeout_title = f'🕙 You can give another cookie {timeout}.'
                                response = discord.Embed(color=0x696969, title=timeout_title)
                        else:
                            response = discord.Embed(color=0xBE1931, title=f'❗ Bots don\'t eat cookies.')
                    else:
                        response = discord.Embed(color=0xBE1931, title=f'❗ Nope, can\'t give cookies to yourself.')
                else:
                    title = f'❗ Sorry, your account is too young to give cookies.'
                    response = discord.Embed(color=0xBE1931, title=title)
            else:
                response = discord.Embed(color=0xBE1931, title='It seems this user is alergic to cookies.')
        else:
            response = discord.Embed(color=0xBE1931, title='It seems that your oven is broken.')
    else:
        response = discord.Embed(color=0xBE1931, title=f'❗ No user targeted.')
    await message.channel.send(embed=response)
