from sigma.core.mechanics.statistics import StatisticsStorage

stats = None


async def ev_mention(ev, message):
    global stats
    if stats is None:
        stats = StatisticsStorage(ev.db, 'mention')
    stats.add_stat()
