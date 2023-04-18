import vk_api
from vk_api import VkUpload
import telegram
from random import choice
import os
from re import sub
import shutil
import asyncio
from datetime import datetime


# авторизуемся в VK API
vk_session = vk_api.VkApi(#token='SECRET')
vk = vk_session.get_api()
upload = VkUpload(vk_session)  # объект для загрузки изображений

# подключение telegram bot
TOKEN = #SECRET
CHAT_ID = #SECRET


# функция для публикации картинки в сообщество
async def post_image():

    # Получение файла в папке
    directory = os.listdir(".")
    files = filter(lambda x: x.endswith('.png') or x.endswith('jpg'), directory)
    files = sorted(list(files))
    get_file = str(choice(files))

    #Поиск ссылки на автора из файла
    with open('arts.txt', 'r', encoding='utf-8') as o:
        for line in o:
            line = line.split()
            if sub(r'.[^.]+$', '', get_file) == line[0]:
                link = line[1]
                break


    #загрузка изображения на сервер VK
    photo = upload.photo_wall(f'{get_file}', group_id='SECRET')[0]

    #создание сообщения с прикрепленной картинкой
    attachments = []
    attachments.append(
        'photo{}_{}'.format(photo['owner_id'], photo['id'])
    )
    vk.wall.post(owner_id='SECRET',  # ID сообщества, куда нужно опубликовать картинку
                 from_group=1,  # флаг, который позволяет опубликовать запись от имени группы
                 attachments=attachments,  # прикрепленная картинка
                 message=f"""#tags""",
                 copyright=f'{link}')

    # Создайте объект бота Telegram
    bot = telegram.Bot(token=TOKEN)

    with open(get_file, 'rb') as f:
        await bot.send_photo(chat_id=CHAT_ID, photo=f)
    print(f'Картинка {get_file} опубликована в VK и Telegram. Время: {datetime.now().strftime("%d.%m.%Y %H:%M")}')

    # Перемещение выложенных файлов
    file_source = ''
    file_destination = ''
    shutil.move(file_source + get_file, file_destination)


async def post_18():
    # Публикация поста 18+
    directory = os.listdir("")
    files = filter(lambda x: x.endswith('.png') or x.endswith('jpg') or x.endswith('jfif'), directory)
    files = sorted(list(files))
    get_file = str(choice(files))

    # Создаём объект бота Telegram
    bot = telegram.Bot(token=TOKEN)

    with open(f'path', 'rb') as f:
        await bot.send_photo(chat_id=CHAT_ID, photo=f, caption='Boom time')
    print(f'Картинка {get_file} опубликована в Telegram 18+ контент. Время: {datetime.now().strftime("%d.%m.%Y %H:%M")}')

    # Перемещение выложенных файлов
    file_source = ''
    file_destination = ''
    shutil.move(file_source + get_file, file_destination)


async def main():
    # Бесконечный цикл, который будет отправлять изображения каждые 4 часа
    # Отладка необходимо из-за ограничений платформ по загрузке файлов(не больше определенного размера и разрешения)
    while True:
        try:
            await post_image()
            if 2 <= datetime.now().hour <= 6:
                await post_18()
                await asyncio.sleep(5 * 60 * 60)
            else:
                await asyncio.sleep(3.3 * 60 * 60)  # каждые 5 часов
        except:
            await post_image()
            if 2 <= datetime.now().hour <= 6:
                await post_18()
                await asyncio.sleep(3.3 * 60 * 60)
            else:
                await asyncio.sleep(3.3 * 60 * 60)  # каждые 5 часов


if __name__ == '__main__':
    asyncio.run(main())
