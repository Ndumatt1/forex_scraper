from flask import Flask, jsonify, request
from bs4 import BeautifulSoup
from datetime import datetime
import humanize
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.service import Service as FirefoxService
from sendmail import send_mail
from mailbody import create_email_body
from decouple import config
from flask_cors import CORS
import random


app = Flask(__name__)
CORS(app)


USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/91.0.864.59 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/89.0.2",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15",
]
USER_PASSWORD = config('USER_PASSWORD')
LOGIN_URL = config('LOGIN_URL')
USER_NAME = config('USER_NAME')
HOME_PAGE = config('HOME_PAGE')


@app.route('/', methods=['GET'])
def scraper():
    if request.method == 'GET':
        try:
            # Provide the path to your geckodriver executable
            geckodriver_path = '/usr/local/bin/geckodriver'

            firefox_options = webdriver.FirefoxOptions()
            firefox_options.add_argument("--headless")
            firefox_options.add_argument(f"--user-agent={random.choice(USER_AGENTS)}")

            firefox_service = FirefoxService(geckodriver_path)

            driver = webdriver.Firefox(service=firefox_service, options=firefox_options)
            driver.get(LOGIN_URL)

            # Locate the username and password fields and submit button using XPath
            username_field = driver.find_element("name", "user_name")
            password_field = driver.find_element("name", "user_password")
            submit_button = driver.find_element("xpath", "/html/body/div/div/div/form/div[5]/button")

            # Enter your credentials
            username_field.send_keys(USER_NAME)
            password_field.send_keys(USER_PASSWORD)

            # Click the submit button
            submit_button.click()

            driver.implicitly_wait(5)

            driver.get(HOME_PAGE)

            driver.implicitly_wait(5)

            html_source = driver.page_source

            driver.quit()  # Close the WebDriver

            soup = BeautifulSoup(html_source, 'html.parser')

            card_bodies = soup.find_all('div', class_='card-body')
            signal_data = []

            for card_body in card_bodies:
                data = {}
                
                # Find all interesting titles in the current card
                titles = card_body.find_all(is_interesting_signal_title)
                
                # Extract signal values for the current card
                signal_values = card_body.find_all('div', class_='user-select-all')
                signal_value_texts = [value.text.strip() for value in signal_values]

                timeagos = card_body.find('span', class_='timeago')
                timestamp = timeagos.get('datetime')

                real_date = datetime.utcfromtimestamp(int(timestamp) / 1000)
                hours_difference = (datetime.utcnow() - real_date)

                data['timestamp'] = int(timestamp) / 1000

                # Extracting and associating titles with corresponding signal values
                for title, signal_value_text in zip(titles, signal_value_texts):
                        data[title.text.strip()] = signal_value_text

                currency_pairs = card_body.find('div', class_='signal-title')

                currencies = ' '.join([pair.text.strip() for pair in currency_pairs])
                data['currency_pair'] = currencies
                data['posted'] = humanize.naturaltime(hours_difference)
                signal_data.append(data)

            email_body = create_email_body(signal_data)

            if email_body is None:
                print("No current Signal")
                return jsonify({"status": "failed", "message": "No current Signal"})
            
            send_mail(email_body)
            return jsonify({'status': 'success', 'message': 'Mail sent successfully!'})
        
        except Exception as e:
             print(f"An error occured {e}")
             return jsonify({"status": "failed", "message": "Internal Server Error"})
    

def is_interesting_signal_title(tag):
    return (
    tag.name == 'div' and
    'signal-title' in tag.get('class', []) and
    any(keyword in tag.text for keyword in ['Buy at', 'Sell at', 'Take profit', 'Stop loss']))


if __name__ == '__main__':
    app.run()
