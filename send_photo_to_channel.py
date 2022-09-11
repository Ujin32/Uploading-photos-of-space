import argparse
import os
import random

from dotenv import load_dotenv

from functions_posting_telegram import send_photo_to_channel


def random_file(image_paths_names):
    path, direct, files = random.choice(image_paths_names)
    while len(files) == 0:
        path, direct, files = random.choice(image_paths_names)
        del direct
    else:
        return path, files


def main():
    load_dotenv()
    telegram_token = os.getenv('TELEGRAM_TOKEN')
    chat_id = os.getenv('TELEGRAM_CHAT_ID')
    parser = argparse.ArgumentParser(
        description='Отправляет фото в телеграм канал'
    )
    parser.add_argument('-img_path', '--image_path', help='Путь до фото')
    args = parser.parse_args()
    if args.image_path is not None:
        if os.path.getsize(args.image_path) < 20971520:
            image_path_head, image_path_tail = os.path.split(args.image_path)
            send_photo_to_channel(
                image_path_head,
                image_path_tail,
                chat_id,
                telegram_token
            )
        else:
            print('Размер файла слишком большой, выберете другой файл')
    elif args.image_path is None:
        image_paths_names = []
        for image in os.walk('images'):
            image_paths_names.append(image)
        random_file_path, random_files = random_file(image_paths_names)
        if len(random_files) > 0:
            files_to_send = []
            for img_name in random_files:
                if os.path.getsize(f'{random_file_path}{img_name}') < 20971520:
                    files_to_send.append(img_name)
                else:
                    pass
            img_name = random.choice(files_to_send)
            send_photo_to_channel(
                random_file_path,
                img_name,
                chat_id,
                telegram_token
            )


if __name__ == '__main__':
    main()