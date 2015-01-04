# coding=UTF-8

from django.shortcuts import render, render_to_response, RequestContext, redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

from login.models import User

from settings.middleware import get_logfiles, get_globalparam
from ino import get_file

user = User()


def main(request):
	if not user.authUser(request):
		msg = u"Nie jesteś zalogowany."
		return render_to_response('login/errorpage.html', {'msg': msg}, context_instance=RequestContext(request))
	else:
		files = get_logfiles()
		contents = []
		tail = get_globalparam("tail")
		for f in files:
			file = get_file(f, tail)
			if file:
				contents.append(file)
			else:
				contents.append("Brak dostępu. Sprawdź uprawnienia do pliku.")
		numbers = []
		for i in range(0, len(files)):
			numbers.append(i)
		list = zip(numbers, files, contents)
		return render_to_response('logs/main.html', {'list': list, 'tail': tail},
								  context_instance=RequestContext(request))


