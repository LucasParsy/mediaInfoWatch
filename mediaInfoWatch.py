import asyncio
import time
import shutil
import filecmp
import sys
import os
from pathlib import Path
# import tkinter as tk
# from tkinter import filedialog


from winsdk.windows.media.control import \
    GlobalSystemMediaTransportControlsSessionManager as MediaManager

from winsdk.windows.storage.streams import \
    DataReader, Buffer, InputStreamOptions

async def read_stream_into_buffer(stream_ref, buffer):
    readable_stream = await stream_ref.open_read_async()
    readable_stream.read_async(buffer, buffer.capacity, InputStreamOptions.READ_AHEAD)


def write_thumbnail(current_media_info, thumbnail_path):
    # create the current_media_info dict with the earlier code first
    thumb_stream_ref = current_media_info['thumbnail']

    # 5MB (5 million byte) buffer - thumbnail unlikely to be larger
    thumb_read_buffer = Buffer(5000000)

    # copies data from data stream reference into buffer created above
    asyncio.run(read_stream_into_buffer(thumb_stream_ref, thumb_read_buffer))

    # reads data (as bytes) from buffer
    buffer_reader = DataReader.from_buffer(thumb_read_buffer)
    byte_buffer = buffer_reader.read_bytes(thumb_read_buffer.length)

    with open(thumbnail_path, 'wb+') as fobj:
        fobj.write(bytearray(byte_buffer))


def on_info_changed(session, args):
    print(session)
    print(args)

async def get_media_info():
    sessions = await MediaManager.request_async()

    # This source_app_user_model_id check and if statement is optional
    # Use it if you want to only get a certain player/program's media
    # (e.g. only chrome.exe's media not any other program's).

    # To get the ID, use a breakpoint() to run sessions.get_current_session()
    # while the media you want to get is playing.
    # Then set TARGET_ID to the string this call returns.

    current_session = sessions.get_current_session()
    if current_session:  # there needs to be a media session running
        # if current_session.source_app_user_model_id == TARGET_ID:
        info = None
        try:
            info = await current_session.try_get_media_properties_async()
        except:
            return None
        # song_attr[0] != '_' ignores system attributes
        info_dict = {song_attr: info.__getattribute__(song_attr) for song_attr in dir(info) if song_attr[0] != '_'}

        # converts winrt vector to list
        info_dict['genres'] = list(info_dict['genres'])
        return info_dict

    # It could be possible to select a program from a list of current
    # available ones. I just haven't implemented this here for my use case.
    # See references for more information.
    return None


def get_folder_path() -> str:
    folder = ""
    if len(sys.argv) < 2:
        print("writing files in this folder")
        print("You can pass the folder as the script argument like this:")
        print(f"python {sys.argv[0]} folderName")
        folder = "./"
        # folder = filedialog.askdirectory() # makes the read_stream_into_buffer() bug...
    else:
        folder = sys.argv[1]
    if not os.path.isdir(folder):
        print(folder, " is not a folder")
        exit()
    return folder

def main():
    folder = get_folder_path()
    thumbnail_path = str(Path(folder, "media_thumb.jpg"))
    music_info_path = str(Path(folder, "music_info.txt"))

    title = None
    while True:
        current_media_info = asyncio.run(get_media_info())
        if current_media_info != None and current_media_info['title'] != title:
            title = current_media_info['title']
            print(title)
            if current_media_info['thumbnail']:
                write_thumbnail(current_media_info, thumbnail_path)
                if filecmp.cmp(thumbnail_path, "./spotify_icon.jpg"):
                    shutil.copyfile("./cd_case.png", thumbnail_path)
            else:
                shutil.copyfile("./cd_case.png", thumbnail_path)
            with open(music_info_path, "w", encoding="utf-8") as f:
                f.write(current_media_info['album_title'].replace("\n", "") + "\n" + title.replace("\n", ""))
        time.sleep(1)

if __name__ == '__main__':
    main()