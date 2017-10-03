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
        recent_post = recent_post[0:5]
    print("updated len:{}".format(len(recent_post)))
    return recent_post

if __name__ == "__main__":
    atags = [
        [
        "stylesightworldwide",
        26
        ],
        [
        "alwaysjudging",
        14
        ],
        [
        "songofstyle",
        11
        ],
        [
        "fhlurs",
        9
        ],
        [
        "nytimesfashion",
        7
        ]
    ]

    tags = [
        [
        "would",
        30
        ],
        [
        "fashionweek",
        29
        ],
        [
        "streetfashion",
        27
        ],
        [
        "blogger",
        27
        ],
        [
        "streetstyle",
        27
        ],
        [
        "ss18",
        22
        ],
        [
        "londonfashionweek",
        22
        ]
    ]

    t =  [[
        "walk",
        22
        ]]

    match_content_tags(tags)
    # get_stop_words()
