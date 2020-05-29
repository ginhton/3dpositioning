import math
from utils import CatchRssi, rssi2DistanceCSDN, rssi2DistanceGithub, CatchRssis, parseJSON

class WCLSimple:
    def __init__(self):
        self.cache = {}

    def add(self, addr, coords):
        if addr not in self.cache:
            self.cache[addr] = {'rssi': -0, 'coords':coords}
            return True
        return False

    def update(self, data):
        # obj = parseJSON(data)
        obj = data

        if 'error' in obj:
            return None

        addr = obj['addr']

        if addr not in self.cache:

            print("%s not in cache" % addr)
            return None

        rssi = int(obj['rssi']) + 80

        if (rssi < 0):

            rssi = 0

        self.cache[addr]['rssi'] = rssi

        X, Y = 0, 0
        S = 0

        for addr in self.cache:

            X += self.cache[addr]['rssi'] * self.cache[addr]['coords']['x']
            Y += self.cache[addr]['rssi'] * self.cache[addr]['coords']['y']
            S += self.cache[addr]['rssi']

        X = X / S
        Y = Y / S

        print(X, Y)
        return {"X": X, "Y": Y}


class WCLWindow:
    def __init__(self, window=5):
        self.cache = {}
        # window should >= 2
        # window means when I receive *window* number data, generate an ouput
        self.window = window
        self.cnt = 0

    def add(self, addr, coords):

        if addr not in self.cache:

            # 0 is a not valid data, and will calculate the wrong distance
            # but we need it, because there maybe no data for some addr in
            # first few time or just because the window is too small
            self.cache[addr] = {'rssi': [0], 'coords':coords}
            return True

        return False

    def update(self, data):

        obj = data

        if 'error' in obj:

            return None

        addr = obj['addr']

        if addr not in self.cache:

            print("%s not in cache" % addr)
            return None

        rssi = abs(int(obj['rssi'])) - 40
        self.cache[addr]['rssi'].append(rssi)

        self.cnt += 1

        if (self.cnt >= self.window):

            X, Y = 0, 0
            S = 0

            for addr in self.cache:

                # problem: if window is small, maybe avg will be zero
                avg = sum(self.cache[addr]['rssi']) / len(self.cache[addr]['rssi'])
                X += avg * self.cache[addr]['coords']['x']
                Y += avg * self.cache[addr]['coords']['y']
                S += avg
                # preserve one data for nexttime use
                # in case there are no fresh data and cause avg become zero
                self.cache[addr]['rssi'] = self.cache[addr]['rssi'][-1:]

            X = X / S
            Y = Y / S

            self.cnt = 0

            print(X, Y)
            return {"X": X, "Y": Y}

        else:

            return None


# when get *number* of rssi for each addr, generate an output
class WCLN:

    def __init__(self, number=2):

        self.cache = {}
        self.number = number

    def add(self, addr, coords):

        if addr not in self.cache:

            self.cache[addr] = {'rssi': [], 'coords':coords}
            return True

        return False

    def update(self, data):

        obj = data

        if 'error' in obj:

            return None

        addr = obj['addr']

        if addr not in self.cache:

            print("%s not in cache" % addr)
            return None

        rssi = abs(int(obj['rssi'])) - 40
        self.cache[addr]['rssi'].append(rssi)

        check = False

        for addr in self.cache:

            if (len(self.cache[addr]['rssi']) >= self.number):

                check = True

            else:

                check = False
                break

        if (check):

            X, Y = 0, 0
            S = 0

            for addr in self.cache:

                avg = sum(self.cache[addr]['rssi']) / len(self.cache[addr]['rssi'])
                X += avg * self.cache[addr]['coords']['x']
                Y += avg * self.cache[addr]['coords']['y']
                S += avg
                self.cache[addr]['rssi'] = []

            X = X / S
            Y = Y / S

            # print(X, Y)
            return {"X":X, "Y":Y}

        else:

            return None



class TriangulatorN:

    def __init__(self, number = 10):

        self.cache = {}
        self.number = number

    # need to just add 3 points
    def add(self, addr, coords):

        if addr not in self.cache:

            self.cache[addr] = {'rssi': [], 'coords':coords}
            return True

        return False

    def update(self, data):

        # need 3 addr and their coodinates
        if (len(self.cache.keys()) < 3):

            print('add more address and coords')
            return None

        obj = data

        if 'error' in obj:

            return None

        addr = obj['addr']

        if addr not in self.cache:

            print("%s not in cache" % addr)
            return None

        rssi = abs(int(obj['rssi']))
        self.cache[addr]['rssi'].append(rssi)

        check = False

        for addr in self.cache:

            if (len(self.cache[addr]['rssi']) >= self.number):

                check = True

            else:

                check = False
                break

        if (check):

            d = []

            for addr in self.cache:

                avg = sum(self.cache[addr]['rssi']) / len(self.cache[addr]['rssi'])
                d.append({"distance": rssi2DistanceCSDN(avg), "addr": addr})
                # d.append({"distance": rssi2DistanceGithub(avg), "addr": addr})
                self.cache[addr]['rssi'] = []

            X, Y = self.triangulate(d)
            print(X, Y)
            return {"X": X, "Y": Y}

        else:

            return None

    # https://blog.csdn.net/qq_35651984/article/details/82633843
    def triangulate(self, d):

        d0 = d[0]['distance']
        d1 = d[1]['distance']
        d2 = d[2]['distance']
        p0_x = self.cache[d[0]['addr']]['coords']['x']
        p1_x = self.cache[d[1]['addr']]['coords']['x']
        p2_x = self.cache[d[2]['addr']]['coords']['x']
        p0_y = self.cache[d[0]['addr']]['coords']['y']
        p1_y = self.cache[d[1]['addr']]['coords']['y']
        p2_y = self.cache[d[2]['addr']]['coords']['y']

        print('distance %f, coords (%d, %d)' % (d0, p0_x, p0_y))
        print('distance %f, coords (%d, %d)' % (d1, p1_x, p1_y))
        print('distance %f, coords (%d, %d)' % (d2, p2_x, p2_y))

        a = p0_x-p2_x
        b = p0_y-p2_y
        c = math.pow(p0_x, 2) - math.pow(p2_x, 2) + math.pow(p0_y, 2) - math.pow(p2_y, 2) + math.pow(d2, 2) - math.pow(d0, 2)
        d = p1_x-p2_x
        e = p1_y-p2_y
        f = math.pow(p1_x, 2) - math.pow(p2_x, 2) + math.pow(p1_y, 2) - math.pow(p2_y, 2) + math.pow(d2, 2) - math.pow(d1, 2)
        x = (b*f-e*c)/(2*b*d-2*a*e)
        y = (a*f-d*c)/(2*a*e-2*b*d)
        return x, y

