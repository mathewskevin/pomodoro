# Pomodoro Timer
# Kevin Mathews 19/11/2019
# A simple command line based pomodoro timer. Simply run this python file from the command line and follow the prompts.

import pyautogui as pygui
import win32gui
import time, datetime
import sys, os, math

# function which brings terminal to forefront
def window_top(window_name): 
	def windowEnumerationHandler(hwnd, top_windows):
		top_windows.append((hwnd, win32gui.GetWindowText(hwnd)))	 
	results = []
	top_windows = []	
	win32gui.EnumWindows(windowEnumerationHandler, top_windows)
	for i in top_windows:	
		if window_name in i[1].lower():
			win32gui.ShowWindow(i[0],5)
			win32gui.SetForegroundWindow(i[0])
			break

# function to move mouse cursor, needed to force command prompt to top
def click_point(point_x, point_y, wait=0):
	time.sleep(wait)
	pygui.click(point_x, point_y)
	time.sleep(wait)			
			
# turns an integer into a two digit string
def zero_string(num_val):
	if num_val < 10:
		output = "0" + str(num_val)
	else:
		output = str(num_val)
	return output

# find start and end time for pomodoro/break
def time_analysis(min_length):			
	# https://stackoverflow.com/questions/12448592/how-to-add-delta-to-python-datetime-time
	# print scheduled pomodoro timespan
	time_delta = datetime.timedelta(minutes=min_length)
	start_time = datetime.datetime.now()
	end_time = start_time + time_delta	
	return start_time, end_time

# command line output for countdown
def stdout_time(type_string, end_time):
	timer_toggle = True
	while timer_toggle == True:
		now_mid = datetime.datetime.now() 
		countdown = end_time - now_mid # countdown time
		
		countdown_min = str(math.floor(countdown.seconds / 60))	
		countdown_sec = zero_string(round(countdown.seconds % 60,0))
		countdown_string = countdown_min + ':' + countdown_sec + ' '
		
		if now_mid >= end_time:
			timer_toggle = False
			countdown_string = '0:00'

		# write output to terminal
		sys.stdout.write('\r' + type_string + ' countdown: ' + countdown_string)
		sys.stdout.flush()
		time.sleep(0.2)

# pomodoro timer
def pomodoro_timer(time_type, time_length):
	start_time, end_time = time_analysis(time_length) # get start and end time

	#https://stackabuse.com/how-to-format-dates-in-python/
	print('\n' + time_type.capitalize() + ' running...')
	print(start_time.strftime("%H:%M"), '<- ' + time_type + ' start time')
	print(end_time.strftime("%H:%M"), '<- ' + time_type + ' end time')
	stdout_time(time_type, end_time)
	
# function to run pomodoro timer
def run_pomodoro(text_out = '\n\nBreak done. Ready to start pomodoro? Hit ENTER to start.'):
	click_point(1570, 1061) # click windows taskbar, needed for window_top()
	window_top('cmd')
	input(text_out) # pause to wait for user to be ready for break
	pomodoro_timer('pomodoro', 25)# print pomodoro timer

# function to run break timer
def run_break(text_out = '\n\nPomodoro done. Ready to start break? Hit ENTER to start.'):	
	click_point(1570, 1061) # click windows taskbar, needed for window_top()
	window_top('cmd')
	input(text_out) # pause to wait for user to be ready for break
	pomodoro_timer('break', 5) # print pomodoro timer

# MAIN LOOP
# wait for input to start initial pomodoro	
if len(sys.argv) > 1:
	if sys.argv[1] == "-b": # if you need to start with a break for any reason, supply the -b argument when starting.
		run_break('\nReady to start break? Hit ENTER to start.')
		run_pomodoro()
		pomodoro_loop = True
	else: # if not b, then error
		print('incorrect arguments')
		pomodoro_loop = False
else:
	pomodoro_loop = True
	run_pomodoro('\nReady to start pomodoro? Hit ENTER to start.')

while pomodoro_loop == True:
	run_break()
	run_pomodoro()
	
print('done.') # this line will never be reached