from django.http import HttpResponse
import json

from InstagramAPI.InstagramAPI import InstagramAPI


def following(request):

  api = InstagramAPI("apicard", "Newpassword")
  api.login()
  api.getSelfUsersFollowing()
  followings = api.LastJson

  return HttpResponse(json.dumps(followings), content_type='application/json')

def liked(request):

  api = InstagramAPI("apicard", "Newpassword")
  api.login()

  items = api.getTotalLikedMedia(10)

  return HttpResponse(json.dumps(items), content_type='application/json')
