import openai
import pyperclip
import pyautogui
import keyboard
openai.api_key = "JUSTINCASE"

clipboard_contents = pyperclip.paste()
keyboard.press_and_release('delete')
pyautogui.typewrite('loading...')
response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "user", "content": 'make this sentence formal: ' + clipboard_contents}])
for x in range(0, 10):
    keyboard.press_and_release('delete')
res = []
for sub in response.choices[0].message.content:
    res.append(sub.replace("\n", ""))
res = ''.join(res)
pyperclip.copy(res)
keyboard.press_and_release('command+v')
