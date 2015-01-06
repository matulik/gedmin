# coding=UTF-8

from django.shortcuts import render, render_to_response, RequestContext, redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

from login.models import User

from ino import set_portageSync, set_portageSyncNothing, get_portageSync, set_portageUpd, set_portageUpdNothing, \
	get_portageUpd, pidis_killer

from redis import Redis
from rq import Queue, use_connection

redis_conn = Redis()
user = User()


def main(request):
	if not user.authUser(request):
		msg = u"Nie jesteś zalogowany."
		return render_to_response('login/errorpage.html', {'msg': msg}, context_instance=RequestContext(request))
	else:
		pidis_killer()
		set_portageSyncNothing()
		set_portageUpdNothing()
		return render_to_response('portmin/main.html', context_instance=RequestContext(request))


def confiles(request):
	if not user.authUser(request):
		msg = u"Nie jesteś zalogowany."
		return render_to_response('login/errorpage.html', {'msg': msg}, context_instance=RequestContext(request))
	else:
		files = ["make.conf", "package.keywords", "package.license", "package.mask", "package.unmask", "package.use"]
		path = "/etc/portage/"
		contents = [];
		for f in files:
			if f:
				contents.append(open(path + f, "r").read())
			else:
				contents.append("Brak dostępu do pliku lub plik nie istnieje.")
		numbers = []
		for i in range(0, len(files)):
			numbers.append(i)
		list = zip(numbers, files, contents)
		return render_to_response('portmin/confiles.html', {'list': list}, context_instance=RequestContext(request))


# ## AJAX FUNCTIONS ###
@csrf_exempt
def aj_sync(request):
	if request.is_ajax():
		resp = get_portageSync()
		if resp == "running":
			return HttpResponse(resp)
		elif resp == "nothing":
			return HttpResponse(resp)
		else:
			return HttpResponse(resp)
	else:
		msg = u"Wejście tutaj nie jest potrzebne"
		return render_to_response('login/errorpage.html', {'msg': msg}, context_instance=RequestContext(request))


@csrf_exempt
def aj_setsync(request):
	if request.is_ajax():
		redis_sync()
		return HttpResponse("I ran it!")
	else:
		msg = u"Wejście tutaj nie jest potrzebne"
		return render_to_response('login/errorpage.html', {'msg': msg}, context_instance=RequestContext(request))


@csrf_exempt
def aj_upd(request):
	if request.is_ajax():
		resp = get_portageUpd()
		if resp == "running":
			return HttpResponse(resp)
		elif resp == "nothing":
			return HttpResponse(resp)
		else:
			return HttpResponse(resp)
	else:
		msg = u"Wejście tutaj nie jest potrzebne"
		return render_to_response('login/errorpage.html', {'msg': msg}, context_instance=RequestContext(request))


@csrf_exempt
def aj_setupd(request):
	if request.is_ajax():
		redis_upd()
		return HttpResponse("I ran it!")
	else:
		msg = u"Wejście tutaj nie jest potrzebne"
		return render_to_response('login/errorpage.html', {'msg': msg}, context_instance=RequestContext(request))


# ## REDIS FUNCTION

def redis_sync():
	use_connection(redis_conn)
	q = Queue('high', connection=redis_conn)
	job = q.enqueue(set_portageSync)


def redis_upd():
	use_connection(redis_conn)
	q = Queue('high', connection=redis_conn)
	job = q.enqueue(set_portageUpd)

