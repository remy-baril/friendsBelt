from __future__ import unicode_literals
from django.db import models
import bcrypt, re
from datetime import datetime
from time import strftime,localtime

EMAIL_REGEX = re.compile (r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    def login(self,post):
        email = post['log_email'].lower()
        users = self.filter(email = email)
        if users:
            user = users[0]
            if bcrypt.checkpw(post['log_password'].encode(),user.password.encode()):
                return user
        return False

    def regValidation(self, post):
        name = post['name']
        alias = post['alias']
        email = post['reg_email'].lower()
        password = post['reg_password']
        cpass = post['cpass']

        errors = []

        ##CHECK MOST STRICT VALS FIRST

        ## first name vals
        if len(name) < 1:
            errors.append('Must enter name')
        elif len(name) < 2:
            errors.append('First name must be at least 2 letters')

        ## last name vals
        if len(alias) < 1:
            errors.append('Must enter alias')
        elif len(alias) < 2:
            errors.append('Last name must be at least 2 letters')

        ## email vals
        if len(email) < 1:
            errors.append('Must enter email')
        elif not EMAIL_REGEX.match(email):
            errors.append('Email is not in valid format')

        ## password vals
        if len(password) < 8:
            errors.append('Password must be at least 8 characters')
        elif password != cpass:
            errors.append('Passwords must match')

        ## checks whether email has already been registered 
        if not errors:
            users = self.filter(email=email)
            if users:
                errors.append('This email has already been registered')

        return {'status': len(errors) == 0, 'errors':errors} #this says return a dictionary of the "errors" array and a status. If the length of arrays is 0

    def createUser(self,post):
        name = post['name']
        alias = post['alias']
        email = post['reg_email'].lower()
        password = bcrypt.hashpw(post['reg_password'].encode(), bcrypt.gensalt())
        return self.create(name = name, email = email, alias = alias, password = password)
        ## ^ puts into in database query 'create' and enters everything into database

    def addFriend(self,user_id,friend_id):
        user = User.objects.get(id=user_id)
        friend = User.objects.get(id=friend_id)
        user.friended.add(friend)
        return friend
    
    def removeFriend(self,user_id,friend_id):
        user = User.objects.get(id=user_id)
        friend = User.objects.get(id=friend_id)
        user.friended.remove(friend)
        return friend

class User(models.Model):
    name = models.CharField(max_length = 255)
    alias = models.CharField(max_length = 255)
    email = models.CharField(max_length = 255)
    password = models.CharField(max_length = 255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    friended = models.ManyToManyField('self', related_name = 'friended_by')

    objects = UserManager() ##connects an instance of UserManager to User model overwriting hidden objects key w new one

    def __str__(self):
        return 'Name: {} {}, Email: {}'.format(self.name,self.alias,self.email)



