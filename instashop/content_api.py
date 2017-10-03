import requests
import json
from datetime import datetime, timedelta


def match_content_tags(words):

    stopwords = get_stop_words()
    
    sites = ["www.whowhatwear.com","www.byrdie.com","www.mydomaine.com"]
    
    fields = "&fields=id,title,slug,images,authors,updated_at,publish_start,section,is_sponsored,sponsored_text"

    dic = {}
    matches = []
    for t in words:
        w = t[0]
        d = {}
        if w in stopwords:
            continue
        for site in sites:
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
            most_recent = keep_recent(flat_matches)
            d.update({site : most_recent})
        dic[w] = d
    print(dic)
    return dic


def get_article_page(param=""):
    api = 'http://api.cliqueinc.com'
    content_slug = '/content/posts/'
    url = api + content_slug + param
    return requests.get(url)

def get_page_data(response):
    data = json.loads(response.text)
    return data['docs']

def get_stop_words():
    with open('stopwords.json') as json_data:
        stopwords = json.load(json_data)
        json_data.close()
    return stopwords

def keep_recent(posts):
    print("original len:{}".format(len(posts)))
    recent_post = posts
    today = datetime.today()
    delta = timedelta(days=30)
    if len(posts)>5:
        for p in posts:
            date = p.get('publish_start')
            date = date[0:10]
            date = datetime.strptime(date,"%Y-%m-%d")
            if today - date > delta:
                recent_post.remove(p)
        if len(recent_post) > 5:
            recent_post = recent_post[0:5]
    print("updated len:{}".format(len(recent_post)))
    return recent_post

def get_collections_with_tags(tags):
  r = requests.get("https://fapi.cliqueinc.com/collections?rows=1350")
  data = r.json()
  # filtered = [c for c in data if tag in c['title'] or tag in c['description'] ]
  filtered = []
  stopwords = get_stop_words()


  for c in data:
    for t in tags:
      if t in stopwords:
          continue
      try:
        if t.lower() in c['title'].lower() or t.lower() in c['description'].lower():
          c['match'] = t
          filtered.append(c)
      except UnicodeDecodeError:
        print "unicode error"
      except TypeError:
        print "non type error"
      except AttributeError:
        print "attr error"

  return filtered
