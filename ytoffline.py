import datetime
import re
import urllib.request

def parse(text):
    n = text[text.find('<name>')+6:text.find('</name')]
    pub = []
    title = []
    link = []

    for x in re.findall('(?<=published>).*(?=T)', text):
        pub.append(x)
    for x in re.findall('(?<=title>).*(?=</ti)', text):
        title.append(x)
    for x in re.findall('(?<=href=")https://www.youtube.com/watch.*(?=")', text):
        link.append(x)
    del pub[0]
    del title[0]

    dat = []
    for x in range(len(link)):
        dat.append([pub[x], title[x], link[x], n])
    return dat

def subs():
    feed = 'https://www.youtube.com/feeds/videos.xml?channel_id='
    db = datetime.datetime.now() - datetime.timedelta(days=7)
    bench = int(str(db)[0:10].replace('-', ''))
    
    subs = {}
    with open('subs.txt', 'r') as fp:
        for line in fp:
            u, i = line.replace('\n', '').split('|')
            subs[u] = i

    vids = []
    for sub in subs:
        print('Retrieving videos from ' + sub, end='\r')
        url = feed + subs[sub]
        text = urllib.request.urlopen(url).read().decode()
        dat = parse(text)
        for v in dat:
            vids.append(v)
    vids = sorted(vids)
    for v in vids:
        if int(v[0].replace('-','')) >= bench:
            print(v[3] + ' - ' + v[1] + ', ' + v[0] + ' ' + v[2])

if __name__ == '__main__':
    subs()
    input('\nPress enter to exit.')
