#!/bin/sh
#
# booststrap.sh
# MopidyForNAS
#
# Created by CbS Ghost on 03/14/2021.i
# Copyright (c) 2021 CbS Ghost. Released under MIT license.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
echo "::: Welcome to bootstrap process of MopidyForNAS project! :::"
echo ""

echo "Creating Docker volume: 'mopidy-data' ..."
docker volume create mopidy-data
echo "done."
echo ""

echo "Creating Docker volume: 'mopidy-media' ..."
docker volume create mopidy-media
echo "done."
echo ""

echo "Creating symlink for 'mopidy-media' ..."
ln -s "`docker volume inspect --format "{{.Mountpoint}}" mopidy-data`" \
	"Mopidy-Media"
echo "done."
echo ""

echo "Starting Mopidy configurator in Docker container ..."
docker run --rm -it --user 0 --device "/dev/snd" \
	-v "$(pwd):/tmp/MopidyForNAS" --entrypoint "/bin/bash" \
	"ivdata/mopidy:latest" "-c" \
	"echo \">>> Installing essential packages. This may take a little while ...\" && apt-get -qq update > /dev/null && apt-get -qq -y install gstreamer1.0-alsa libasound2-dev > /dev/null && pip3 install -q -U pick pyalsaaudio && python3 /tmp/MopidyForNAS/mopidy-configurator.py"
echo "done."
echo ""

echo "Fixing permission of config file ..."
chmod 600 "mopidy.conf"
echo "done."
echo ""

echo "All done. Run 'docker-compose up -d' to start Mopidy Docker."
echo "Don't forget to modify 'mopidy.conf' for additional online music" \
     "service. (Spotify, TuneIn, etc)"
echo ""

