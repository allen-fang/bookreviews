from __future__ import unicode_literals

from django.db import models
import re
import bcrypt

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
	def register(self, postData):
		errors = []
		# check validations 
		if len(postData['name']) < 2:
			errors.append('First name must at least 2 letters')
		if postData['name'].isdigit():
			errors.append('First name cannot contain numbers')
		if not EMAIL_REGEX.match(postData['email']):
			errors.append('Invalid Email')
		if len(postData['password']) < 8:
			errors.append('Password must be at least 8 charcters')
		if postData['password'] != postData['confirm_pw']:
			errors.append('Passwords do not match!')

		# if no errors, check if email has already been registered, otherwise create new user
		if not errors:
			password = postData['password'].encode()
			hashed = bcrypt.hashpw(password, bcrypt.gensalt())
			if self.filter(email=postData['email']).exists():
				errors.append('Email is already registered.')
				return { 'error': errors }
			else:
				user = self.create(name = postData['name'], alias = postData['alias'], email = postData['email'], hash_pw = hashed)
				return { 'theuser': user }
		else:
			return { 'error': errors }

	def login(self, postData):
		errors = []
		if self.filter(email=postData['email']).exists():
			password = postData['password'].encode('utf-8')
			stored_hashed = User.objects.get(email=postData['email']).hash_pw
			if bcrypt.hashpw(password.encode('utf-8'), stored_hashed.encode()) != stored_hashed:
				print "INCORRECT PASSWORD"
				errors.append('Incorrect password')
			else:
				print "CORRECT PASSWORD"
				user = self.get(email=postData['email'])
		else:
			errors.append('Email is not registered')
	
		if not errors:
			return { 'theuser': user }
		else:
			return { 'error': errors }

# Create your models here.
class User(models.Model):
	name = models.CharField(max_length=255)
	alias = models.CharField(max_length=255)
	email = models.CharField(max_length=255)
	hash_pw = models.CharField(max_length=255)
	objects = UserManager()
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

class Book(models.Model):
	title = models.CharField(max_length=255)
	author = models.CharField(max_length=255)
	reviewed = models.ManyToManyField(User, related_name="reviewed")
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

class Review(models.Model):
	content = models.CharField(max_length=255)
	rating = models.IntegerField()
	user = models.ForeignKey(User)
	book = models.ForeignKey(Book)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)



















