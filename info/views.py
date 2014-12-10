# coding=UTF-8

from django.shortcuts import render, render_to_response, RequestContext, redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

from login.models import User

from redis import Redis
from rq import Queue, use_connection

from ino import *

redis_conn = Redis()
user = User()


def main(request):
	if not user.authUser(request):
		msg = u"Nie jesteś zalogowany."
		return render_to_response('login/errorpage.html', {'msg': msg}, context_instance=RequestContext(request))
	else:
		pidis_killer()
		redis_servertime()
		return render_to_response('info/main.html', context_instance=RequestContext(request))


def system(request):
	if not user.authUser(request):
		msg = u"Nie jesteś zalogowany."
		return render_to_response('login/errorpage.html', {'msg': msg}, context_instance=RequestContext(request))
	else:
		pidis_killer()
		redis_system()
		return render_to_response('info/system.html', context_instance=RequestContext(request))


def drives(request):
	if not user.authUser(request):
		msg = u"Nie jesteś zalogowany."
		return render_to_response('login/errorpage.html', {'msg': msg}, context_instance=RequestContext(request))
	else:
		pidis_killer()
		redis_drives()
		return render_to_response('info/drives.html', context_instance=RequestContext(request))


def network(request):
	if not user.authUser(request):
		msg = u"Nie jesteś zalogowany."
		return render_to_response('login/errorpage.html', {'msg': msg}, context_instance=RequestContext(request))
	else:
		pidis_killer()
		redis_network()
		return render_to_response('info/network.html', context_instance=RequestContext(request))


# ## AJAX FUNCTIONS ###
@csrf_exempt
def aj_servertime(request):
	if request.is_ajax():
		resp = getServerTime()
		if resp == "running":
			return HttpResponse(resp)
		else:
			return HttpResponse(resp)
	else:
		msg = u"Wejście tutaj nie jest potrzebne"
		return render_to_response('login/errorpage.html', {'msg': msg}, context_instance=RequestContext(request))


@csrf_exempt
def aj_kernelinfo(request):
	if request.is_ajax():
		resp = getKernelInfo()
		if resp == "running":
			return HttpResponse(resp)
		else:
			return HttpResponse(resp)
	else:
		msg = u"Wejście tutaj nie jest potrzebne"
		return render_to_response('login/errorpage.html', {'msg': msg}, context_instance=RequestContext(request))


@csrf_exempt
def aj_serverdate(request):
	if request.is_ajax():
		resp = getServerDate()
		if resp == "running":
			return HttpResponse(resp)
		else:
			return HttpResponse(resp)
	else:
		msg = u"Wejście tutaj nie jest potrzebne"
		return render_to_response('login/errorpage.html', {'msg': msg}, context_instance=RequestContext(request))


@csrf_exempt
def aj_uptime(request):
	if request.is_ajax():
		resp = getUptime()
		if resp == "running":
			return HttpResponse(resp)
		else:
			return HttpResponse(resp)
	else:
		msg = u"Wejście tutaj nie jest potrzebne"
		return render_to_response('login/errorpage.html', {'msg': msg}, context_instance=RequestContext(request))


@csrf_exempt
def aj_hddlist(request):
	if request.is_ajax():
		resp = getDrivesList()
		if resp == "running":
			return HttpResponse(resp)
		else:
			return HttpResponse(resp)
	else:
		msg = u"Wejście tutaj nie jest potrzebne"
		return render_to_response('login/errorpage.html', {'msg': msg}, context_instance=RequestContext(request))


@csrf_exempt
def aj_partlist(request):
	if request.is_ajax():
		resp = getPartitionList()
		if resp == "running":
			return HttpResponse(resp)
		else:
			return HttpResponse(resp)
	else:
		msg = u"Wejście tutaj nie jest potrzebne"
		return render_to_response('login/errorpage.html', {'msg': msg}, context_instance=RequestContext(request))


@csrf_exempt
def aj_hddtemp(request):
	if request.is_ajax():
		resp = getHDDTemps()
		if resp == "running":
			return HttpResponse(resp)
		else:
			return HttpResponse(resp)
	else:
		msg = u"Wejście tutaj nie jest potrzebne"
		return render_to_response('login/errorpage.html', {'msg': msg}, context_instance=RequestContext(request))


@csrf_exempt
def aj_netdevs(request):
	#if request.is_ajax():
	resp = getNetworkDevs()
	if resp == "running":
		return HttpResponse(resp)
	else:
		return HttpResponse(resp)
#	else:
#		msg = u"Wejście tutaj nie jest potrzebne"
#		return render_to_response('login/errorpage.html', {'msg': msg}, context_instance=RequestContext(request))


@csrf_exempt
def aj_localip(request):
	if request.is_ajax():
		resp = getLocalIP()
		if resp == "running":
			return HttpResponse(resp)
		else:
			return HttpResponse(resp)
	else:
		msg = u"Wejście tutaj nie jest potrzebne"
		return render_to_response('login/errorpage.html', {'msg': msg}, context_instance=RequestContext(request))


@csrf_exempt
def aj_globalip(request):
	if request.is_ajax():
		resp = getGlobalIP()
		if resp == "running":
			return HttpResponse(resp)
		else:
			return HttpResponse(resp)
	else:
		msg = u"Wejście tutaj nie jest potrzebne"
		return render_to_response('login/errorpage.html', {'msg': msg}, context_instance=RequestContext(request))


@csrf_exempt
def aj_pinginfo(request):
	if request.is_ajax():
		resp = getPingInfo()
		if resp == "running":
			return HttpResponse(resp)
		else:
			return HttpResponse(resp)
	else:
		msg = u"Wejście tutaj nie jest potrzebne"
		return render_to_response('login/errorpage.html', {'msg': msg}, context_instance=RequestContext(request))


# ## REDIS FUNCTIONS ###
def redis_servertime():
	use_connection(redis_conn)
	q = Queue('high', connection=redis_conn)
	job = q.enqueue(setServerTime)


def redis_system():
	use_connection(redis_conn)
	q = Queue('high', connection=redis_conn)
	job = q.enqueue(setKernelInfo)
	job = q.enqueue(setServerDate)
	job = q.enqueue(setUptime)


def redis_drives():
	use_connection(redis_conn)
	q = Queue('high', connection=redis_conn)
	job = q.enqueue(setDrivesList)
	job = q.enqueue(setPartitionList)
	job = q.enqueue(setHDDTemps)


def redis_network():
	use_connection(redis_conn)
	q = Queue('high', connection=redis_conn)
	job = q.enqueue(setNetworkDevs)
	job = q.enqueue(setLocalIP)
	job = q.enqueue(setGlobalIP)
	job = q.enqueue(setPingInfo, "www.wp.pl", 10)


'''def jobs_killer():
	''''''Funkcjonalnosc przesiona do ino.py -> pidis_killer''''''
	"""Anuluje wszystkie zadania - do wykonania przed wykonaniem nowego widoku"""
	pidis_killer()'''