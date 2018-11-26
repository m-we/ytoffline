import datetime
import json

import feedparser

feedb = 'https://www.youtube.com/feeds/videos.xml?channel_id='
# Set days= to whatever number you want if a week is too much or too little.
# Feedparser returns a limited number of videos, however, so setting days to
# 10000 probably won't return every video a channel has ever uploaded.
db = datetime.datetime.now() - datetime.timedelta(days=7)
bench = int(str(db)[0:10].replace('-', ''))

def Subs():
    urls = []
    with open('subs.json', 'r') as fp:
        subs = json.load(fp)

    vids = []
    for sub in subs:
        print('Retrieving videos from ' + sub, end='\r')
        feed = feedparser.parse(feedb + subs[sub])
        for j in feed['items']:
            # Get int of publication date and verify it's within the past week.
            draw = j['published_parsed']
            d = draw.tm_year * 10000 + draw.tm_mon * 100 + draw.tm_mday
            if d >= bench:
                # Append data to a list to be sorted by publication date.
                dat = [
                    j['published_parsed'], sub, j['link'],
                    j['media_thumbnail'][0]['url'], j['title']
                ]
                vids.append(dat)

    vids = sorted(vids)
    for v in vids:
        d = str(v[0].tm_year) + '-' + str(v[0].tm_mon) + '-' + str(v[0].tm_mday)
        print(v[1] + ' - ' + v[4] + ' - ' + d + ' - ' + v[2])

if __name__ == '__main__':
    Subs()
    input('\n\nPress enter to exit.')
