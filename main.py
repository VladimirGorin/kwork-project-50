import utils.install
from utils.channels import Channels

try:
    channels = Channels("./data/channels.txt")
    channels.read_channels_file()
    channels.create_folders()

    for channel in channels.channels:
        try:
            channels.get_channel_shorts(channel)

            for short_link in channels.shorts_links:
                try:
                    print(f"\nСкачиваем shorts: {short_link}")
                    channels.save_short(short_link)
                except Exception as e:
                    print(f"Произошла ошибка при попытке скачивания shorts (продалжаем работу): {e}")
                    continue

        except Exception as e:
            print(f"Произошла ошибка при попытке получение URL для shorts (продалжаем работу с другим каналом): {e}")
            continue

except Exception as e:
    print(f"Произошла ошибка: {e}")

input("\nНажмите ENTER что бы закрыть консоль.")
