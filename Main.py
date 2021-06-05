import cv2
import os

import datetime as dt
from time import sleep


###   ЗДЕСЬ МОЖНО МЕНЯТЬ ПАРАМЕТРЫ   ###
TIME_START  = dt.time(hour=8,  minute=30) # ВРЕМЯ НАЧАЛА ПЕРИОДА СЪЕМКИ
TIME_FINISH = dt.time(hour=18, minute=12) # ВРЕМЯ ОКОНЧАНИЯ ПЕРИОДА СЪЕМКИ
                                          # должен быть больше HOUR_START
SLEEP_THR = 2        # Sleep Threshold: ВРЕМЕННОЙ ПРОМЕЖУТОК ДЛЯ sleep() В СЕКУНДАХ
FPD = 24*30          # Frames Per Day:  КОЛ-ВО КАДРОВ В СУТКИ
###   ДАЛЬШЕ НЕ СТОИТ   ###


WARNING_SHOWED = False
SBF = 24*60*60//FPD  # Seconds Between Frames: СЕКУНД МЕЖДУ КАДРАМИ

FOLDER_NT = "dir%Y_%m_%d"  # Folder Name Pattern: ШАБЛОН ИМЕНИ ПАПКИ
IMAGE_NT  = "%H"           # Image  Name Pattern: ШАБЛОН ИМЕНИ ИЗОБРАЖЕНИЯ
if FPD > 60:               #
    IMAGE_NT += "_%M"      # чем больше кадров в единицу времени,
    if FPD > 60*60:        # тем больше точность времени в названии изображения
        IMAGE_NT += "_%S"
IMAGE_NT += "image.png"


###   sleep() по разнице между текущим моментом и началом нового периода   ###
def sleepDelta(dts, today, debug=False):
    delta = int((dts - today).total_seconds())
    sleepTime = delta - SLEEP_THR
    
    if sleepTime <= 0:
        sleepTime = delta

    if sleepTime > 0:
        if debug:
            print("Estimated sleep time is approx.:"+extractTU(sleepTime))

            global WARNING_SHOWED  # сообщение с предупреждением выводиться только один раз
            if not WARNING_SHOWED:
                WARNING_SHOWED = True
                print("WARNING! Program will be unresponsive during this time")

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
    print("Images will be taken daily every"+extractTU(SBF))
    print("from "+TIME_START.strftime("%H:%M:%S")+" to "+TIME_FINISH.strftime("%H:%M:%S"))
    
    
    print("\nInitializing camera, please wait...")
    camera = cv2.VideoCapture(0)
    
    try:
        if not camera.isOpened():
            raise BaseException("No cameras found!")
        
        print("CAMERA INITIALIZED\n")
        
        today = dt.datetime.today()
        while True:
            dtf = dt.datetime.combine(today, TIME_FINISH)   # datetime_finish
            if today >= dtf: dtf += dt.timedelta(hours=24)  # если текущее время уже не попадает в интервал текущего дня
                                                            # перенести запуск на следующий день
            dts = dt.datetime.combine(dtf, TIME_START)      # datetime_start

            folderPath = dts.strftime(FOLDER_NT)
                
            if not os.path.exists(folderPath):    # создать папку для изображений текущего дня
                os.mkdir(folderPath)
                print("Day "+dts.strftime("%b %d")+" folder created: /"+folderPath)

            if not dts <= today < dtf:            # ожидать до начала ближайшего интервала
                print("Waiting for the next period starting at "+dts.strftime("%b %d, %H:%M:%S"))
                sleepDelta(dts, today, debug=True)

            today = dt.datetime.today()
            dts   = dt.datetime.today()
            while today < dtf:
                while today < dts:                # sleepDelta(...) выполняет задержку на время чуть меньшее, чем необходимо
                    today = dt.datetime.today()   # последние секунды задержки отсчитываются в этом цикле
                
                imagePath = today.strftime(IMAGE_NT)
                
                ret, image = camera.read()
                if not ret:
                    raise BaseException("Camera connection lost!")
                    
                cv2.imwrite(folderPath+'/'+imagePath, image)
                print(today.strftime("\n[%H:%M:%S]"), "Frame successfully captured")

                today = dt.datetime.today()
                dts += dt.timedelta(seconds=SBF)  # вычислить время считывания следующего изображения

                if dts < dtf:  # если следующее изображение успевает быть считанным до конца текущего интервала
                    print("Waiting for the next alarm")
                    sleepDelta(dts, today, debug=True)  # ожидать до момента считывания следующего изображения
                    today = dt.datetime.today()
                else:
                    today = dtf
                       
    finally:
        camera.release()  # отключить камеру при любом завершении программы
        raise


# https://stackoverflow.com/questions/419163/what-does-if-name-main-do
if __name__ == "__main__":
    main()
