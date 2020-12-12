One Python script and one Go script (you only need one) which retrieve videos uploaded by channels listed in subs.txt. It's not as pretty as a subscription page, but the advantage is you don't have to log in (or have a Google account at all) to use it. There is a limit of 15 videos per channel, but if you want older uploads you can change how far back is checked in the script.

Add subs to subs.txt with the format CHANNEL_NAME|CHANNEL_ID, one per line. A channel's ID is a long string of letters, numbers, and symbols starting with UC. It may be in the channel URL (https://www.youtube.com/channel/UCupvZG-5ko_eiXAupbDfxWw). If it isn't, you can Right Click>View Page Source. Press CTRL+F and type channel_id= and copy it from there.

<a href="url"><img src="https://github.com/malcolm-weathers/ytoffline/blob/master/example.jpg?raw=true" align="left" height="400" ></a>
