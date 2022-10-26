import aiogram
from aiogram import Bot, Dispatcher, executor, types
import os
import logging
import config
from image_processor import ImageProcessor

logging.basicConfig(level=logging.INFO)

bot = Bot(token=config.BOT_API_TOKEN)
dp = Dispatcher(bot)


class RecievedPhotoFile(types.Message):

    def __init__(self, message):
        self.photo_filename = message.date.strftime('%d%m%y_%H-%M-%S') + '.jpg'
        self.photo_destination = f'users_photos/{message.from_user.username}_{message.from_user.id}/{self.photo_filename}'


@dp.message_handler(commands=['start'])
async def command_messages(message: types.Message):
    await bot.send_message(message.from_user.id, f'Hi, @{message.from_user.username} 👋 \n\n'
                                                 f'Welcome to @AIPhotoCheck_bot!\n\n'
                                                 f'Send me any picture in .jpg format to analysis it with Error Level Analysis (ELA).\n'
                                                 f'To learn more about ELA use /help command or read: https://en.wikipedia.org/wiki/Error_level_analysis')


@dp.message_handler(commands=['help'])
async def help_message(message: types.Message):
    await bot.send_message(message.from_user.id, f'Error Level Analysis (ELA) permits identifying areas within an image that are at different compression levels. '
                                                 f'With JPEG images, the entire picture should be at roughly the same level. '
                                                 f'If a section of the image is at a significantly different error level, then it likely indicates a digital modification.\n\n'
                                                 f'⚠ Note: send picture as an uncompressed file for best results.')


@dp.message_handler(content_types=['document', 'photo'])
async def file_photo_analysis(message: types.Message):
    logging.info(f'[{message.date}] Recieved message <{message.content_type}> from {message.from_user.username}')
    if message.content_type == 'document' and message.document.mime_type.split('/')[0] != 'image':
        await bot.send_message(message.from_user.id,
                               'Данный тип файлов не поддерживается')
        return
    await bot.send_message(message.from_user.id,
                           'Изображение анализируется:')

    photo_file = RecievedPhotoFile(message)

    match message.content_type:
        case 'document':
            await message.document.download(destination_file=photo_file.photo_destination, make_dirs=True)
        case 'photo':
            await message.photo[-1].download(destination_file=photo_file.photo_destination, make_dirs=True)

    logging.info(
        f'[{message.date}] <Photo> recieved and saved to: {photo_file.photo_destination}')

    image_processor = ImageProcessor(photo_file.photo_destination, quality=90, scale=30, blending_opacity=0.5)

    await send_photo_or_file(message.from_user.id, image_processor.ELA_filename,
                             additional_text='ELA')

    await send_photo_or_file(message.from_user.id, image_processor.overlayed_filename,
                             additional_text='Original image with ELA map')


async def send_photo_or_file(user_id, photo_path, additional_text=None):
    if os.stat(photo_path).st_size < config.max_photo_size_bytes:
        await bot.send_photo(user_id, open(photo_path, 'rb'),
                             caption=additional_text)
    else:
        await bot.send_document(user_id, open(photo_path, 'rb'),
                                caption=additional_text)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
