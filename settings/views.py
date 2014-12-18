# coding=UTF-8

from django.shortcuts import render, render_to_response, RequestContext, redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

from os.path import exists

from settings.middleware import set_globalparam, get_globalparam
from login.models import User

user = User()


def main(request):
	if not user.authUser(request):
		msg = u"Nie jesteś zalogowany."
		return render_to_response('login/errorpage.html', {'msg': msg}, context_instance=RequestContext(request))
	else:
		host = get_globalparam("pinghost")
		timeout = get_globalparam("timeout")
		maxflogs = get_globalparam("maxflogs")
		return render_to_response('settings/main.html', {'host': host, 'timeout': timeout, 'maxflogs': maxflogs},
								  context_instance=RequestContext(request))


def changepass(request):
	if not user.authUser(request):
		msg = u"Nie jesteś zalogowany."
		return render_to_response('login/errorpage.html', {'msg': msg}, context_instance=RequestContext(request))
	else:
		us = user.get_user(request)
		return render_to_response('settings/changepass.html', {'username': us.username},
								  context_instance=RequestContext(request))


def updateparams(request):
	if not user.authUser(request):
		msg = u"Nie jesteś zalogowany."
		return render_to_response('login/errorpage.html', {'msg': msg}, context_instance=RequestContext(request))
	else:
		if request.method == "POST":
			val = True
			val_m = True
			val_t = True
			timeout = request.POST["timeout"]
			pinghost = request.POST["pinghost"]
			maxflogs = request.POST["maxflogs"]

			if timeout.isdigit() == False:
				print "tim"
				val_t = False
			if maxflogs.isdigit() == False:
				val_m = False
			if (timeout == "" and maxflogs == "") or (val_t == True and maxflogs == "") or (
					val_m == True and timeout == ""):
				val = True

			if val == True:
				if not timeout == "":
					set_globalparam("timeout", str(timeout))
				if not pinghost == "":
					set_globalparam("pinghost", str(pinghost))
				if not maxflogs == "":
					set_globalparam("maxflogs", str(maxflogs))

				msg = "Dane zostały zaaktualizowane."
				timeout = get_globalparam("timeout")
				pinghost = get_globalparam("pinghost")
				maxflogs = get_globalparam("maxflogs")
				return render_to_response('settings/main.html',
										  {'msg': msg, 'timeout': timeout, 'host': pinghost, 'maxflogs': maxflogs},
										  context_instance=RequestContext(request))
			else:
				msg = "Dane niepoprawne. Spróbuj ponownie."
				timeout = get_globalparam("timeout")
				pinghost = get_globalparam("pinghost")
				maxflogs = get_globalparam("maxflogs")
				return render_to_response('settings/main.html',
										  {'msg': msg, 'timeout': timeout, 'host': pinghost, 'maxflogs': maxflogs},
										  context_instance=RequestContext(request))
		else:
			msg = u"Coś poszło nie tak"
			return render_to_response('login/errorpage.html', {'msg': msg},
									  context_instance=RequestContext(request))


def updatepass(request):
	if not user.authUser(request):
		msg = u"Nie jesteś zalogowany."
		return render_to_response('login/errorpage.html', {'msg': msg}, context_instance=RequestContext(request))
	else:
		if request.method == "POST":
			old = request.POST["oldpass"]
			new = request.POST["newpass"]
			rep = request.POST["reppass"]
			loguser = User.objects.get(id=request.session['id'])
			if loguser.compare_pass(old):
				if new == rep and not new == "":
					loguser.set_user(new)
					msg = u"Hasło zostało zmienione i będzie aktywne przy następnym logowaniu"
				else:
					msg = u"Hasła nie pasują od siebie lub zawierają błędne znaki"
			else:
				msg = u"Podałeś błędne hasło"
			return render_to_response('settings/changepass.html', {'username': loguser.username, 'msg': msg},
									  context_instance=RequestContext(request))

		else:
			msg = u"Coś poszło nie tak"
			return render_to_response('login/errorpage.html', {'msg': msg},
									  context_instance=RequestContext(request))


