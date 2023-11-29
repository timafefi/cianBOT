import logging
import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiogram import types, Bot, Dispatcher
from cian import Cparser
from aiogram.filters.command import Command

logging.basicConfig(level=logging.INFO)
bot = Bot(token='1115198779:AAHPsbIAg3UBSb4A-ZsulryV1LQdi3Ck2Hc')
scheduler = AsyncIOScheduler()
dp = Dispatcher()
cp = Cparser()
ids = []


def beautify_output(j):
    s = f'Цена: {j["price_per_month"]}\nКомнат: {j["rooms_count"]}. '\
        f'Площадь: {j["total_meters"]}м^2\nМетро: {j["underground"]}\n'\
        f'{j["link"]}'
    return s

@dp.message(Command('start'))
async def cmd_start(message: types.Message):
    s = 'Каждые 5 минут вам будет приходить уведомление, если на Циан появится'\
        'новая аренда.\nПараметры по умолчанию:\n'\
        'Цена <= 40000\nКомнаты - 1 или 2\nБез риелтора\nГород - Москва\n'\
        'Чтобы пересать получать уведомления используйте /cancel'
    if message.from_user.id not in ids:
        ids.append(message.from_user.id)
    await message.answer(s)

@dp.message(Command('cancel'))
async def cmd_cancel(message: types.Message):
    s = 'Вы больше не будете получать обновления\n'\
        'Чтобы снова начать их получать, используйте /start'
    ids.pop(message.from_user.id)

async def get_new_flats():
    diff = cp.update()
    print(diff)
    print(ids)
    for i in ids:
        for out in reversed(diff):
            await bot.send_message(i, beautify_output(out))



async def main():
    scheduler.add_job(get_new_flats, "interval", seconds=300)
    scheduler.start()
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
