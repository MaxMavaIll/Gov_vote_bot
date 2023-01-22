from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler_di import ContextSchedulerDecorator
from tzlocal import get_localzone
from aiogram import Bot


def setup_scheduler(bot):
    scheduler = ContextSchedulerDecorator(
        AsyncIOScheduler( timezone=str(get_localzone()))
    )
    scheduler.ctx.add_instance(bot, declared_class=Bot)
    return scheduler
