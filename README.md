# Mopidy For NAS

Run Mopidy music service on a pre-built NAS (QNAP, Synology, etc.) with docker container.

## Features

The following extensions are included:

- [Mopidy-Iris](https://github.com/jaedb/iris): A user-friendly web client.
- [Mopidy-Spotify](https://github.com/mopidy/mopidy-spotify): Backend for playing Spotify music. (Disabled by default)
- [Mopidy-YouTube](https://github.com/natumbri/mopidy-youtube): Backend for playing sounds from YouTube.
- [Mopidy-YTMusic](https://github.com/OzymandiasTheGreat/mopidy-ytmusic): Backend for playing YouTube Music. (Disabled by default)

## Get Started
> Note: Docker and Docker Comopose is required to be installed on NAS.

1. SSH or telnet into the NAS with admin (root) user.

2. Change to the working directory. This directory must be fully isolated from other user. 
```
cd [your_docker_compose_collection_dir]
```

3. Download the MopidyForNAS repo. It is recommended to use `git` to keep them up to date.
> Hint: [Entware](https://github.com/Entware/Entware/wiki) is your friend.
```
git clone --recursive https://github.com/cbsghost/MopidyForNAS.git
cd MopidyForNAS
```
Alternatively, you can download them to a single zip bundle if `git` isn't available in the NAS.
```
wget https://github.com/cbsghost/MopidyForNAS/archive/master.zip
unzip master.zip
cd MopidyForNAS-master
```

4. Execute the `bootstrap.sh` script.
```
./bootstrap.sh
```
During bootstrap process, the guide will ask for a audio output device for playing music.
Use up and down arrow key to select the audio device for your needs.
Press 't' to play tone on the selected audio device.

5. Edit `mopidy.conf` using any text editor.

Only the youtube extension is enabled by default.
You may want to enable some other extensions. (Spotify, TuneIn, etc.)
Please refer to each exension's homepage for their configuration details.

In the working directory, there is now a symlinked directory called `Mopidy-Media`.
Place any music you want into the direcotry. It can be organized by sub-directories.

6. Start the Mopidy docker app. Access the client using any web browser with address `http://[IP]:6680/`.
```
docker-compose up -d
```

You can rerun `bootstrap.sh` at any time when you want to change audio output device.
The script will only change the audio settings on your modified `mopidy.conf`.

## License
Copyright (c) 2021 CbS Ghost. Released under MIT license.  
For more information, please refer to [LICENSE.txt](LICENSE.txt).
