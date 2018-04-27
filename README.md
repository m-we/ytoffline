# ytoffline

ytoffline is a script for those concerned by Google's invasive tracking methods. It allows the user to effectively subscribe to YouTube channels without using a Google account. Add channel names and ids to the subs.json file and run the script to fetch uploads from every channel listed. Uploads are printed in chronological order with title and date information. It's not as pretty as the subscriptions page, but, combined with a VPN, it's a hell of a lot more privacy-friendly.

## Requirements

The only requirement for this script is the feedparser module, which is available through pip.

## Usage

Add channel name and ID to subs.json and double-click ytoffline.py to run. The channel ID is almost always in the URL, but if it isn't, there's a way to locate it. Go to the channel page and right click and select "View page source." Press CTRL+F and type in channel_id= and it will find the channel id. This will be a string of characters that starts with UC. For example, Primitive Technology's YouTube url is https://www.youtube.com/channel/UCAL3JXZSzSm8AlZyD3nQdBA, so the id is UCAL3JXZSzSm8AlZyD3nQdBA.
