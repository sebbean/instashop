from django.http import HttpResponse
import json
import requests

from InstagramAPI.InstagramAPI import InstagramAPI
from instashop import data_massage
from instashop import content_api

def instagram_api(request):
  api = InstagramAPI(request.GET.get('username','yogalola22'), request.GET.get('password','yoga12345'))
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
  items = data_massage.extract_liked_data(api.getTotalLikedMedia(int(request.GET.get('pages','21'))))
  word_list = data_massage.word_count_freq(items)

  return HttpResponse(json.dumps(word_list), content_type='application/json')

def liked_authors(request):
  api = instagram_api(request)
  items = data_massage.extract_liked_data(api.getTotalLikedMedia(int(request.GET.get('pages','21'))))
  author_list = data_massage.extract_liked_authors(items)

  return HttpResponse(json.dumps(author_list), content_type='application/json')

def combined_lists(request):
  api = instagram_api(request)
  items = data_massage.extract_liked_data(api.getTotalLikedMedia(int(request.GET.get('pages','21'))))
  word_list = data_massage.word_count_freq(items)
  author_list = data_massage.extract_liked_authors(items)
  combined_dict = {"popular": word_list, "liked_authors": author_list}

  return HttpResponse(json.dumps(combined_dict), content_type='application/json')

def matched_stories(request):
  api = instagram_api(request)
  items = data_massage.extract_liked_data(api.getTotalLikedMedia(int(request.GET.get('pages','5'))))
  site = int(request.GET.get('site','1'))
  word_list = data_massage.word_count_freq(items)
  author_list = data_massage.extract_liked_authors(items)
  word_matches = content_api.match_content_tags(word_list, site=site)
  author_matches = content_api.match_content_tags(author_list, site=site)
  combined_dict = {"popular": word_matches, "liked_authors": author_matches}
  return HttpResponse(json.dumps(combined_dict), content_type='application/json')

def matched_collections(request):
  api = instagram_api(request)
  items = data_massage.extract_liked_data(api.getTotalLikedMedia(int(request.GET.get('pages','5'))))
  word_list = data_massage.word_count_freq(items)
  author_list = data_massage.extract_liked_authors(items)
  combined_dict = {"popular": content_api.get_collections_with_tags([item[0] for item in word_list]), "liked_authors": content_api.get_collections_with_tags([item[0] for item in author_list])}

  return HttpResponse(json.dumps(combined_dict), content_type='application/json')


