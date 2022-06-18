## mediaInfoWatch
### a Snaz "playing now" replacement working with native Windows media controls

<br>
This Windows tool allows you to extract the title, artist and thumbnail of your music playing. 

Useful for Twitch/Youtube streamers.

Works with the native Windows media features.
So if you click on your "speakers" icon on the Windows Bar, and see a media control bar like below, you're good to go. 

<img src="img/example_audio_session.png" alt="example audio bar playing" width="200"/>

works well with:
- Spotify
- Firefox

Works more or less with: 
- Windows 11 new Media Player

### usage:

```
pip install requirements.txt
python mediaInfoWatch.py
```

you can change the folder where the infos are stored by passing it as argument like this:
`python mediaInfoWatch.py FolferName`

at each new music it will create/change 2 files: 
- *media_thumb.jpg*
- *music_info.txt*

up to you to create a file watcher/ integrate it with your usage (stream, video game...)

### todo:
 - have a folder picker that doesn't make the program halt forever
 - make the program more customizable like Snaz (extract more info, more customization)
 - optimize it more, if doable and useful.
 - have devs of music players use this `SystemMediaTransportControls`/`MediaSession` API to make this program more useful.

issues/ pull requests welcome