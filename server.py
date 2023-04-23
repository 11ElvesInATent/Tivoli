from ftplib import FTP
import os
import time
from pathlib import Path


ds = '.DS_Store'

pwd = '123'
username = '123'
server_navn = '123'

path_lort = '/Users/gustavnortvig/desktop/tivoli/billeder_raw/'

file_path = Path(path_lort)
fil_emner1 = os.listdir(file_path)
fil_emner1.remove(ds)

file_til = '/public_html/billeder/'

change = []

run = False
delete_everything = True


if run:
	with FTP(server_navn, username, pwd) as ftp:
		for billede in fil_emner1:
			ok = Path(path_lort+billede)
			with open(ok, 'rb') as file:
				ftp.cwd(file_til)
				ftp.storbinary(f'STOR {ok.name}', file)

		while True:
			
			ftp.voidcmd("NOOP")
			fil_emner = os.listdir(file_path)

			if change:
				for billede in change:
					ok = Path(path_lort+billede)
					#sti_oversigt = 
					with open(ok, 'rb') as file:
						ftp.cwd(file_til)
						ftp.storbinary(f'STOR {ok.name}', file)


			time.sleep(1)
			fil_emner_ny = os.listdir(file_path)
			change = list(set(fil_emner_ny)^set(fil_emner))


if delete_everything:
	with FTP(server_navn, username, pwd) as ftp:
		for billede in ftp.nlst(file_til):
			if list(billede)[-1] == 'g': # png eller jpg
				ftp.delete(billede)
		
		