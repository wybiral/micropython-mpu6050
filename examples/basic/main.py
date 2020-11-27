from machine import I2C, Pin
from time import sleep
import mpu6050

i2c = I2C(scl=Pin(5), sda=Pin(4))

mpu = mpu6050.MPU6050(i2c)

mpu.init()

print('Calibrating...')
mpu.calibrate()
print('Done!')

while True:
    print(mpu.read())
    sleep(0.125)
