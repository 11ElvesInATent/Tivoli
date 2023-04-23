#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import time
import pychromecast
from PIL import Image, ImageFont, ImageDraw
import random
from ftplib import FTP
from pathlib import Path

#device_friendly_name = "den gule lort"
device_friendly_name = 'Living Room TV'

path_tivoli = '/Users/gustavnortvig/desktop/tivoli/billeder/' # kilde til tom mappe som bliver fyldt med billeder MED stand-info
path_lort = '/Users/gustavnortvig/desktop/tivoli/billeder_uden_lort/' # sammen som ovenfor, bare uden stand-info (rene billeder)
path_desk_tivoli = '/Desktop/tivoli/billeder/'
ip_adress = '192.168.1.15'

file_til = '/public_html/billeder/'


max_length = 3
sov = 10 # sek mellem billeder
ds = '.DS_Store'

chromecasts = pychromecast.get_chromecasts()
print([cc.device.friendly_name for cc in chromecasts])
cast = next(cc for cc in chromecasts if cc.device.friendly_name == "Living Room TV")



#chromecasts, browser = pychromecast.get_listed_chromecasts(friendly_names=[device_friendly_name])	



cast.wait()


#cast = chromecasts[0]

#print(cast.cast_info.friendly_name)
mc = cast.media_controller

run = 0


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
	Im = x.resize((100,100))
	Im.save(til)
	
	#img = Image.open(fra)

	#img = img.transpose(Image.ROTATE_90)

	#img = img.resize((1000,100), Image.LANCZOS)
	'''
	width, height = img.size

	newsize = (width, int(height*black_space))

	new_img = Image.new("RGB", newsize, (153,24,24))
	new_img.paste(img, (0, 0))


	draw = ImageDraw.Draw(new_img)
	font = ImageFont.truetype("Algerian_Regular.ttf", 25)
	draw.text((width*0.1, height*1.02),"Kom til fotoboden på 160",(255,255,255),font=font)
	'''
	#img.save(til)


kevin = os.listdir(path_lort)
kevin.remove(ds)

for bil in kevin:
	fra = path_lort+bil
	til = path_tivoli+bil

	tegning(fra,til)



while run < 5:

	run += 1

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

	
#pychromecast.discovery.stop_discovery(browser)
mc.block_until_active()