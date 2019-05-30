import w1thermsensor
import datetime
import time
import os
import configparser

config = configparser.ConfigParser()
sensor = w1thermsensor.W1ThermSensor()

ROW = '{0:.4f};{1}\r\n'


#file management
ROOT_DIR = "days"
fNameDay = '{}/termo.{{0:%Y-%m-%d}}.csv'.format(ROOT_DIR)
fNameAlerts = '{}/termo.alerts.csv'.format(ROOT_DIR)
if not os.path.exists(ROOT_DIR):
    os.makedirs(ROOT_DIR)


def calculate_average(totalSeconds, dt, errDev, errMin, errMax):
    #local interval
    startTime = datetime.datetime.now()
    avg = 0 #average calculation helper

    dataFormat = '{0:.3f}*C\t{1}\t(dt={2:.2f}s)'
    loopCounter = 0
    steps = 0.0
    while (loopCounter < totalSeconds):
        now = datetime.datetime.now() #current time
        temperature = sensor.get_temperature() #current temperature
        readDuration = (datetime.datetime.now() - now).total_seconds()
        a = check_alert(temperature, errMin, errMax, errDev)
        if a:
            alert = '\tALERT!'
        else:
            alert = ''
        avg += temperature
        waitLength = dt - readDuration
        data = '{0:.3f}*C\t{1}\t(read={2:.2f}s){3}'.format(temperature, now, readDuration, alert)
        print(data)
        
        steps += 1.0

        if (waitLength <= 0):
            loopCounter += readDuration
        else:
            loopCounter += dt
            time.sleep(waitLength)
    totalTime = datetime.datetime.now() - startTime
    avg /=  steps
    data = dataFormat.format(avg, datetime.datetime.now(), totalTime.total_seconds())
    print('* Average:\r\n\t', data)
    return avg

def generate_line():
    config.read('termo.conf')
   
    cTiming = config['TIME']
    LOCAL_TICK = cTiming.getfloat('readInterval', 2.0)
    AVG_TICK = cTiming.getfloat('avgInterval', 900.0)
    AVG_STEPS = AVG_TICK / LOCAL_TICK
       
    cLimits = config['LIMITS']
    ERR_DEV = cLimits.getfloat('precision', 0.5)
    ERR_MIN = cLimits.getfloat('min', 2.0)
    ERR_MAX = cLimits.getfloat('max', 8.0)
   
    currentAverage = calculate_average(AVG_TICK, LOCAL_TICK, ERR_DEV, ERR_MIN, ERR_MAX)
    currentTime = datetime.datetime.now()

    rowData = ROW.format(currentAverage, currentTime)

    todayDate = datetime.datetime.now()
    with open(fNameDay.format(todayDate), 'a') as todayFile:
        todayFile.write(rowData)
#    todayFile.close()


def check_alert(temperature, tmin, tmax, dev):
    if (temperature > tmin - dev and temperature < tmax + dev):
        return False
    #invalid temperature!
    with open(fNameAlerts, 'a') as alertFile:
        info = '{1:.1f};{0}\r\n'.format(datetime.datetime.now(), temperature)
        alertFile.write(info)
    return True

while True:
    generate_line()
