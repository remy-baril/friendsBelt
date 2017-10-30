# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from .models import *
from ..logReg.models import User
from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages

def index(request):
    user_id = request.session['user_id']
    currentUser = User.objects.get(id=user_id)
    myFriends = currentUser.friended.all()
    otherUsers = User.objects.exclude(id__in = myFriends).exclude(id = currentUser.id)

    context = {
        'currentUser': currentUser,
        'otherUsers': otherUsers,
        'myFriends': myFriends,
        'friendCount': len(myFriends.filter(friended=user_id)),
    }

    return render(request,'friendsApp/index.html', context)

def user(request,friend_id):
    user_id = request.session['user_id']
    user = User.objects.get(id=user_id)
    friend = User.objects.get(id=friend_id)
    data = {
        "user" : user,
        "friend" : friend
    }
    return render(request,'friendsApp/friendPage.html',data)

def addFriend(request,friend_id):
    user_id = request.session['user_id']
    addedFriend = User.objects.addFriend(user_id,friend_id)
    data = {
        "addedFriend": addedFriend
    }
    
    return redirect('/friends/')

def removeFriend(request,friend_id):
    user_id = request.session['user_id']
    removedFriend = User.objects.removeFriend(user_id,friend_id)
    data = {
        "removedFriend": removedFriend
    }
    return redirect('/friends/')

