#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import time
import pychromecast
from PIL import Image, ImageFont, ImageDraw
import random
from ftplib import FTP
from pathlib import Path

device_friendly_name = 'Living Room TV'

path_tivoli = '/Users/gustavnortvig/desktop/tivoli/billeder_new/' # kilde til tom mappe som bliver fyldt med billeder MED stand-info
path_lort = '/Users/gustavnortvig/desktop/tivoli/billeder_raw/' # sammen som ovenfor, bare uden stand-info (rene billeder)
path_desk_tivoli = '/Desktop/tivoli/billeder/'
ip_adress = '999'

file_til = '/public_html/billeder/'

sov = 10 # sek mellem billeder
ds = '.DS_Store'

chromecasts = pychromecast.get_chromecasts()
print([cc.device.friendly_name for cc in chromecasts])
cast = next(cc for cc in chromecasts if cc.device.friendly_name == device_friendly_name)

cast.wait()

mc = cast.media_controller


def updater(billede = None):
	fil_tivoli = os.listdir(path_lort)

	if billede != ds: 
		mc.play_media("http://"+ip_adress+":8000"+path_desk_tivoli+billede, content_type = 'image/png')
		mc.block_until_active()
		mc.pause()
		mc.play()

	change = []

	t0 = time.perf_counter()
	t1 = t0

	while t1 - t0 < sov:
		t1 = time.perf_counter()
		
		fil_tivoli_ny = os.listdir(path_lort)
		time.sleep(0.1)

		f = set(fil_tivoli_ny)^set(fil_tivoli)
		g = [bb for bb in f if bb not in change]
		
		for bb in g:
			change.append(bb)


	if len(change) > max_length:

		slettes = change[max_length:len(change)]
		for name in slettes:
			os.system('rm '+path_lort+name)

		change = change[0:max_length]

	return(change)


def tegning(fra,til):
	x = Image.open(fra)
	Im = x.resize((750,500))
	Im.save(til)


kevin = os.listdir(path_lort)
kevin.remove(ds)

for bil in kevin:
	fra = path_lort+bil
	til = path_tivoli+bil

	tegning(fra,til)



while True:
	fil_tivoli = os.listdir(path_tivoli)
	fil_tivoli.remove(ds)
	print(fil_tivoli)

	random_name = fil_tivoli[random.randint(0,len(fil_tivoli)-1)]
	print('det aktive billede: '+random_name)
	talley = updater(random_name)
	
	print('talley: ',talley)
	
	while talley: # der er nye billeder
		t0 = talley[0]
		os.listdir(path_lort).remove(ds)
		fra = path_lort+t0
		til = path_tivoli+t0
		tegning(fra,til)

		print('det aktive billede1: ', t0)
		q = updater(t0)
		talley.pop(0)
		talley.extend(q)
		print('talley1: ',talley)
		
