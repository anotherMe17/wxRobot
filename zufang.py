# -*- coding: utf-8 -*-
import time
import requests
from bs4 import BeautifulSoup

BASE_URL = "http://m.58.com/chaohui/chuzu/0/pn2/?reform=pcfront&PGTID=0d3090a7-0219-c4de-d604-c0c2ad039f78&ClickID=1"


def get_zufang_list():
    url = BASE_URL
    response = requests.get(url)
    decode_zufang_list(BeautifulSoup(response.text, "lxml"))


def has_logr(logr):
    return logr is not None and len(logr) > 26


def decode_zufang_list(soup):
    for zf in soup.find_all('li', attrs={"logr": has_logr}):
        print('-----------------------------------------------------')
        # print(zf.prettify())
        a = zf.find_all('a')
        print('href --> {0}'.format(a[1]['href']))
        # print('desc --> {0}'.format(a[1].text.strip()))
        if len(a) > 3:
            print('district --> {0}'.format(a[3].text.strip()))
        room = zf.find('p', class_='room')
        print('room --> {0}'.format(room.text.strip().replace(' ', '').replace('\n', '')))
        add = zf.find('p', class_='add')
        print('add --> {0}'.format(add.text.strip().replace(' ', '').replace('\n', '')))
        # contract_people = zf.find('p', class_='geren')
        # print('contract_people --> {0}'.format(contract_people.text.strip()))
        # money = zf.find('div', class_='money')
        # print('money --> {0}'.format(money.text.strip()))
        get_room_info(a[1]['href'])


def get_room_info(url):
    room_detail_response = requests.get(url)
    room_detail = BeautifulSoup(room_detail_response.text, "lxml")

    money = room_detail.find('b', class_='f36')
    print('money --> {}'.format(money.text))

    pat_way = room_detail.find('span', class_='c_333')
    print('pat_way --> {}'.format(pat_way.text))

    for info in room_detail.find('ul', class_='f14').find_all('li'):
        print(info.text.strip().replace(' ', '').replace('\n', ''))

    # print(room_detail.prettify())
    # room_info = room_detail.find('ul')
    # print(room_info)
    # for info in room_detail.select('ul.houseInfo-meta > span'):
    #     print(' --> {}'.format(info.text.strip().replace(' ', '').replace('\n', '')))
    # room_equipment = room_detail.find('ul', class_='houseDetail-fac')
    # print(room_equipment)
    # for equipment in room_equipment.find_all('i'):
    #    print(' --> {}'.format(equipment.text.strip().replace(' ', '').replace('\n', '')))

    # desc = room_detail.find('p', class_='panel-description')
    # print('desc --> {0}'.format(desc.text.strip()))
    # location = room_detail.find('img', id='mapimg')
    # print('lon --> {}'.format(location['data-lon']))
    # print('lat --> {}'.format(location['data-lat']))
    time.sleep(20)


if __name__ == '__main__':
    get_zufang_list()
