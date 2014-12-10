#!/usr/bin/env python

import subprocess, os, time
from urllib import urlopen

from redis import Redis
from rq import Queue, use_connection, cancel_job

path = "/home/matulik/projekty/praca/gedmin/scripts/"


# ##Sets function - sets data to files ###
# ##Get function - gets date from files only if process isn't running ###

# pidArchive function keeps list of PIDs of all commands. 
# It's will be useful in the future to kills zombie processes

def pidArchive(pid):
	file = open(path + "temp/pidArchive", "a")
	file.write(str(pid) + "\n")
	file.close


def killZombies():
	file = open(path + "temp/pidArchive", "r")
	for i in file:
		if i == "" or i == "\n":
			continue
		else:
			cmd = 'sudo kill -9 ' + str(i)
			ret = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
			(output, err) = ret.communicate()
			print output
	file = open(path + "temp/pidArchive", "w")
	file.write("")
	file.close()


def pidis_killer():
	redis_conn = Redis()
	use_connection(redis_conn)
	q = Queue('high', connection=redis_conn)
	q.empty()
	jobs = q.job_ids
	for j in jobs:
		cancel_job(j)
	killZombies()


## SERVER TIME ##
def setServerTime():
	cmd = path + 'lives.sh servertime'
	ret = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
	open(path + "temp/ServerTimePid", "w").write(str(ret.pid))
	pidArchive(ret.pid)
	(output, err) = ret.communicate()
	open(path + "temp/ServerTimeOut", "w").write(str(output))


def getServerTime():
	#pid = open(path+"temp/ServerTimePid","r").read()
	#if os.path.exists("/proc/"+pid):
	#	return "running"
	#else:
	return open(path + "temp/ServerTimeOut", "r").read()


## KERNEL INFO ##
def setKernelInfo():
	open(path + "temp/KernelInfoOut", "w").write("running")
	ret = subprocess.Popen(["uname", "-r"], stdout=subprocess.PIPE)
	open(path + "temp/KernelInfoPid", "w").write(str(ret.pid))
	pidArchive(ret.pid)
	(output, err) = ret.communicate()
	open(path + "temp/KernelInfoOut", "w").write(str(output))


def getKernelInfo():
	pid = open(path + "temp/KernelInfoPid", "r").read()
	if os.path.exists("/proc/" + pid):
		return "running"
	else:
		return open(path + "temp/KernelInfoOut", "r").read()


## SERVER DATE ##
def setServerDate():
	open(path + "temp/ServerDateOut", "w").write("running")
	ret = subprocess.Popen(["date"], stdout=subprocess.PIPE)
	open(path + "temp/ServerDatePid", "w").write(str(ret.pid))
	pidArchive(ret.pid)
	(output, err) = ret.communicate()
	open(path + "temp/ServerDateOut", "w").write(str(output))


def getServerDate():
	pid = open(path + "temp/ServerDatePid", "r").read()
	if os.path.exists("/proc/" + pid):
		return "running"
	else:
		return open(path + "temp/ServerDateOut", "r").read()


## UPTIME ##
def setUptime():
	open(path + "temp/UptimeOut", "w").write("running")
	ret = subprocess.Popen(["uptime", "-p"], stdout=subprocess.PIPE)
	open(path + "temp/UptimePid", "w").write(str(ret.pid))
	pidArchive(ret.pid)
	(output, err) = ret.communicate()
	open(path + "temp/UptimeOut", "w").write(str(output))


def getUptime():
	pid = open(path + "temp/UptimePid", "r").read()
	if os.path.exists("/proc/" + pid):
		return "running"
	else:
		return open(path + "temp/UptimeOut", "r").read()


## DRIVE LIST ##
def setDrivesList():
	open(path + "temp/DrivesListOut", "w").write("running")
	ret = subprocess.Popen(["lsblk", "-S"], stdout=subprocess.PIPE)
	open(path + "temp/DrivesListPid", "w").write(str(ret.pid))
	pidArchive(ret.pid)
	(output, err) = ret.communicate()
	open(path + "temp/DrivesListOut", "w").write(str(output))


