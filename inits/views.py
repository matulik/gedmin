# coding=UTF-8

from django.shortcuts import render, render_to_response, RequestContext, redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

from login.models import User

from redis import Redis
from rq import Queue, use_connection

from ino import setDeamons, getDeamons, startDeamon, stopDeamon, restartDeamon, getSSRinfo, pidis_killer

user = User()
redis_conn = Redis()
currentDeamon = ""


def main(request):
	if not user.authUser(request):
		msg = u"Nie jesteś zalogowany."
		return render_to_response('login/errorpage.html', {'msg': msg}, context_instance=RequestContext(request))
	else:
		return render_to_response('inits/main.html', context_instance=RequestContext(request))


@csrf_exempt
def startD(request):
	if not user.authUser(request):
		msg = u"Nie jesteś zalogowany."
		return render_to_response('login/errorpage.html', {'msg': msg}, context_instance=RequestContext(request))
	else:
		pidis_killer()
		request.session["deamon"] = request.POST["deamon"]
		redis_startD(request.POST["deamon"])
		info = getSSRinfo(request.POST["deamon"])
		return render_to_response('inits/infowindow.html', {'info': info, 'deamon': request.POST["deamon"]},
								  context_instance=RequestContext(request))


@csrf_exempt
def stopD(request):
	if not user.authUser(request):
		msg = u"Nie jesteś zalogowany."
		return render_to_response('login/errorpage.html', {'msg': msg}, context_instance=RequestContext(request))
	else:
		pidis_killer()
		request.session["deamon"] = request.POST["deamon"]
		redis_stopD(request.POST["deamon"])
		info = getSSRinfo(request.POST["deamon"])
		return render_to_response('inits/infowindow.html', {'info': info, 'deamon': request.POST["deamon"]},
								  context_instance=RequestContext(request))


@csrf_exempt
def restartD(request):
	if not user.authUser(request):
		msg = u"Nie jesteś zalogowany."
		return render_to_response('login/errorpage.html', {'msg': msg}, context_instance=RequestContext(request))
	else:
		pidis_killer()
		request.session["deamon"] = request.POST["deamon"]
		redis_restartD(request.POST["deamon"])
		info = getSSRinfo(request.POST["deamon"])
		return render_to_response('inits/infowindow.html', {'info': info, 'deamon': request.POST["deamon"]},
								  context_instance=RequestContext(request))


# ## AJAX FUNCTIONS ###
@csrf_exempt
def aj_deamons(request):
	if request.is_ajax():
		resp = getDeamons()
		if resp == "running":
			return HttpResponse(resp)
		else:
			redis_deamons()
			return HttpResponse(resp)
	else:
		msg = u"Wejście tutaj nie jest potrzebne"
		return render_to_response('login/errorpage.html', {'msg': msg}, context_instance=RequestContext(request))


@csrf_exempt
def aj_deamonoutput(request):
	if request.is_ajax():
		resp = getSSRinfo(request.session["deamon"])
		return HttpResponse(resp)
	else:
		msg = u"Wejście tutaj nie jest potrzebne"
		return render_to_response('login/errorpage.html', {'msg': msg}, context_instance=RequestContext(request))


# ## REDIS FUNCTIONS ###
def redis_deamons():
	use_connection(redis_conn)
	q = Queue('high', connection=redis_conn)
	job = q.enqueue(setDeamons)


def redis_startD(name):
	use_connection(redis_conn)
	q = Queue('high', connection=redis_conn)
	job = q.enqueue(startDeamon, str(name))


def redis_stopD(name):
	use_connection(redis_conn)
	q = Queue('high', connection=redis_conn)
	job = q.enqueue(stopDeamon, str(name))


def redis_restartD(name):
	use_connection(redis_conn)
	q = Queue('high', connection=redis_conn)
	job = q.enqueue(restartDeamon, str(name))