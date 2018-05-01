from datetime import datetime
from pynput import keyboard
from collections import namedtuple

import sys
import os
import threading
import mss
import mss.tools

Frame = namedtuple('Frame', 'timestamp image input')


def main(argv):
	global inputStateLock, inputState, recordingEvent, exitEvent
	global startTime, filename

	try:
		filename = argv[1];
	except:
		print("Please provide a filename for the .sync file")
		return False

	if not os.path.exists(filename):
		os.makedirs(filename)

	# Creates header info for reading with csv.DictReader
	input_log = open("{0}\\inputlog.csv".format(filename), "a")
	input_log.write("frame,input\n")

	inputStateLock = threading.Lock()
	inputState = 0
	recordingEvent = threading.Event()
	exitEvent = threading.Event()

	recorder = threading.Thread(target=thread_caputure_frames)
	saver = threading.Thread(target=thread_save_frames)
	keylogger = keyboard.Listener(on_press=on_press, on_release=on_release)
	keylogger.start()

	print("Recorder Knight is running, press F10 to begin recording")
	recordingEvent.wait()
	print("Recording has begun Press F10 again to end")
	startTime = datetime.now()
	recorder.start()
	saver.start()
	
	#recording thread Hello WOrld

	keylogger.join()
	recorder.join()
	saver.join()
	print("Recording has ended")


# the input state is a binary vector representing <w a s d j k>
def on_press(key):
	global recordingEvent, inputStateLock, inputState

	if(type(key) is keyboard.KeyCode):
		if (key.char is not None and key.char in 'wasdjk'):
		 	inputStateLock.acquire()
		 	if(key.char is 'w'):
		 		inputState = inputState | 1
		 	elif(key.char is 'a'):
		 		inputState = inputState | 2
		 	elif(key.char is 's'):
		 		inputState = inputState | 4
		 	elif(key.char is 'd'):
		 		inputState = inputState | 8
		 	elif(key.char is 'j'):
		 		inputState = inputState | 16
		 	elif(key.char is 'k'):
		 		inputState = inputState | 32
		 	inputStateLock.release()
	else:
		if(key is keyboard.Key.f10 and not recordingEvent.is_set()):
			recordingEvent.set()
		elif(key is keyboard.Key.f10 and recordingEvent.is_set()):
			recordingEvent.clear()


def on_release(key):
	global exitEvent, inputState

	if(type(key) is keyboard.KeyCode):
		if (key.char is not None and key.char in 'wasdjk'):
			inputStateLock.acquire()
			if(key.char is 'w'):
				inputState = inputState & (63-1)
			elif(key.char is 'a'):
				inputState = inputState & (63-2)
			elif(key.char is 's'):
				inputState = inputState & (63-4)
			elif(key.char is 'd'):
				inputState = inputState & (63-8)
			elif(key.char is 'j'):
				inputState = inputState & (63-16)
			elif(key.char is 'k'):
				inputState = inputState & (63-32)
			inputStateLock.release()
	else:
		if(key is keyboard.Key.f10 and not recordingEvent.is_set()):
			exitEvent.set()
			return False


def thread_caputure_frames():
	global inputStateLock, inputState, exitEvent, startTime, activeList, inactiveList, save_event

	frontList = []
	backList = []

	activeList = frontList
	inactiveList = backList

	save_event = threading.Event();

	mon = {'top': 31, 'left': 8, 'width': 400, 'height': 240}
	sct = mss.mss()

	while True:
		if(exitEvent.is_set()):
			tmplist = activeList
			activeList = inactiveList
			inactiveList = tmplist
			save_event.set()
			return False

		img = sct.grab(mon)
		now = datetime.now() - startTime
		inputStateLock.acquire()
		activeList.append(Frame(timestamp=now, image=img, input=inputState))
		inputStateLock.release()

		if(len(activeList) > 7500 and not save_event.is_set()):
			tmplist = activeList
			activeList = inactiveList
			inactiveList = tmplist

			save_event.set()


def thread_save_frames():
	global save_event, inactiveList, filename

	while True:
		save_event.wait()
		print("Saving has begun...")

		input_log = open("{0}\\inputlog.csv".format(filename), "a")
		while(len(inactiveList) > 0):
			curr_frame = inactiveList.pop(0)
			timestamp_str = '{0}_{1}'.format(curr_frame.timestamp.seconds, curr_frame.timestamp.microseconds)
			mss.tools.to_png(curr_frame.image.rgb, curr_frame.image.size, output='{0}\\{1}.png'.format(filename, timestamp_str))
			input_log.write('{0},{1}\n'.format(timestamp_str,curr_frame.input))

		input_log.close()
		save_event.clear()
		print("Saving has finished.")

		if(exitEvent.is_set()):
			return False



if (__name__ == "__main__"):
	main(sys.argv)