def getDrivesList():
	pid = open(path + "temp/DrivesListPid", "r").read()
	if os.path.exists("/proc/" + pid):
		return "running"
	else:
		r = open(path + "temp/DrivesListOut", "r").readlines()
		ret = ''
		for i in range(1, len(r)):
			ret = ret + r[i]
		return ret


## PARTITION LIST ##
def setPartitionList():
	open(path + "temp/PartitionListOut", "w").write("running")
	ret = subprocess.Popen(["lsblk"], stdout=subprocess.PIPE)
	open(path + "temp/PartitionListPid", "w").write(str(ret.pid))
	pidArchive(ret.pid)
	(output, err) = ret.communicate()
	open(path + "temp/PartitionListOut", "w").write(str(output))


def getPartitionList():
	pid = open(path + "temp/PartitionListPid", "r").read()
	if os.path.exists("/proc/" + pid):
		return "running"
	else:
		return open(path + "temp/PartitionListOut", "r").read()


## HDDTEMPS ##
def setHDDTemps():
	open(path + "temp/HDDTempsOut", "w").write("running")
	ret = subprocess.Popen(["lsblk", "-S", "-o", "NAME"], stdout=subprocess.PIPE)
	open(path + "temp/HDDTempsPid", "w").write(str(ret.pid))
	pidArchive(ret.pid)
	(output, err) = ret.communicate()
	open(path + "temp/HDDTempsOut", "w").write(str(output))
	_setHDDTemps()


def _setHDDTemps():
	pid = open(path + "temp/HDDTempsPid", "r").read()
	if os.path.exists("/proc/" + pid):
		return "running"
	else:
		lines = open(path + "temp/HDDTempsOut", "r").readlines()
		hdlist = []
		for line in range(1, len(lines)):
			if "sd" in lines[line]:
				hdlist.append(lines[line])
			if "hd" in lines[line]:
				hdlist.append(lines[line])
	rets = []
	for i in hdlist:
		cmd = "sudo hddtemp -n " + "/dev/" + str(i).replace("\n", "")
		ret = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
		#ret = subprocess.Popen(["hddtemp", "-n", "/dev/"+str(i).replace("\n","")], stdout=subprocess.PIPE)
		open(path + "temp/_HDDTempsPid", "a").write(str(ret.pid))
		pidArchive(ret.pid)
		(output, err) = ret.communicate()
		rets.append(output)
	file = open(path + "temp/_HDDTempsOut", "w")
	file.write("")
	for i in range(0, len(hdlist)):
		wr = hdlist[i] + " - " + rets[i]
		file.write(str(wr).replace("\n", "") + "\n")
	#open(path+"temp/_HDDTempsOut","a").write(str(wr).replace("\n",""))
	file.close()


def getHDDTemps():
	pid = open(path + "temp/_HDDTempsPid", "r").read()
	if os.path.exists("/proc/" + pid):
		return "running"
	else:
		return open(path + "temp/_HDDTempsOut", "r").read()


## PING ##
def setPingInfo(url, count):
	open(path + "temp/PingOut", "w").write("running")
	cmd = "ping -c " + str(count) + " " + str(url)
	print cmd
	ret = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
	#ret = subprocess.Popen(["ping", "-c 3", "wp.pl"], stdout=subprocess.PIPE)
	open(path + "temp/PingPid", "w").write(str(ret.pid))
	pidArchive(ret.pid)
	(output, err) = ret.communicate()
	file = []
	n = 0
	for i in range(0, len(output)):
		if output[i] == "\n":
			file.append(output[n:i])
			n = i
	_file = file[len(file) - 3:len(file)]
	ret = ""
	for i in _file:
		ret = ret + str(i)
	open(path + "temp/PingOut", "w").write(str(ret))


