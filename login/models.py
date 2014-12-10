# coding=UTF-8

from django.db import models
from hashlib import sha1
from datetime import datetime

from ino import pidis_killer

"""Maksymalna liczba błędnych logowań"""
max_flogs = 3
"""Czas trwania sesji w sekundach"""
session_timeout = 10000

class User(models.Model):
	username = models.CharField(max_length=50, blank=False)
	password = models.CharField(max_length=50, blank=False)
	active = models.BooleanField(default=False)
	firstname = models.CharField(max_length=50)
	surname = models.CharField(max_length=50)
	email = models.EmailField()
	last_login = models.DateTimeField(default=datetime.now())
	flogs = models.IntegerField(max_length=1, default=0)

	def set_user(self, pwd):
		"""Haszuje hasło i zapisuje tą instancje"""
		self.password = sha1(pwd.encode('utf8')).hexdigest()
		self.save()

	def compare_pass(self, pwd):
		"""Sprawdza czy hasło jest poprawne i zwraca T/F"""
		temp = sha1(pwd.encode('utf8')).hexdigest()
		return self.password == temp

	def can_login(self):
		"""Sprawdza, czy uzytkownik jest aktywny"""
		return self.active

	def login(self, request):
		"""Zapisuje date zalogowania, sprawdza licznik błędnych logowań i kasuje/uniemozliwia logowanie"""
		if not self.active:
			return False
		else:
			global max_flogs
			if self.flogs > max_flogs:
				return False
			else:
				self.flogs = 0
				self.last_login = datetime.now()
				self.save()
				request.session['login'] = True
				request.session['id'] = self.id
				request.session.set_expiry(session_timeout)
				return True

	def logout(self, request):
		pidis_killer()
		request.session.flush()
		request.session['login'] = False
		request.session['id'] = None


	def inc_flogs(self):
		"""Zwiększa licznik złych logowań"""
		self.flogs = self.flogs + 1
		self.save()

	def authUser(self, request):
		if not request.session.get('login', None):
			return False
		else:
			if request.session['login'] == True:
				uid = request.session['id']
				if User.objects.filter(id=uid).exists():
					user = User.objects.get(id=uid)
					if user.can_login():
						return True
					else:
						return False
				else:
					return False
			else:
				return False