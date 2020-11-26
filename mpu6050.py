import ustruct

class MPU6050:

    def __init__(self, i2c, addr=0x68):
        self.i2c = i2c
        self.addr = addr
        self._a_cal = [0.0, 0.0, 0.0]
        self._g_cal = [0.0, 0.0, 0.0]

    def init(self):
        self.i2c.start()
        self.i2c.writeto(self.addr, bytearray([107, 0]))
        self.i2c.stop()

    def read_raw(self):
        self.i2c.start()
        raw = self.i2c.readfrom_mem(self.addr, 0x3b, 14)
        self.i2c.stop()
        return ustruct.unpack(">hhhhhhh", raw)

    def read(self):
        x = self.read_raw()
        a = [0, 0, 0]
        g = [0, 0, 0]
        for i in range(3):
            a[i] = (x[i] / 32768) - self._a_cal[i]
            g[i] = (x[i + 4] / 131) - self._g_cal[i]
        t = x[3] / 340.00 + 36.53
        return {'a': a, 'g': g, 't': t}

    def calibrate(self, n=100):
        a_cal = [0.0, 0.0, 0.0]
        g_cal = [0.0, 0.0, 0.0]
        for j in range(n):
            x = self.read_raw()
            for i in range(3):
                a_cal[i] += x[i] / 32768
                g_cal[i] += x[i + 4] / 131
        for i in range(3):
            self._a_cal[i] = a_cal[i] / n
            self._g_cal[i] = g_cal[i] / n
