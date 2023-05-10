import requests
import os
import argparse
from dotenv import load_dotenv, find_dotenv


def is_bitlink(token, url):
    bitly_url = f"https://api-ssl.bitly.com/v4/bitlinks/{url}"
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get(bitly_url, headers=headers)
    response.raise_for_status()
    return response.ok


def shorten_link(token, url):
    bitly_url = "https://api-ssl.bitly.com/v4/bitlinks"
    params = {'long_url': url}
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.post(bitly_url, headers=headers, json=params)
    response.raise_for_status()
    return response.json()["id"]


def click_count(token, url):
    bitly_url = f"https://api-ssl.bitly.com/v4/bitlinks/{url}/clicks/summary"
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get(bitly_url, headers=headers)
    response.raise_for_status()
    return response.json()["total_clicks"]


def createParser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-l', '--link')
    return parser


if __name__ == '__main__':
    parser = createParser()
    link_bitly = parser.parse_args().link
    load_dotenv(find_dotenv())
    token = os.environ.get("BITLINK_TOKEN", "ERROR")
    if token == "ERROR":
        print("Не указан токен Bitly")
    else:
        if (str(link_bitly) != "None"):
            bitlink = link_bitly
            try:
                if is_bitlink(token, bitlink):
                    print(f"Кол-во переходов по ссылке : {click_count(token, bitlink)}")
                else:
                    print(f"Короткая ссылка : {shorten_link(token, bitlink)}")

            except requests.exceptions.HTTPError:
                print("Указана не верная ссылка")
        else:
            print("Нет параметра -l <ссылка>")
