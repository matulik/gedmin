# coding=UTF-8

from django.shortcuts import render, render_to_response, RequestContext, redirect

from login.models import User

from redis import Redis
from rq import Queue, cancel_job


def main(request):
	user = User()
	if user.authUser(request):
		return render_to_response('info/main.html', context_instance=RequestContext(request))
	else:
		return render_to_response('login/login.html', context_instance=RequestContext(request))


def login(request):
	if request.method == 'POST':
		msg = ""
		username = request.POST['username']
		if User.objects.filter(username=username).exists():
			user = User.objects.get(username=username)
			password = request.POST['password']
			if user.compare_pass(password):
				if user.login(request):
					print "Login ok!"
					return render_to_response('info/main.html', context_instance=RequestContext(request))
				else:
					msg = u"Twoje konto jest nieaktywne. Skontaktuj się z administratorem."
			else:
				msg = u"Podałeś błędny login/hasło. Spróbuj ponownie."
				user.inc_flogs()
		else:
			msg = u"Podałeś błędny login/hasło. Spróbuj ponownie."
		return render_to_response('login/login.html', {'msg': msg}, context_instance=RequestContext(request))
	else:
		print "Its not POST"
		redirect('/')


def logout(request):
	uid = request.session['id']
	if User.objects.filter(id=uid).exists():
		user = User.objects.get(id=uid)
		user.logout(request)
		msg = "Wylogowano."
		return render_to_response('login/errorpage.html', {'msg': msg}, context_instance=RequestContext(request))
	else:
		return render_to_response('login/login.html', context_instance=RequestContext(request))


def errorpage(request):
	return render_to_response('login/errorpage.html', {'msg': msg}, context_instance=RequestContext(request))
