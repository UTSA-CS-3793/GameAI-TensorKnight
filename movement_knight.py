# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import pyautogui
import ctypes
import time
import random

SendInput = ctypes.windll.user32.SendInput

# C struct redefinitions 
PUL = ctypes.POINTER(ctypes.c_ulong)
class KeyBdInput(ctypes.Structure):
    _fields_ = [("wVk", ctypes.c_ushort),
                ("wScan", ctypes.c_ushort),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", PUL)]

class HardwareInput(ctypes.Structure):
    _fields_ = [("uMsg", ctypes.c_ulong),
                ("wParamL", ctypes.c_short),
                ("wParamH", ctypes.c_ushort)]

class MouseInput(ctypes.Structure):
    _fields_ = [("dx", ctypes.c_long),
                ("dy", ctypes.c_long),
                ("mouseData", ctypes.c_ulong),
                ("dwFlags", ctypes.c_ulong),
                ("time",ctypes.c_ulong),
                ("dwExtraInfo", PUL)]

class Input_I(ctypes.Union):
    _fields_ = [("ki", KeyBdInput),
                 ("mi", MouseInput),
                 ("hi", HardwareInput)]

class Input(ctypes.Structure):
    _fields_ = [("type", ctypes.c_ulong),
                ("ii", Input_I)]

# Actuals Functions

def PressKey(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput( 0, hexKeyCode, 0x0008, 0, ctypes.pointer(extra) )
    x = Input( ctypes.c_ulong(1), ii_ )
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

def ReleaseKey(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput( 0, hexKeyCode, 0x0008 | 0x0002, 0, ctypes.pointer(extra) )
    x = Input( ctypes.c_ulong(1), ii_ )
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))
    
def PogoJump():
    PressKey(K)
    PressKey(S)
    time.sleep(1)
    ReleaseKey(K)
    ReleaseKey(S)
def Attack():
    PressKey(J)
    time.sleep(1)
    ReleaseKey(J)
def MoveRight():
    PressKey(D)
    time.sleep(1)
    ReleaseKey(D)
def MoveLeft():
    PressKey(A)
    time.sleep(1)
    ReleaseKey(A)
def Wait():
    time.sleep(1)
def JumpRight():
    PressKey(K)
    PressKey(D)
    PressKey(S)
    time.sleep(1)
    ReleaseKey(K)
    ReleaseKey(D)
    ReleaseKey(S)
    time.sleep(1)
def JumpLeft():
    PressKey(K)
    PressKey(A)
    PressKey(S)
    time.sleep(1)
    ReleaseKey(K)
    ReleaseKey(A)
    ReleaseKey(S)
def MoveUp():
    PressKey(K)
    PressKey(W)
    time.sleep(3)
    ReleaseKey(K)
    ReleaseKey(W)


A = 0x1E
D = 0x20
J = 0x24
K = 0x25
S = 0x1F
W = 0x11
counter = 0
while (counter < 28):
    JumpRight()  
    Attack()
    counter = counter + 1
    print(counter)
    
MoveUp()
# directx scan codes http://www.gamespp.com/directx/directInputKeyboardScanCodes.html
while (True):
    randint=random.randrange(10)
    print(randint)
    if randint == 1:
        PogoJump()
    else:
        if randint == 2:
            Attack()
        else:
            if randint == 3:
                MoveLeft()
            else:
                if randint == 4:
                    MoveRight()
                else:
                        if randint == 5:
                            JumpRight()
                        else:
                            if randint == 6:
                                JumpRight()
                            else:
                                if randint == 7:
                                    Attack()
                                else:
                                        if randint == 8:
                                            MoveUp()
                                        else:
                                            if randint == 9:
                                                JumpLeft()
                                            else:
                                                if randint == 0:
                                                    MoveUp()
                                                

               


    
    
    
    