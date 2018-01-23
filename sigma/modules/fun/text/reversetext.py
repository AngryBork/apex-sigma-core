import discord


async def reversetext(cmd, message, args):
    if args:
        text = ' '.join(args)
        reverse_output = reversed(text)
        response = discord.Embed(color=0x3B88C3)
        response.add_field(name='↩ Reversed Text', value=''.join(reverse_output)[:800])
    else:
        response = discord.Embed(color=0xBE1931, title='❗ Nothing inputted.')
    await message.channel.send(embed=response)
