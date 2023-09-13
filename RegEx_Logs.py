
import re
import logging
import os
import datetime

# _____Logging_____:

current_time = datetime.datetime.now()

year = '{:02d}year'.format(current_time.year)
month = '{:02d}month'.format(current_time.month)
day = '{:02d}day'.format(current_time.day)
hour = '{:02d}hour'.format(current_time.hour)
minute = '{:02d}min'.format(current_time.minute)
second = '{:02d}sec'.format(current_time.second)

dir_ = os.path.dirname(__file__)
log_file = os.path.join(dir_, "logs", "{0}_{1}_{2}_{3}_{4}_{5}_maya.log".format(year, month, day, hour, minute, second))

logger = logging.getLogger("MayaLogs")
logger.setLevel(logging.DEBUG)

for i in logger.handlers:
    print ("Removing {} handler".format(i))
    logger.removeHandler(i)


file_handler = logging.FileHandler(log_file, mode='w')
file_handler_format = logging.Formatter('[%(module)s.%(funcName)s.%(lineno)d]%(levelname)s:%(message)s')
file_handler.setFormatter(file_handler_format)

logger.addHandler(file_handler)

def main():
    logger.debug()
    logger.info()
    logger.error()
    logger.warning()

    file_handler.close()
    logger.removeHandler(file_handler)
  


# _____RegEx script_____:

file_path = 'C:/Users/Mariia Grebeshkova/OneDrive/Documents/Data.txt' # the file path to be filtred  

if not os.path.isfile(file_path):
    logger.error("There is no such file path {}".format(file_path))
    
else:
    logger.info("Acces to the file  {}".format(file_path))
    with open(file_path, 'r') as file:
        a = file.readlines()
    
template = re.compile("^([+-]?\d{0,5}[1-9]|[+-]10{7}|0|([-]?[1-9]*|0\.\d*[1-9]+))$")


for line in a:
    line = line.strip() # delete all blank spaces
    if template.match(line):
        logger.info(line + " - It`s a match!")
        print(line + " - " + "It`s a match!")
    


# [0-9]?[0-9]?[0-9]?[0-9]?[0-9]?[1-9] = \d{0,5}[1-9] can`t be all zeroes, last number in a diapazone 1-9
# for float numbers: [0-9]+\.[1-9]+ = \d+\.[1-9]+ (0.0 excluded) but also have to exclude - 00.32423 therefore: ([1-9]*|0\.[0-9]*[1-9]+)
Script_L9.py
Displaying Script_L9.py.
