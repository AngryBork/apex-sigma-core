import asyncio
import secrets

import discord

ongoing = []
symbols = ['❤', '♦', '♠', '♣', '⭐', '⚡']


def check_answer(arguments, sequence):
    arguments = arguments[:6]
    loop_index = 0
    results = []
    correct = True
    for arg in arguments:
        loop_index += 1
        if arg == sequence[loop_index]:
            sign = '🔷'
        elif arg in sequence:
            sign = '🔶'
            correct = False
        else:
            sign = '🔻'
            correct = False
        results.append(sign)
    return correct, results


async def sequencegame(cmd, message, args):
    if message.author.id not in ongoing:
        chosen = []
        while len(chosen) < 6:
            symbol = secrets.choice(symbols)
            chosen.append(symbol)
        title = '🎯 You have 90 seconds for each atempt.'
        desc = f'Symbols you can use: {"".join(symbols)}'
        start_embed = discord.Embed(color=0xf9f9f9)
        start_embed.add_field(name=title, value=desc)
        await message.channel.send(embed=start_embed)

        def answer_check(msg):
            if message.author.id == msg.author.id:
                if message.channel.id == msg.channel.id:
                    message_args = msg.content.split(' ')
                    if len(message_args) == 6:
                        good = False
                        for arg in message_args:
                            if arg in symbols:
                                good = True
                                break
                    else:
                        good = False
                else:
                    good = False
            else:
                good = False
            return good

        finished = False
        virtory = False
        timeout = False
        tries = 0
        while not finished and tries < 6:
            try:
                answer = await cmd.bot.wait_for('message', check=answer_check, timeout=90)
                correct, results = check_answer(answer.content.split(' '), chosen)
                tries += 1
                if correct:
                    finished = True
                    virtory = True
                    cmd.db.add_currency(answer.author, message.guild, 50)
                    win_title = f'🎉 Correct, {answer.author.display_name}. You won 50 Kud!'
                    win_embed = discord.Embed(color=0x77B255, title=win_title)
                    await message.channel.send(embed=win_embed)
                else:
                    atempt_title = f'💣 {tries}/6: {"".join(results)}'
                    atempt_embed = discord.Embed(color=0x262626, title=atempt_title)
                    await message.channel.send(embed=atempt_embed)
            except asyncio.TimeoutError:
                finished = True
                virtory = False
                timeout = True
                timeout_title = f'🕙 Time\'s up! It was {"".join(chosen)}...'
                timeout_embed = discord.Embed(color=0x696969, title=timeout_title)
                await message.channel.send(embed=timeout_embed)
        if not virtory and not timeout:
            lose_title = f'💥 Ooh, sorry, it was {"".join(chosen)}...'
            final_embed = discord.Embed(color=0xff3300, title=lose_title)
            await message.channel.send(embed=final_embed)
    else:
        ongoing_error = discord.Embed(color=0xBE1931, title='❗ There is one already ongoing.')
        await message.channel.send(embed=ongoing_error)
