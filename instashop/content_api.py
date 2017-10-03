import requests
import json


def match_content_tags(words,site=1):

    if site == 1:
        site = "www.whowhatwear.com"
    elif site == 2:
        site = "www.byrdie.com"
    elif site == 3:
        site = "www.mydomaine.com"
    else:
        site = "www.whowhatwear.com"

    fields = "&fields=id,title,slug,images,authors,updated_at,publish_start,section,is_sponsored,sponsored_text"

    dic = {}
    matches = []
    for t in words:
        w = t[0]
        brands = site + "?tag=brands-" + w + fields
        tags = site + "?tag=tags-" + w + fields
        celebrities = site + "?tag=celebrities-" + w + fields
        r1 = get_article_page(param=brands)
        r2 = get_article_page(param=tags)
        r3 = get_article_page(param=celebrities)
        r1 = get_page_data(r1)
        r2 = get_page_data(r2)
        r3 = get_page_data(r3)
        matches.append(r1)
        matches.append(r2)
        matches.append(r3)
        flat_matches = [item for sublist in matches for item in sublist]
        dic[w] = flat_matches
    return dic


def get_article_page(param=""):
    api = 'http://api.cliqueinc.com'
    content_slug = '/content/posts/'
    url = api + content_slug + param
    return requests.get(url)

def get_page_data(response):
    data = json.loads(response.text)
    return data['docs']


def get_collections_with_tags(tags):
  r = requests.get("https://fapi.cliqueinc.com/collections?rows=1350")
  data = r.json()
  # filtered = [c for c in data if tag in c['title'] or tag in c['description'] ]
  filtered = []
  for c in data:
    for t in tags:
      try:
        if t in c['title'] or t in c['description']:
          filtered.append(c)
      except UnicodeDecodeError:
        print "unicode error"
      except TypeError:
        print "non type error"

  return filtered

