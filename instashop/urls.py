"""instashop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from instashop import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^instagram/following$', views.following),
    url(r'^instagram/liked$', views.liked),
    url(r'^instagram/popular_words$', views.popular_sorted),
    url(r'^instagram/liked_authors$', views.liked_authors),
    url(r'^instagram/combined_lists$', views.combined_lists),
    url(r'^instagram/matches$', views.matches),
    url(r'^instagram/matched_collections$', views.matched_collections)
]