def getPingInfo():
	pid = open(path + "temp/PingPid", "r").read()
	if os.path.exists("/proc/" + pid):
		return "running"
	else:
		return open(path + "temp/PingOut", "r").read()


## NETWORK DEVS ##
def setNetworkDevs():
	open(path + "temp/NetworkDevsOut", "w").write("running")
	cmd = "sudo lspci | egrep -i --color \'network|ethernet\'"
	ret = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
	open(path + "temp/NetworkDevsPid", "w").write(str(ret.pid))
	pidArchive(ret.pid)
	(output, err) = ret.communicate()
	open(path + "temp/NetworkDevsOut", "w").write(str(output))


def getNetworkDevs():
	pid = open(path + "temp/NetworkDevsPid", "r").read()
	if os.path.exists("/proc/" + pid):
		return "running"
	else:
		return open(path + "temp/NetworkDevsOut", "r").read()


## LOCAL IP ##
def setLocalIP():
	open(path + "temp/LocalIPOut", "w").write("running")
	cmd = "ifconfig | grep -Eo \'inet (addr:)?([0-9]*\.){3}[0-9]*\' | grep -Eo \'([0-9]*\.){3}[0-9]*\' | grep -v \'127.0.0.1\'"
	ret = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
	open(path + "temp/LocalIPPid", "w").write(str(ret.pid))
	pidArchive(ret.pid)
	(output, err) = ret.communicate()
	open(path + "temp/LocalIPOut", "w").write(str(output))


def getLocalIP():
	pid = open(path + "temp/LocalIPPid", "r").read()
	if os.path.exists("/proc/" + pid):
		return "running"
	else:
		return open(path + "temp/LocalIPOut", "r").read()


## GLOBAL IP ##
def setGlobalIP():
	open(path + "temp/GlobalIPOut", "w").write("running")
	ip = urlopen("http://ipecho.net/plain")
	open(path + "temp/GlobalIPOut", "w").write(str(ip.read()))


def getGlobalIP():
	f = open(path + "temp/GlobalIPOut", "r").read()
	if f == "running":
		return "running"
	else:
		return f


## PROC INFO ##
def setProcInfo():
	open(path + "temp/ProcOut", "w").write("running")
	cmd = "cat /proc/cpuinfo | grep 'model name' | tail -n 1"
	ret = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
	open(path + "temp/ProcPid", "w").write(str(ret.pid))
	pidArchive(ret.pid)
	(output, err) = ret.communicate()
	p = output
	for i in range(0, len(output)):
		if output[i] == ':':
			break
	open(path + "temp/ProcOut", "w").write(str(output[i + 1:]))


def getProcInfo():
	pid = open(path + "temp/ProcPid", "r").read()
	if os.path.exists("/proc/" + pid):
		return "running"
	else:
		return open(path + "temp/ProcOut", "r").read()


## MHz NOW ##
### TODO NHZ LIVEBAR ###
def setMHzInfo():
	open(path + "temp/MHzInfoOut", "w").write("running")
	cmd = "cat /proc/cpuinfo | grep MHz"
	ret = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
	open(path + "temp/MHzInfoPid", "w").write(str(ret.pid))
	(output, err) = ret.communicate()
	mhzs = []
	temp = ""
	for i in output:
		if i == "\n":
			mhzs.append(temp)
			temp = ""
		else:
			temp = temp + i;
	temp = 0
	for i in range(0, len(mhzs[0])):
		if mhzs[0][i] == ":":
			temp = i
			break
	mhzs_n = []
	for i in mhzs:
		mhzs_n.append(i[temp + 1:])
	f = open(path + "temp/MHzInfoOut", "w")
	for i in mhzs_n:
		f.write(str(i) + "\n")


def getMHzInfo():
	### TODO MHZ LIVBAR GET ###
	pid = open(path + "temp/MHzInfoPid", "r").read()
	if os.path.exists("/proc/" + pid):
		return "running"
	else:
		return open(path + "temp/MHzInfoOut", "r").read()

