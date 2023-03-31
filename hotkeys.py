from AppKit import *
from PyObjCTools import AppHelper
import openai
import pyperclip
import pyautogui
import keyboard
import time

openai.api_key = ""

## CHANGE ME TO TWEAK CONTROLS
MODIFIERS = [
    NSEventModifierFlagShift,
    NSEventModifierFlagCommand
]
KEY_SHORTCUT = "\""
MAX_DELAY = 0.5

def gotEvent(ev):
    print(ev)

    TOTAL_MODS = [
        NSEventModifierFlagShift,
        NSEventModifierFlagCommand,
        # NSEventModifierFlagCapsLock, fuck capslock
        NSEventModifierFlagControl,
        NSEventModifierFlagOption,
        NSEventModifierFlagNumericPad,
        NSEventModifierFlagHelp,
        NSEventModifierFlagFunction,
    ]
    
    #### INPUT VALIDATION
    
    flags = ev.modifierFlags()

    if ev.charactersIgnoringModifiers() != KEY_SHORTCUT:
        return

    for mod in TOTAL_MODS:
        # If it's requested, it must be pressed
        if mod in MODIFIERS:
            if flags & mod == 0:
                return
        # Otherwise, it must not be pressed
        else:
            if flags & mod != 0:
                return
            
    triggerComputation()

    return

    #### TIME VALIDATION
    
    tm = ev.timestamp()
    
    if tm - HotKeyApp.initial_timestamp <= MAX_DELAY:
        triggerComputation()
    else:
        HotKeyApp.initial_timestamp = tm

def triggerComputation():
    clipboard_contents = pyperclip.paste()

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": 'make this sentence formal: ' + clipboard_contents}])
    
    res = []
    for sub in response.choices[0].message.content:
        res.append(sub.replace("\n", ""))
    res = ''.join(res).strip("\"")
    print(res)
    pyperclip.copy(res)
    clipboard_contents = res

    pyautogui.keyDown('command')
    time.sleep(0.5)
    pyautogui.keyDown('v')
    time.sleep(0.5)
    pyautogui.keyUp('v')
    pyautogui.keyUp('command')
    # pyautogui.hotkey('command', 'v')

class HotKeyApp(NSApplication):

    initial_timestamp = 0.0

    def finishLaunching(self):
        super(HotKeyApp, self).finishLaunching()
        NSEvent.addGlobalMonitorForEventsMatchingMask_handler_(NSEventMaskKeyDown, gotEvent)

    def sendEvent_(self, theEvent):
        super(HotKeyApp, self).sendEvent_(theEvent)

if __name__ == "__main__":
    app = HotKeyApp.sharedApplication()
    AppHelper.runEventLoop()
