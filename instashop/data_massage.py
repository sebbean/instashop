import re


def extract_liked_data(raw_data):
    liked_list = dict()

    for item in raw_data:
        try:
            id = item['id']
            like_count = item['like_count']
            caption = item['caption']['text'].encode('utf-8')
            hashes_tags = extract_hashes_tags(caption)
            image_url = item['image_versions2']['candidates'][0]['url']
            if id not in liked_list:
                liked_list[id] = {'like_count': like_count, 'caption': caption, 'image_url': image_url, 'hashes_tags': hashes_tags}
        except TypeError:
            pass
        except KeyError:
            pass

    return liked_list


def extract_hashes_tags(caption):
    hash_pattern = '(?<=#).*?(?=\s)'
    hash_regex = re.compile(hash_pattern)

    results_dict = dict()

    tag_pattern = '(?<=@).*?(?=\s)'
    tag_regex = re.compile(tag_pattern)

    hashes = re.findall(hash_regex, caption)
    tags = re.findall(tag_regex, caption)

    results_dict.update({"hashes": hashes, "tags": tags})

    return results_dict