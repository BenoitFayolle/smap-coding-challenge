from django.conf.urls import url
from django.urls import path
from . import views

urlpatterns = [
    url(r'^$', views.summary),
    url(r'^summary/', views.summary),
    path('detail/<int:id_request>', views.detail, name='detail')
]
