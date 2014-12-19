# coding=UTF-8
from os.path import exists

default_params = {
	"path": "/home/matulik/projekty/praca/gedmin/settings/",
	"timeout": "300",
	"pinghost": "google.com",
	"maxflogs": "3",
}


def get_globalparam(param):
	if exists(default_params["path"] + "settings"):
		file = open(default_params["path"] + "settings", "a+").readlines()
		b = False
		if file:
			for i in file:
				if param in i:
					b = True
					return str(i[len(param) + 1:].replace("\n", ""))
			if not b:
				if param in default_params:
					return default_params[param]
			else:
				return None
		else:
			if param in default_params:
				return default_params[param]
			else:
				return None
	else:
		if param in default_params:
			return default_params[param]
		else:
			return None


def set_globalparam(param, value):
	if exists(default_params["path"] + "settings"):
		file = open(default_params["path"] + "settings", "r").readlines()
		b = False
		k = 0
		if file:
			for i in file:
				if param in i:
					b = True
					break
				else:
					k = k + 1
			if b == True:
				file[k] = str(param) + "=" + str(value) + "\n"
				f = ""
				for i in file:
					if i == "\n" or i == "":
						continue
					else:
						f = f + i
				open(default_params["path"] + "settings", "w").write(f)

			if b == False:
				_file = open(default_params["path"] + "settings", "a")
				_file.write("\n" + str(param) + "=" + str(value))

	else:
		file = open(default_params["path"] + "settings", "a")
		file.write(str(param) + "=" + str(value))

