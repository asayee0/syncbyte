# SyncByte
## Music Player and Streamer
### Software Engineering 2 Project

# How to use
1. Install python tkinter
`sudo apt install python-tk`
2. Install the requirements
`pip3 install -r requirements.txt`
3. Create a folder called `music` in `syncbyte-master` and add any .mp3 files to that folder
4. Run the server. Once running, the server will start listening for connections.
`python3 musicplayer_host.py`
5. Run the client
`python3 musicplayer_client.py`
6. Once running, the client will prompt for an address to connect to. Enter `localhost`.
7. The server will take a few seconds to transfer the song to the client, and once it's done, the client will automatically begin playing the song from the server's timestamp.

# Team
Miguel Forde 

Chanelle Glasglow

Marcus Hackshaw

Asa Yee