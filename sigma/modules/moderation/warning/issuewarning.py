import secrets

import arrow
import discord

from sigma.core.utilities.data_processing import user_avatar
from sigma.core.utilities.event_logging import log_event
from sigma.core.utilities.generic_responses import permission_denied


def warning_data(author: discord.Member, target: discord.Member, reason: str):
    data = {
        'guild': author.guild.id,
        'moderator': {
            'id': author.id,
            'name': author.name,
            'discriminator': author.discriminator,
            'nickname': author.display_name
        },
        'target': {
            'id': target.id,
            'name': target.name,
            'discriminator': author.discriminator,
            'nickname': author.display_name
        },
        'warning': {
            'id': secrets.token_hex(2),
            'active': True,
            'reason': reason,
            'timestamp': arrow.utcnow().float_timestamp
        }
    }
    return data


def make_log_embed(author: discord.Member, target: discord.Member, warn_data: dict):
    target_avatar = user_avatar(target)
    author_descrp = f'{author.mention}\n{author.name}#{author.discriminator}'
    target_descrp = f'{target.mention}\n{target.name}#{target.discriminator}'
    response = discord.Embed(color=0xFFCC4D, timestamp=arrow.utcnow().datetime)
    response.set_author(name=f'{target.name} has been warned by {author.name}.', icon_url=target_avatar)
    response.add_field(name='⚠ Warned User', value=target_descrp, inline=True)
    response.add_field(name='🛡 Moderator', value=author_descrp, inline=True)
    response.add_field(name='📄 Reason', value=warn_data.get('warning').get('reason'), inline=False)
    response.set_footer(text=f'[{warn_data.get("warning").get("id")}] UserID: {target.id}')
    return response


async def issuewarning(cmd, message, args):
    if message.author.guild_permissions.manage_messages:
        if message.mentions:
            target = message.mentions[0]
            if target.id != message.author.id:
                if not target.bot:
                    reason = ' '.join(args[1:]) if args[1:] else 'No reason stated.'
                    warn_data = warning_data(message.author, target, reason)
                    warn_iden = warn_data.get('warning').get('id')
                    await cmd.db[cmd.db.db_cfg.database].Warnings.insert_one(warn_data)
                    response = discord.Embed(color=0x77B255, title=f'✅ Warning {warn_iden} issued to {target.name}.')
                    log_embed = make_log_embed(message.author, target, warn_data)
                    await log_event(cmd.bot, message.guild, cmd.db, log_embed, 'LogWarnings')
                    to_target = discord.Embed(color=0xFFCC4D)
                    to_target.add_field(name='⚠ You received a warning.', value=f'Reason: {reason}')
                    to_target.set_footer(text=f'From {message.guild.name}', icon_url=message.guild.icon_url)
                    try:
                        await target.send(embed=to_target)
                    except Exception:
                        pass
                else:
                    response = discord.Embed(color=0xBE1931, title=f'❗ You can\'t target bots.')
            else:
                response = discord.Embed(color=0xBE1931, title=f'❗ You can\'t target yourself.')
        else:
            response = discord.Embed(color=0xBE1931, title=f'❗ You didn\'t tag any user.')
    else:
        response = permission_denied('Manage Messages')
    await message.channel.send(embed=response)
