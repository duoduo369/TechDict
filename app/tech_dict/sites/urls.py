from django.conf.urls import patterns, url

from sites import views

urlpatterns = patterns('',
    url(r'^search$', views.SearchView.as_view()),
)
