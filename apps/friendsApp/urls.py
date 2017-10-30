from django.conf.urls import url,include
from . import views

urlpatterns = [
    url(r'^user/(?P<friend_id>\d+)$', views.user),
    url(r'^addFriend/(?P<friend_id>\d+)$', views.addFriend),
    url(r'^removeFriend/(?P<friend_id>\d+)$', views.removeFriend),
    url(r'^$',views.index)
]