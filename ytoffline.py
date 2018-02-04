# m-we
# v1.0.1 (2018-01-22)
# ytoffline - Command-line YouTube subscriptions for those looking for privacy.
#             Combined with a VPN, allows you to subscribe to channels without
#             having your data linked to an account or your identity. For the
#             paranoid, there is an option to download the file to your
#             computer to avoid using a browser. Enter "a url" to download
#             audio, "aw url" to download the worst audio. "vw url" and
#             "v url" work similarly, but download both video and audio.
#
#             To add a channel to subs.json, use the channel ID. This is often
#             in the URL (youtube.com/channel/UC123...ABC). If it isn't, go to
#             the channel page, view the page source, and search for
#             channel_id= using CTRL+F.
#
# Requires feedparser, youtube-dl.

import datetime, feedparser, json, time, youtube_dl

feedb = "https://www.youtube.com/feeds/videos.xml?channel_id="
# Set days= to whatever number you want if a week is too much or too little.
# Feedparser returns a limited number of videos, however, so setting days to
# 10000 probably won't return every video a channel has ever uploaded.
db = datetime.datetime.now() - datetime.timedelta(days=7)
bench = int(str(db)[0:10].replace("-", ""))

# Does everything.
def Subs():
    urls = []
    # See example subs.json for formatting. Fairly simple.
    with open("subs.json", "r") as fp:
        subs = json.load(fp)

    vids = []
    for sub in subs:
        # Print all of the initial stuff on the same line to save space.
        print("Retrieving videos from " + sub + ".", end="\t\t\t\t\t\t\t\t\r")
        feed = feedparser.parse(feedb + subs[sub])
        for j in feed["items"]:
            # Get int of publication date and verify it's within the past week.
            draw = j["published_parsed"]
            d = draw.tm_year * 10000 + draw.tm_mon * 100 + draw.tm_mday
            if d >= bench:
                # Append data to a list to be sorted by publication date.
                dat = [
                    j["published_parsed"], sub, j["link"],
                    j["media_thumbnail"][0]["url"], j["title"]
                ]
                vids.append(dat)

    # Sort by published date. Most recent videos are printed last, so less
    # scrolling has to be done to find them. URLs can be copied and pasted
    # from the command line.
    vids = sorted(vids)
    for v in vids:
        d = str(v[0].tm_year) + "-" + str(v[0].tm_mon) + "-" + str(v[0].tm_mday)
        print(v[1] + " - " + v[4] + " - " + d + " - " + v[2])

def Process(cmd):
    if cmd.startswith("aw "):
        fname = "tmp/" + cmd.split("?v=")[1] + ".m4a"
        ydl = youtube_dl.YoutubeDL({"outtmpl": fname,
                                    "format": "worstaudio[ext=m4a]"})
        r = ydl.extract_info(cmd[2:], download=True)
    elif cmd.startswith("a "):
        fname = "tmp/" + cmd.split("?v=")[1] + ".m4a"
        ydl = youtube_dl.YoutubeDL({"outtmpl": fname,
                                    "format": "bestaudio[ext=m4a]"})
        r = ydl.extract_info(cmd[2:], download=True)
    elif cmd.startswith("vw "):
        fname = "tmp/" + cmd.split("?v=")[1] + ".mp4"
        ydl = youtube_dl.YoutubeDL({"outtmpl": fname,
                                    "format": "worstvideo+worstaudio"})
    elif cmd.startswith("v "):
        fname = "tmp/" + cmd.split("?v=")[1] + ".mp4"
        ydl = youtube_dl.YoutubeDL({"outtmpl": fname,
                                    "format": "bestvideo+bestaudio"})

def main():
    Subs()
    print("\n")
    cmd = 0
    while cmd != "":
        cmd = input("> ")
        Process(cmd)

if __name__ == "__main__":
    main()
    input("\n\nPress enter to exit.")
