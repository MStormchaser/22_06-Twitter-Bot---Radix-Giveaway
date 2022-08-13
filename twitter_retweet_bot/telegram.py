import os
from dotenv import load_dotenv
import requests
import report as rep
import logging as log


# logging config
log.basicConfig(level=log.INFO, filename="retweet_bot/logs/retweet_log.log", filemode="a", 
                    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s")
# set it to var logger
logger = log.getLogger(__name__)

# holds the api token
load_dotenv()
api_key = os.getenv('telegram_token')
chat_id = os.getenv("chat_id")



class TelegramBot():

    def __init__(self, token, chat_id):
        self.token = token
        self.chat_id = chat_id
        self.base_url = f"https://api.telegram.org/bot{self.token}"

    def send_message(self, text):
        url = f"{self.base_url}/sendMessage"
        params = {"chat_id": self.chat_id, "text":text}
        response = requests.get(url, data=params)

        if response.status_code == 200:
            log.info(f"Message sent. Status Code: {response.status_code}")
        else:
            log.error(f"Message NOT send. A problem occured. Error Message: {response.text}")


    def send_image(self, image_path):
        """
        LOCAL IMAGES:
        - Image path must be passed in as read binary in a dictionary
        file = {}
        file["photo"] = open(file, "rb")

        HOSTED IMAGES:
        -  Full url path
        """

        url = f"{self.base_url}/sendPhoto"
        params = {"chat_id": self.chat_id}
        response = requests.get(url, data=params, files=image_path)

        if response.status_code == 200:
            log.info(f"Image sent. Status Code: {response.status_code}")
        else:
            log.error(f"Image NOT send. A problem occured. Error Message: {response.text}")

def telegram_run():
    client = TelegramBot(api_key, chat_id)
    client.send_image(rep.daily_count_plot())
    client.send_message(rep.daily_nums())

