from django.core.management.base import BaseCommand, CommandError
from selenium import webdriver
from ._whatsapp_bot_by_selenium import main


class Command(BaseCommand):
    help = 'Whatsapp Bot handle'

    def handle(self, *args, **options):
        options = webdriver.ChromeOptions()
        options.add_argument('--user-data-dir=/home/melis/.config/google-chrome/Default')
        options.add_argument('--profile-directory=Default')
        chrome_browser = webdriver.Chrome(executable_path='./chromedriver', options=options)
        try:
            main(chrome_browser)
        except KeyboardInterrupt:
            chrome_browser.close()
