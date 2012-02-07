import ImageGrab, ImageOps
import Image
import ImageChops
import sys, os
import win32api, win32con
import time
from random import random
from random import randrange
from multiprocessing import Process
import math

def mousePos(x):
	win32api.SetCursorPos(x);
    
def leftClick():
	win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
	win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)
	print "MOUSE CLICK!!"
	time.sleep(.05)
    
#def rightClick():
#    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN,0,0)
#	win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP,0,0)
#    print "MOUSE CLICK!!"
#    time.sleep(.05)
    	

		
t = 0.0;
		
record_state = 0; #not recorded
		
min_pos = [999999, 999999];
max_pos = [0,0];
	
read_tuple = None;
pattern_image = None;
	

def read_cfg():
	global read_tuple;
	global pattern_image;
	
	file = open( 'Spinning.cfg', 'r' );
	read_tuple = eval( file.readline() );
	file.close();
	pattern_image = Image.open( 'Spinning.png' )
	
read_cfg();
	
while 1:
		if win32api.GetKeyState( win32api.VkKeyScan('r') ):
			im = ImageGrab.grab( read_tuple );
			diff = ImageChops.difference(im, Image.open( 'Spinning.png' ))
			if not diff.getbbox():
				mousePos( ( (read_tuple[2]+read_tuple[0])/2, (read_tuple[1]+read_tuple[3])/2 ) );
				leftClick();
			else:
				print "there is difference " + str(diff.getbbox()) + '||||' + str( read_tuple )
				im.save(os.getcwd() + '\\' + 'Spinning2.png', "PNG")
				exit();
			
		if win32api.GetKeyState( win32api.VkKeyScan('q') ):
			record_state = 1; #recording

		if win32api.GetKeyState( win32api.VkKeyScan('w') ):
			record_state = 2; #finished
			
		if record_state	== 1:
			pos = win32api.GetCursorPos();
			min_pos[0] = min( min_pos[0], pos[0] );
			min_pos[1] = min( min_pos[1], pos[1] );
			max_pos[0] = max( max_pos[0], pos[0] );
			max_pos[1] = max( max_pos[1], pos[1] );
		
		if record_state==2 and win32api.GetKeyState(win32api.VkKeyScan('e')):
			#dump
			im = ImageGrab.grab( tuple(min_pos + max_pos) );
			im.save(os.getcwd() + '\\' + 'Spinning.png', "PNG")
			file = open( 'Spinning.cfg', 'w' );
			file.write( str( min_pos + max_pos ) );
			file.close();
			
		#mousePos( ( int(300 * math.sin( t * 3.1415 / 180.0 )) + 700, int( 300 * math.cos( t * 3.1415 / 180.0 ) ) + 400 ) );
		#t += 1.0;
		#if t > 360: t = 0;
		
		#time.sleep(0.01);

#im = ImageGrab.grab()
#im.save(os.getcwd() + '\\' + 'Spinning.png', "PNG")
    