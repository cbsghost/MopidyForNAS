#!/usr/bin/env python3
#
# mopidy-configurtor.py
# MopidyForNAS
#
# Created by CbS Ghost on 03/14/2021.
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
import alsaaudio
import configparser
import logging
import os
import re
import sys
from time import sleep
from pick import Picker

import gi
gi.require_version("Gst", "1.0")
from gi.repository import Gst, GObject
Gst.init(None)

configData = None

def SetupReadConfigData():
	global configData
	logging.info("Reading config file")
	configData = configparser.ConfigParser()
	if (configData.read("mopidy.conf") == []):
		logging.info("No existing 'mopidy.conf', reading 'mopidy.conf.example' instead...")
		if (configData.read("mopidy.conf.example")== []):
			raise Exception("Missing example config file")
	logging.info("Finish reading config file")

def SetupAudioDevice():
	global configData
	logging.info("Setting up audio output device")
	selectedDevice = re.compile(r"alsasink device=\"(\S+)\"").match(configData["audio"]["output"])
	availableDeviceList = alsaaudio.pcms()
	devicePickerDefaultIndex = 0
	if (selectedDevice is not None):
		if (selectedDevice.groups()[0] in availableDeviceList):
			devicePickerDefaultIndex = availableDeviceList.index(selectedDevice.groups()[0])
	devicePickerTitle = ("Please select an audio device for music playback using arrow keys.\n"
				"Press 't' to test audio output\n"
				"Press 'Enter' to confirm")
	devicePicker = Picker(availableDeviceList, devicePickerTitle,
					indicator='-->', default_index=devicePickerDefaultIndex)
	devicePicker.register_custom_handler(ord("t"),  PlayTestingAudio)
	devicePickerOption, devicePickerIndex = devicePicker.start()
	configData["audio"]["output"] = "alsasink device=\"%s\"" % availableDeviceList[devicePickerIndex]
	logging.info("Finish setting up audio output device")

def SetupWriteConfigData():
	global configData
	logging.info("Write config file")
	with open("mopidy.conf", "w") as configFile:
		configData.write(configFile)
	logging.info("Finish writing config file")

def PlayTestingAudio(picker):
	pipe = Gst.Pipeline()
	audiotestsrc = Gst.ElementFactory.make("audiotestsrc")
	pipe.add(audiotestsrc)
	sink = Gst.ElementFactory.make("alsasink")
	sink.set_property("device", picker.options[picker.index])
	pipe.add(sink)
	audiotestsrc.link(sink)
	pipe.set_state(Gst.State.PLAYING)
	sleep(3)
	pipe.set_state(Gst.State.NULL)
	return None

if __name__ == "__main__":
	os.chdir(os.path.dirname(os.path.realpath(sys.argv[0])))
	logging.basicConfig(format="[%(levelname)s] %(message)s", level=logging.INFO)
	logging.info("::: Mopidy Configurator :::")
	try:
		SetupReadConfigData()
		SetupAudioDevice()
		SetupWriteConfigData()
	except Exception as err:
		logging.error("Exited with error: %s" % str(err))
		exit(1)
	logging.info("Exited successfully")

