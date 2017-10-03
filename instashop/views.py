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
