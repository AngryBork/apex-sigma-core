import discord

cache = {}


def get_changed_invite(guild_id, bound_list, invites):
    invite = None
    cached = cache.get(guild_id)
    if cached is None:
        cached = []
    if invites is None:
        invites = []
    cache.update({guild_id: invites})
    if invites:
        for cached_inv in cached:
            for curr_inv in invites:
                if cached_inv.uses != curr_inv.uses:
                    if curr_inv.id in bound_list:
                        invite = curr_inv
                        break
    return invite


async def bound_role_cacher(ev):
    for guild in ev.bot.guilds:
        if guild.me.guild_permissions.create_instant_invite:
            try:
                invites = await guild.invites()
            except discord.Forbidden:
                invites = []
            cache.update({guild.id: invites})
