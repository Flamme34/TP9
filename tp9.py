import locale, sqlite3, smbus2, ctypes, struct
from datetime import datetime
from time import sleep

locale.setlocale(locale.LC_TIME, 'en_US.UTF-8')

source = "bbb-colb-olid"
#Variable DS1629
ds1629_ADDR = 0x4F
temp_raw = ctypes.c_int16()
bus = smbus2.SMBus(2)
bus.write_byte_data(ds1629_ADDR,0xAC,0x00)

date = datetime.now().strftime("%d-%b-%Y %H:%M:%S")
measure = 00

def add_to_database(measure,date,source):
    conn = sqlite3.connect("database-colb-olid.db")
    cursor = conn.cursor()
    date = datetime.now().strftime("%d-%b-%Y %H:%M:%S")
    cursor.execute("""INSERT INTO databaseColbOlid VALUES (?, ?, ?)""",(measure, date, source))
    conn.commit()

def read_ds1629():
    global temp_raw, ds1629_ADDR
    temp_bytes = bytes(bus.read_i2c_block_data(ds1629_ADDR,0xAA,2))
    temp_raw.value = ((temp_bytes[0]<<8 | temp_bytes[1]))
    temp_celsius = float(temp_raw.value)/256
    return int(temp_celsius)

add_to_database(measure, date,source)
num = 0
while True:
    num+=1
    add_to_database(read_ds1629(), date,source)
    print(num)
    sleep(0.1)

