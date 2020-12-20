import os
import time
import datetime
import signal
import math
from gi.repository import Gtk as gtk
from gi.repository import AppIndicator3 as appindicator
from gi.repository import Notify as notify

APPINDICATOR_ID = 'timetracker'
timetrackerrun = 0
basepath = os.path.dirname(os.path.abspath(__file__))+"/"
storagefile = basepath + "database.js"
runnedtimesincestart = 0
starttime = 0
buttontextlist = ['start/stop','time since start','open overview in browser','quit','run open-script']
language = "en"

def main():
    global indicator
    global basepath
    global buttontextlist
    global language
    global storagefile
    print(basepath)
    with open(basepath+"config.js","r") as reader:
      lines = reader.readlines()
      for line in lines:
        if "language" in line:
          if "es" in line:
            print('switch to spanish')
            buttontextlist = ['aranca/termina','tiempo corrido actual','abre sobrevista en navegador','quit', 'ejecute script de inicio']
            language = "es"
        if "name:" in line:
          storagefilename = line.split('"')[1]
          print(storagefilename)
          storagefile = basepath + storagefilename+".js"
          print("switched to use file "+storagefile)

    timetrackerrun = 0
    indicator = appindicator.Indicator.new(APPINDICATOR_ID, os.path.abspath(basepath+'symbol.png'), appindicator.IndicatorCategory.SYSTEM_SERVICES)
    indicator.set_status(appindicator.IndicatorStatus.ACTIVE)
    indicator.set_menu(build_menu())
    notify.init(APPINDICATOR_ID)
    gtk.main()

def build_menu():
    global buttontextlist
    menu = gtk.Menu()
    #startstop function:
    item_start = gtk.MenuItem(buttontextlist[0])
    item_start.connect('activate',startstop)
    item_quit = gtk.MenuItem(buttontextlist[3])
    item_quit.connect('activate', quit)
    item_openall = gtk.MenuItem(buttontextlist[4])
    item_openall.connect('activate',openall)
    item_openoverview = gtk.MenuItem(buttontextlist[2])
    item_openoverview.connect('activate',open_overview)
    item_runtime = gtk.MenuItem(buttontextlist[1])
    item_runtime.connect('activate',showrunningtime)
    menu.append(item_start)
    menu.append(item_runtime)
#    menu.append(item_openall)
    menu.append(item_openoverview)
    menu.append(item_quit)
    menu.show_all()
    return menu

def startstop(asdf):
   global timetrackerrun
   global storagefile
   global runnedtimesincestart
   global starttime
   global basepath

   if timetrackerrun == 0:
    indicator.set_icon(basepath + 'running.png')
    timetrackerrun = 1
    file = open(storagefile, "a")
    file.write("addStartTime('"+datetime.datetime.now().strftime("%Y-%m-%dT%H:%M")+"');\n")
    #file.write("addStartTime("+str(time.time())+");\n");
    starttime = time.time()
   else:
    indicator.set_icon(basepath + 'stopped.png')
    timetrackerrun = 0
    file = open(storagefile, "a")
    file.write("addEndTime('"+datetime.datetime.now().strftime("%Y-%m-%dT%H:%M")+"');\n")
#    file.write("addEndTime("+str(time.time())+");\n");
    endtime = time.time()
    runnedtimesincestart = runnedtimesincestart + endtime - starttime
    starttime = 0

def openall(asdf):
    os.system("caja ~/Dokumente/ &")
    os.system("atom &")

def showrunningtime(_):
    global language
    titletext = "runned time since start:"
    if "es" in language:
      titletext ="tiempo corrido actual:"
    notify.Notification.new(titletext, running_time(), None).show()

def open_overview(_):
    global basepath
    os.system("xdg-open "+basepath+"timetracker.html")

def running_time():
    global runnedtimesincestart
    global starttime
    global language
    actruntime = 0
    if starttime >0:
        actruntime = time.time()-starttime

    runtime = (runnedtimesincestart+actruntime) / 60
    runhours = math.floor(runtime / 60)
    runhourstxt = str(runhours).split('.')[0]
    runminutes = math.floor(runtime - (runhours*60))
    runminutestxt = str(runminutes).split('.')[0]
    returntext = "since last start you have worked " + runhourstxt + " hours and "+runminutestxt+" minutes. globaltime:"+str(runnedtimesincestart)+" starttime:"+str(starttime) + " actruntime:"+str(math.floor(actruntime))
    if "es" in language:
      returntext = "desde iniciar timetracker trabajaste " + runhourstxt + " horas y "+runminutestxt+" minutas."
    return returntext
def quit(source):
    gtk.main_quit()


if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    main()
