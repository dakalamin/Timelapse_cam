import cv2
import os
import sys

import datetime as dt
from time import sleep


###   ЗДЕСЬ МОЖНО МЕНЯТЬ ПАРАМЕТРЫ   ###
TIME_START  = dt.time(hour=8,  minute=30)  # ВРЕМЯ НАЧАЛА ПЕРИОДА СЪЕМКИ
TIME_FINISH = dt.time(hour=18, minute=12)  # ВРЕМЯ ОКОНЧАНИЯ ПЕРИОДА СЪЕМКИ
                                           # должен быть больше HOUR_START
#TODO: add smart threshold definition
SLEEP_THR = 2  # Sleep Threshold: ВРЕМЕННОЙ ПРОМЕЖУТОК ДЛЯ sleep() В СЕКУНДАХ
FPD = 24 * 30  # Frames Per Day:  КОЛ-ВО КАДРОВ В СУТКИ
###   ДАЛЬШЕ НЕ СТОИТ   ###


WARNING_SHOWED = False
SBF = 24*60*60 // FPD  # Seconds Between Frames: СЕКУНД МЕЖДУ КАДРАМИ

# Folder Name Pattern: ШАБЛОН ИМЕНИ ПАПКИ
# Image  Name Pattern: ШАБЛОН ИМЕНИ ИЗОБРАЖЕНИЯ
# -------------------  чем больше кадров в единицу времени,
# -------------------  тем больше точность времени в названии изображения
FOLDER_NT = "dir%Y_%m_%d"
IMAGE_NT  = "%H" + "_%M"*(FPD > 60) + "_%S"*(FPD > 60*60) + "image.png"


DEBUG_MODE = True
dg_print = lambda *args, **kwargs: print(*args, **kwargs) if DEBUG_MODE else None


###   sleep() по разнице между текущим моментом и началом нового периода   ###
def sleepDelta(dts, today):
    delta = int((dts - today).total_seconds())
    sleepTime = delta - SLEEP_THR
    
    if sleepTime <= 0:
        sleepTime = delta

    if sleepTime > 0:
        dg_print("Estimated sleep time is approx.:" + extractTU(sleepTime))

        # сообщение с предупреждением выводится только один раз
        global WARNING_SHOWED
        if not WARNING_SHOWED:
            WARNING_SHOWED = True
            dg_print("WARNING! Program will be unresponsive during this time")

        sleep(sleepTime)


###   Exctracting Time Units: формирует строку Час/Мин/Сек по кол-ву секунд   ###
def extractTU(seconds):
    DEBUG_SBF = (seconds//3600, (seconds//60)%60, seconds%60)
    DEBUG_TU  = ("hour", "minute", "second")

    string = ""
    
    for i in range(3):
        if DEBUG_SBF[i]:
            string += " {} {}".format(str(DEBUG_SBF[i]), DEBUG_TU[i])
            if DEBUG_SBF[i] > 1:
                string += "s"

    return string
        

def main():
    dg_print("Images will be taken daily every" + extractTU(SBF))
    dg_print("from " + TIME_START.strftime("%H:%M:%S") + " to " + TIME_FINISH.strftime("%H:%M:%S"))
    
    dg_print("\nInitializing camera, please wait...")
    camera = cv2.VideoCapture(0)
    
    try:
        if not camera.isOpened():
            raise Exception("No cameras found!")
        
        dg_print("CAMERA INITIALIZED\n")
        
        today = dt.datetime.today()
        while True:
            dtf = dt.datetime.combine(today, TIME_FINISH)   # datetime_finish
            if today >= dtf: dtf += dt.timedelta(hours=24)  # если текущее время уже не попадает в интервал текущего дня
                                                            # перенести запуск на следующий день
            dts = dt.datetime.combine(dtf, TIME_START)      # datetime_start

            folderPath = dts.strftime(FOLDER_NT)
                
            if not os.path.exists(folderPath):    # создать папку для изображений текущего дня
                os.mkdir(folderPath)
                dg_print("Day " + dts.strftime("%b %d") + " folder created: /" + folderPath)

            if not dts <= today < dtf:            # ожидать начала ближайшего интервала
                dg_print("Waiting for the next period starting at " + dts.strftime("%b %d, %H:%M:%S"))
                sleepDelta(dts, today)

            today = dts = dt.datetime.today()
            while today < dtf:
                while today < dts:                # sleepDelta(...) выполняет задержку на время чуть меньшее, чем необходимо
                    today = dt.datetime.today()   # последние секунды задержки отсчитываются в этом цикле
                
                imagePath = today.strftime(IMAGE_NT)
                
                ret, image = camera.read()
                if not ret:
                    raise Exception("Camera connection lost!")
                    
                cv2.imwrite(folderPath+'/'+imagePath, image)
                dg_print(today.strftime("\n[%H:%M:%S]"), "Frame successfully captured")

                today = dt.datetime.today()
                dts += dt.timedelta(seconds=SBF)  # вычислить время считывания следующего изображения

                if dts < dtf:  # если следующее изображение успевает быть считанным до конца текущего интервала
                    dg_print("Waiting for the next alarm")
                    sleepDelta(dts, today)        # ожидать момента считывания следующего изображения
                    today = dt.datetime.today()
                else:
                    today = dtf

    finally:
        camera.release()  # отключить камеру при любом завершении программы


# https://stackoverflow.com/questions/419163/what-does-if-name-main-do
if __name__ == "__main__":
    main()
