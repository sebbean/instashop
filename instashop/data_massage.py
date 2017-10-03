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


def word_count_freq(liked_list):
    word_list = list()
    word_count_dict = dict()
    for item in liked_list:
        hashes_tags = liked_list[item]['hashes_tags']
        for each in hashes_tags:
            for word in hashes_tags[each]:
                word_list.append(word)
    print(word_list)
    for item in word_list:
        if item not in word_count_dict:
            word_count_dict[item] = 1
        else:
            word_count_dict[item] += 1

    return word_count_dict
