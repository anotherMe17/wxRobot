# -*- coding: utf-8 -*-
import time
import requests
import re
import pymysql
import hashlib
from bs4 import BeautifulSoup

BASE_URL = "http://hz.58.com/chuzu/0/pn%s/?PGTID=0d3090a7-0004-f510-04c9-70a976ddf913&ClickID=2"
mysql_config = {
    'host': '127.0.0.1',
    'port': 3306,
    'user': 'root',
    'password': 'root',
    'db': 'zufang',
    'charset': 'utf8mb4',
    'cursorclass': pymysql.cursors.DictCursor,
}
# open database
db = pymysql.connect(**mysql_config)


class RoomInfoDB(object):
    house_detail_url = None
    money = 0
    district = None
    room_size = None
    room_layout = None
    room_height = None
    room_orientation = None
    pay_way = None
    leasing_way = None
    lat = 0
    lon = 0

    def __init__(self):
        pass

    def __str__(self):
        room_str = '-----------------------------------------------------------------------------\n'
        # room_str += 'url --> {}\n'.format(self.house_detail_url)
        room_str += '小区 --> {}\n'.format(self.district)
        room_str += '租金 --> {}\n'.format(self.money)
        room_str += '房间大小 --> {}\n'.format(self.room_size)
        room_str += '房间布局 --> {}\n'.format(self.room_layout)
        room_str += '朝向 --> {}\n'.format(self.room_orientation)
        room_str += '高度 --> {}\n'.format(self.room_height)
        room_str += '租赁方式 --> {}\n'.format(self.leasing_way)
        room_str += '支付方式 --> {}\n'.format(self.pay_way)
        room_str += '经纬度 --> {} , {}\n'.format(self.lat, self.lon)
        # print('----------------------------------------------------------------------------------')
        return room_str


def get_zufang_list():
    for page in range(1, 71):
        url = BASE_URL % page
        response = requests.get(url)
        decode_zufang_list(BeautifulSoup(response.text, "lxml"))


def has_logr(logr):
    return logr is not None and len(logr) > 26


def decode_zufang_list(soup):
    for zf in soup.find_all('li', attrs={"logr": has_logr}):
        a = zf.find_all('a')
        get_room_info(a[1]['href'])


def get_room_info(url):
    room_detail_response = requests.get(url)
    room_detail = BeautifulSoup(room_detail_response.text, "lxml")
    # print(room_detail)
    # init room
    room = RoomInfoDB()
    # set house_detail_url
    room.house_detail_url = url
    try:
        room.money = room_detail.find('b', class_='f36').text
        room.pay_way = room_detail.find('span', class_='c_333').text

        # 小区，楼层，面积，付款方式
        other_info = room_detail.find('ul', class_='f14').find_all('span')
        room.leasing_way = other_info[1].text
        # search layout and size
        other_info_search = re.search(r'(.*?)\s+(.*?)\s+(.*)', other_info[3].text)
        if other_info_search is not None:
            room.room_layout = other_info_search.group(1)
            room.room_size = other_info_search.group(2)
        # search orientation and height
        room_orientation_search = re.search(r'(.*?)\s+(.*)', other_info[5].text)
        if room_orientation_search is not None:
            room.room_orientation = room_orientation_search.group(1)
            room.room_height = room_orientation_search.group(2)

        room.district = room_detail.find('a', class_='c_333 ah').text

        # house location
        location = room_detail.find('div', id='ditu')
        if location is not None:
            # location might empty
            a_tag = location.find('a')
            if a_tag is not None:
                search_location = re.search(r'location=(.*),(.*)&title', location.find('a')['href'])
                room.lat = search_location.group(1)
                room.lon = search_location.group(2)
        print(room)
    except AttributeError as e:
        print(e)
    write_room_into_db(room)
    time.sleep(3)


def write_room_into_db(room):
    sql = '''
    INSERT INTO `room`(id,url,district,room_size,room_layout,room_height,room_orientation,pay_way,
    leasing_way,lat,lon,money)
    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
    '''
    try:
        with db.cursor() as cursor:
            cursor.execute(sql,
                           (md5(room.house_detail_url), room.house_detail_url, room.district,
                            room.room_size,
                            room.room_layout, room.room_height, room.room_orientation,
                            room.pay_way,
                            room.leasing_way, room.lat, room.lon, room.money))
    except BaseException as e:
        print(e)
        print('error url --> {}'.format(room.house_detail_url))
    db.commit()


def md5(encode_str):
    m = hashlib.md5()
    m.update(encode_str.encode('gb2312'))
    return m.hexdigest()


def create_room_table():
    sql = '''
    CREATE TABLE `room` (
  `id` varchar(50) NOT NULL,
  `url` text,
  `district` varchar(100) DEFAULT NULL,
  `room_size` int(11) DEFAULT NULL,
  `room_layout` varchar(100) DEFAULT NULL,
  `room_height` varchar(100) DEFAULT NULL,
  `room_orientation` varchar(100) DEFAULT NULL,
  `pay_way` varchar(100) DEFAULT NULL,
  `leasing_way` varchar(100) DEFAULT NULL,
  `lat` float DEFAULT NULL,
  `lon` float DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    '''
    with db.cursor() as cursor:
        cursor.execute(sql)
    db.commit()


if __name__ == '__main__':
    # create_room_table()
    get_zufang_list()
    db.close()
