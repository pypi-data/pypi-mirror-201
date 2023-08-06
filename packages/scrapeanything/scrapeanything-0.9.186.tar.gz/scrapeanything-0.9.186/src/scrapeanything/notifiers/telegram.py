import requests
from scrapeanything.database.repository import Repository
from scrapeanything.utils.config import Config
from scrapeanything.utils.service import Service

class TelegramBot(Service):

    def __init__(self, config: Config=None, repository: Repository=None) -> None:
        super().__init__(config, repository)

        self.TOKEN = self.config.get(section='NOTIFIERS', key='TELEGRAM_CHATID')
        self.CHAT_ID = self.config.get(section='NOTIFIERS', key='TELEGRAM_TOKEN')
        # self.TOKEN = '6023559959:AAHYuMGqqqAtO4I5D3DSX5THtVLGaYgsuTI'
        # self.CHAT_ID = '-1001845468851'

    def get_chat_id(self) -> str:
        url = f"https://api.telegram.org/bot{self.TOKEN}/getUpdates"
        print(requests.get(url).json())

    def send_message(self, message: str) -> None:
        url = f"https://api.telegram.org/bot{self.TOKEN}/sendMessage?chat_id={self.CHAT_ID}&text={message}"
        print(requests.get(url).json()) # this sends the message

    def send_image(self, filename: str) -> None:
        file = { 'photo': open(filename, 'rb') }
        resp = requests.post()