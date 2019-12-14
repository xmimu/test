#!/usr/bin/env python3
# -*- coding:utf-8 -*-


import os
import re
import requests


def parse_headers(file):
	data = {}
	with open(file, 'r', encoding="utf-8") as f:
		res = f.readlines()
	for i in res:
		k, v = i.replace('\n', '').split(': ')
		data[k] = v
	return data


def get_rank(headers):
	url = 'https://www.pixiv.net/ranking.php?mode=weekly&content=illust'
	r = requests.get(url, headers=headers)
	html = r.text
	elem = re.findall(r'href="(/artworks/\d+)"', html)
	return elem


def parse_rank(elem, headers):
	for i in elem:
		url = f'https://www.pixiv.net{i}'
		r = requests.get(url, headers=headers)
		html = r.text
		img_title = re.findall(r'<title>(.*?)</title>', html)
		img_url = re.findall(r'"original":"(https://.*?)"}', html)
		save_img(img_title, img_url, headers)


def save_img(img_title, img_url, headers):
	img_url = img_url[0]
	img_title = re.sub(r'[\/:*\?"<>|#]', '', img_title[0])
	file = f'{img_title}.{img_url.split(".")[-1]}'

	folder = './pixiv'
	file_path = os.path.join(folder, file)
	if not os.path.isdir(folder):
		os.mkdir(folder)
	if os.path.isfile(file_path):
		print(f'pass\t{file}')
		return

	r = requests.get(img_url, headers=headers)
	with open(file_path, 'wb') as f:
		f.write(r.content)
	print(f'saved\t{file}')



def main():
	headers = parse_headers('headers.txt')
	elem = get_rank(headers)
	parse_rank(elem, headers)


if __name__ == '__main__':
	main()