from pytube import YouTube

from selenium import webdriver
from bs4 import BeautifulSoup

import os, time

class Channels():
    def __init__(self, channels_txt_path) -> None:
        self.channels_txt_path = channels_txt_path
        self.channels = []
        self.shorts_links = []

        self.output_path = None

    def read_channels_file(self):
        with open(self.channels_txt_path, "r") as file:
            array = [row.strip() for row in file]
            self.channels = array

        print(f"Получено каналов с файла: {len(self.channels)}")

    def scroll_page(self, driver, channel_url):
        prev_height = 0

        driver.get(channel_url)
        time.sleep(5)

        while True:
            driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight)")
            time.sleep(5)

            current_height = driver.execute_script("return document.documentElement.scrollHeight")

            if current_height == prev_height:
                time.sleep(5)
                new_height = driver.execute_script("return document.documentElement.scrollHeight")
                if new_height == current_height:
                    break

            prev_height = current_height

    def extract_links(self, driver):
        html_content = driver.page_source

        soup = BeautifulSoup(html_content, 'html.parser')

        thumbnails = []

        ytd_items = soup.find_all('ytd-rich-item-renderer')

        for item in ytd_items:
            thumbnail = item.find('a', {'id': 'thumbnail'})
            if thumbnail:
                thumbnail_url = "https://www.youtube.com{}".format(thumbnail.get('href'))
                thumbnails.append(thumbnail_url)

        self.shorts_links = thumbnails


    def get_channel_shorts(self, channel):
        self.output_path = f"./data/shorts/{channel}/"
        print(f'Получаем ссылки на shorts для канала: {channel}')

        driver = webdriver.Chrome()
        channel_shorts_url = "https://www.youtube.com/{}/shorts".format(channel)

        self.scroll_page(driver, channel_shorts_url)
        self.extract_links(driver)
        driver.quit()

        print(f"Всего успешно полуено shorts ссылок: {len(self.shorts_links)}")

    def create_folders(self):
        base_path = './data/shorts/'
        for folder_name in self.channels:
            folder_path = os.path.join(base_path, folder_name)
            try:
                os.makedirs(folder_path)
            except FileExistsError:
                ""

        print("Создание папок для shorts успешно")

    def save_short(self, url):
        short = YouTube(url)
        video_stream = short.streams.filter(file_extension='mp4').first()
        video_path = video_stream.download(output_path=self.output_path)
        print(f"\nВидео сохранено по пути: {video_path}\n")
