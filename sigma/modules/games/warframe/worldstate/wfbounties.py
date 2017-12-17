import json

import aiohttp
import arrow
import discord
import yaml


def capital_split(word):
    out = ''
    loop_index = 0
    for char in word:
        loop_index += 1
        if char == char.upper() and loop_index != 1:
            char = f' {char}'
        out += char
    return out


async def wfbounties(cmd, message, args):
    if args:
        try:
            btier = abs(int(args[0]))
            if not 5 >= btier >= 1:
                btier = None
        except ValueError:
            btier = None
        if btier:
            world_state = 'http://content.warframe.com/dynamic/worldState.php'
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(world_state) as data:
                        data = await data.read()
                        data = json.loads(data)
                synd_missions = data['SyndicateMissions']
                poe_data = None
                for synd_mission in synd_missions:
                    if synd_mission['Tag'] == 'CetusSyndicate':
                        poe_data = synd_mission
            except aiohttp.ClientPayloadError:
                poe_data = None
            if poe_data:
                end_stamp = int(poe_data['Expiry']['$date']['$numberLong']) // 1000
                end_arr = arrow.get(end_stamp)
                with open(cmd.resource('bounty_rewards.yml'), encoding='utf-8') as reward_file:
                    reward_data = yaml.safe_load(reward_file)
                job_index = btier - 1
                job = poe_data['Jobs'][job_index]
                job_mission = capital_split(job.get('jobType').split('/')[-1])
                job_rewards = reward_data.get(job.get('rewards').split('/')[-1])
                job_info = f'Levels: {job.get("minEnemyLevel")} - {job.get("maxEnemyLevel")}'
                job_info += f' | Standing: {job.get("xpAmounts")[0]} - {job.get("xpAmounts")[-1]}'
                job_info += f' | Mission: {job_mission}'
                cetus_wh = 'https://vignette.wikia.nocookie.net/warframe/images/8/80/OstronSigil.png'
                cetus_or = 'https://i.imgur.com/Bbz9JOJ.png'
                response = discord.Embed(color=0xb74624, timestamp=end_arr.datetime)
                response.set_author(name=f'Ostron Tier {btier} Bounty', icon_url=cetus_or)
                response.add_field(name='Job Information', value=job_info)
                response.add_field(name='Bounty Rewards', value=', '.join(job_rewards))
                response.set_footer(text=f'Bounties change {end_arr.humanize()}.', icon_url=cetus_wh)
            else:
                response = discord.Embed(title='❗ Could not retrieve Plains of Eidolon data.', color=0xBE1931)
        else:
            response = discord.Embed(title='❗ Invalid tier provided.', color=0xBE1931)
    else:
        response = discord.Embed(title='❗ Please provide a bounty tier.', color=0xBE1931)
    await message.channel.send(embed=response)
