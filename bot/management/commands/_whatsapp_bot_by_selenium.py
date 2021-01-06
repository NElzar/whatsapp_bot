from selenium import webdriver

from bot.models import Result, Script, Answer
from ._scripts import get_products_titles, get_step, get_answers_step
import time
from selenium.common.exceptions import NoSuchElementException

users_state = {}


def send_message(driver, text):
    input_box = driver.find_elements_by_class_name("_1awRl")[1]
    input_box.send_keys(text)
    driver.find_elements_by_class_name("_3qpzV")[1].click()


def get_user_phone(driver):
    return driver.find_element_by_css_selector("div[data-id^='false_']").get_attribute('data-id').split('false_')[1].split('@')[0]


def answer_to_message(user_text, user_phone):
    if user_text == "Начать":
        return 'Введите что хотите взять из следующего списка: ' + ', '.join(get_products_titles())
    users_state.setdefault(user_phone, {})
    if user_text in get_products_titles():
        step = get_step(user_text)
        users_state[user_phone] = {
            'step_id': step.pk,
            'next_step_id': step.next_id,
            'user_text': user_text,
        }
        result, _ = Result.objects.get_or_create(user_phone=user_phone)
        result.script = Script.objects.get(title=user_text)
        result.save()
        return step.text + '\n' + ', '.join(step.answers.values_list('text', flat=True))
    if 'step_id' not in users_state[user_phone]:
        return 'Выберите из списка!'
    if user_text in get_answers_step(users_state[user_phone]['step_id']):
        if users_state[user_phone]['next_step_id'] is None:
            return 'Ваш запрос принят. Ожидайте дальнейших инструкций!'
        step = get_step(step=users_state[user_phone]['next_step_id'])
        users_state[user_phone] = {
            'step_id': step.pk,
            'next_step_id': step.next_id,
            'user_text': user_text,
        }
        result = Result.objects.get(user_phone=user_phone)
        result.answers.add(Answer.objects.get(text=user_text))
        result.save()
        return step.text + '\n' + ', '.join(step.answers.values_list('text', flat=True))

    return 'Выберите один из варитантов ответа выше или напишите "Начать"'


def main(driver):
    driver.get('https://web.whatsapp.com/')

    time.sleep(10)

    while True:
        try:
            new_massage = driver.find_element_by_class_name('VOr2j')
        except NoSuchElementException:
            user_name = 'bot'
            user = driver.find_element_by_xpath('//span[@title="{}"]'.format(user_name))
            user.click()
            time.sleep(0.5)
            continue

        new_massage.click()
        last_sent_message = None
        answer_massages = driver.find_elements_by_class_name('message-in')
        if len(answer_massages):
            last_message = answer_massages[-1].text.split('\n')[0]
            if not last_message == last_sent_message:
                last_sent_message = last_message
                user_phone = get_user_phone(driver)
                last_sent_message = answer_to_message(last_message, user_phone)
                send_message(driver, last_sent_message)

        time.sleep(1)


if __name__ == '__main__':
    options = webdriver.ChromeOptions()
    options.add_argument('--user-data-dir=/home/elzar/.config/google-chrome/Default')
    options.add_argument('--profile-directory=Default')
    chrome_browser = webdriver.Chrome(executable_path='./chromedriver', options=options)
    try:
        main(chrome_browser)
    except KeyboardInterrupt:
        chrome_browser.close()
