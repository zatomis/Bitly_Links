import requests
import json
import os
import sys
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
  if (response.ok):
    return (response.json)["id"]
  else:
    return False


def click_count(token, url):
  bitly_url = f"https://api-ssl.bitly.com/v4/bitlinks/{url}/clicks/summary"
  headers = {'Authorization': f'Bearer {token}'}
  response = requests.get(bitly_url, headers=headers)
  response.raise_for_status()
  return (response.json)["total_clicks"]


def createParser ():
    parser = argparse.ArgumentParser()
    parser.add_argument ('-l', '--link')
    return parser


if __name__ == '__main__':
  parser = createParser()
  link_convert = parser.parse_args(sys.argv[1:]).link
  load_dotenv(find_dotenv())
  token = os.environ.get("BITLINK_TOKEN", "ERROR")
  if token=="ERROR":
    print("Не указан токен Bitly")
  else:  
    if (str(link_convert) == "None"):
      bitlink = input("Введите ссылку : ")
    else:
      bitlink = link_convert
    try:
      if is_bitlink(token, bitlink):
          print(f"Кол-во переходов по ссылке : {str(click_count(token, bitlink))}")
      else:
          if (shorten_link(token, bitlink)):
            print(f"Короткая ссылка : {shot_link}\nПереходов по ней : {str(click_count(token, bitlink))}")
    except requests.exceptions.HTTPError:
      print("Указана не верная ссылка")
