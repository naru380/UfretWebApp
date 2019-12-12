from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    url = request.POST.get('url')

    if isUfretScoreUrl(str(url)):
        params = get_score_params(url)
    else:
        params = {'noURL': True}

    return render(request, 'sample/sample.html', params)
    #return HttpResponse("Hello World!!")

import re
import requests
from bs4 import BeautifulSoup

LYLICS_AND_CHORDS_CLASS_NAME = 'atfolhyds'
LYLICS_TAG_CLASS_NAME = 'mejiowvnz'
CHORDS_TAG_CLASS_NAME = 'krijcheug'

def isUfretScoreUrl(url):
    if re.match(r'https://www\.ufret\.jp/song\.php\?data=\d+', url):
        return True
    else:
        return False

def get_score_params(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    title = soup.title.text
    song_name = re.match(r'^(.+) / (.+) ギターコード/ウクレレコード/ピアノコード - U-フレット', title).group(1)
    artist_name = re.match(r'^(.+) / (.+) ギターコード/ウクレレコード/ピアノコード - U-フレット', title).group(2)
    print(song_name)
    print(artist_name)
    score_tags = soup.find_all('', class_=[LYLICS_AND_CHORDS_CLASS_NAME, LYLICS_TAG_CLASS_NAME, CHORDS_TAG_CLASS_NAME])

    i = 0
    pair = ['', '']
    score_parts = []
    try:
        for tag in score_tags:
            class_name = tag.get('class')[0]
            text = tag.text
            if class_name == LYLICS_AND_CHORDS_CLASS_NAME:
                score_parts.append(['', text])
                i += 1
            else:
                if class_name == CHORDS_TAG_CLASS_NAME:
                    pair[0] = text
                elif class_name == LYLICS_TAG_CLASS_NAME:
                    pair[1] = text
                    score_parts.append(pair)
                    pair = ['', '']
                    i += 1
                else:
                    raise Exception('unexpected tag.class: {}.'.format(tag.get('class')))
    except Exception as e:
        print(e)
        exit(0)

    params = {
        'song_name': song_name,
        'artist_name': artist_name,
        'score_parts':  score_parts,
    }

    return params
