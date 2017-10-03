from django.http import HttpResponse
import json

from InstagramAPI.InstagramAPI import InstagramAPI
from instashop import data_massage

def instagram_api(request):
  api = InstagramAPI(request.GET.get('username','apicard'), request.GET.get('password','Newpassword'))
  api.login()
  return api

def following(request):
  api = instagram_api(request)
  api.getSelfUsersFollowing()
  followings = api.LastJson

  return HttpResponse(json.dumps(followings), content_type='application/json')

def liked(request):
  api = instagram_api(request)
  items = data_massage.extract_liked_data(api.getTotalLikedMedia(int(request.GET.get('pages','1'))))

  return HttpResponse(json.dumps(items), content_type='application/json')

def popular_sorted(request):
  api = instagram_api(request)
  liked_list = data_massage.extract_liked_data(api.getTotalLikedMedia(int(request.GET.get('pages','21'))))
  word_list = data_massage.word_count_freq(liked_list)

  return HttpResponse(json.dumps(word_list), content_type='application/json')

def liked_authors(request):
  api = instagram_api(request)
  items = data_massage.extract_liked_data(api.getTotalLikedMedia(int(request.GET.get('pages','1'))))
  author_list = dict()

  for item in items:
    if item['author_name'] not in author_list:
      author_list[item['author_name']] = 1
    else:
      author_list[item['author_name']] += 1

  return HttpResponse(json.dumps(items), content_type='application/json')
