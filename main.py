import requests
import json
import os
import sys
import argparse
from dotenv import load_dotenv, find_dotenv


def is_active_link(url):
  response = requests.get(url)
  response.raise_for_status()
  return response.ok


def is_bitlink(token, url):
  bitly_url = f"https://api-ssl.bitly.com/v4/bitlinks/{url.strip()}"
  headers = {'Authorization': f'Bearer {token}'}
  response = requests.get(bitly_url, headers=headers)
  response.raise_for_status()
  return response.ok


def shorten_link(token, url):
  bitly_url = "https://api-ssl.bitly.com/v4/bitlinks"
  params = {'long_url': f'{url}'}
  headers = {'Authorization': f'Bearer {token}'}
  response = requests.post(bitly_url, headers=headers, json=params)
  if (response.ok):
    return json.loads(response.text)["id"]
  else:
    return "OtherShotLink"


def click_count(token, url):
  bitly_url = f"https://api-ssl.bitly.com/v4/bitlinks/{url}/clicks/summary"
  headers = {'Authorization': f'Bearer {token}'}
  response = requests.get(bitly_url, headers=headers)
  response.raise_for_status()
  return json.loads(response.text)["total_clicks"]


def createParser ():
    parser = argparse.ArgumentParser()
    parser.add_argument ('-l', '--link')
    return parser


def main(link_convert):
  load_dotenv(find_dotenv())
  token_key = os.environ.get("BITLINK_TOKEN")

  if (link_convert == "None"):
    bitlink = input("Введите ссылку : ")
  else:
    bitlink = link_convert
    
  try:
    if is_bitlink(token_key, bitlink):
        print("Кол-во переходов по ссылке : " +
              str(click_count(token_key, bitlink)))
    else:
      if is_active_link(bitlink):
        shot_link = shorten_link(token_key, bitlink)
        if (shot_link != "OtherShotLink"):
          print("Короткая ссылка : " + shot_link + "\nПереходов по ней : " +
                str(click_count(token_key, bitlink)))
        else:
          print("Это другая сокращенная ссылка : " + bitlink)
  except requests.exceptions.HTTPError:
    print("Ошибка в ссылке")


if __name__ == '__main__':
  parser = createParser()
  main(str(parser.parse_args(sys.argv[1:]).link))
