# m-we
# v1.0.0
# ytoffline - Command-line YouTube subscriptions without an account. Created
#             for the privacy-conscious. This doesn't prevent Google/YouTube
#             from tracking you, but it does make it slightly more difficult
#             by not having all the data nice and bundled up with an account.
#             For those with a VPN, this lets you effectively subscribe to
#             channels anonymously.
#
#             Channels are stored in subs.json, the format you can see there.
#             Some channels will have the channel_id in the URL. It's usually
#             a long string of letters and numbers starting with UC. For
#             channels that don't, right click and select "View Page Source".
#             Use Ctrl+F to search for "channel_id=" and copy the string
#             from there.
#
# Requires feedparser (pip install feedparser).

import datetime, feedparser, json

feedb = "https://www.youtube.com/feeds/videos.xml?channel_id="
# Set days= to whatever number you want if a week is too much or too little.
# Feedparser returns a limited number of videos, however, so setting days to
# 10000 probably won't return every video a channel has ever uploaded.
db = datetime.datetime.now() - datetime.timedelta(days=7)
bench = int(str(db)[0:10].replace("-", ""))

# Does everything.
def main():
    urls = []
    # See example subs.json for formatting. Fairly simple.
    with open("subs.json", "r") as fp:
        subs = json.load(fp)

    vids = []
    for sub in subs:
        # Print all of the initial stuff on the same line to save space.
        print("Retrieving videos from " + sub + ".", end="\t\t\t\t\t\t\t\t\r")
        feed = feedparser.parse(feedb + subs[sub]["id"])
        for j in feed["items"]:
            # Get int of publication date and verify it's within the past week.
            draw = j["published_parsed"]
            d = draw.tm_year * 10000 + draw.tm_mon * 100 + draw.tm_mday
            if d >= bench:
                # Append data to a list to be sorted by publication date.
                dat = [
                    j["published_parsed"],
                    sub,
                    j["link"],
                    j["media_thumbnail"][0]["url"],
                    j["title"]
                ]
                vids.append(dat)

    # Sort by published date. Most recent videos are printed last, so less
    # scrolling has to be done to find them. URLs can be copied and pasted
    # from the command line.
    vids = sorted(vids)
    for v in vids:
        d = str(v[0].tm_year) + "-" + str(v[0].tm_mon) + "-" + str(v[0].tm_mday)
        print(v[1] + " - " + v[4] + " - " + d + " - " + v[2])

if __name__ == '__main__':
    main()
    input("\n\nPress enter to exit.")
