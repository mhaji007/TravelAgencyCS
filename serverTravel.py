
''' Mehdi Hajikhani
    Panther Id NO. 5594946'''
import sys
import socket
import threading

host = '127.0.0.1'
port = 10000
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

flightList = []

flightDataList = [('NYC', 'LAX', 10, 300),
                  ('MIA', 'ORL', 50, 400),
                  ('LAG', 'MIA', 50, 500),
                  ('HNS', 'PHX', 40, 400),
                  ('PHX', 'ORL', 50, 500),
                  ('ALB', 'DFX', 40, 400),
                  ('LAX', 'ORL', 30, 100),
                  ('CVG', 'PIE', 20, 300),
                  ('SFO', 'DCA', 10, 500),
                  ('TPA', 'ACT', 20, 600),
                  ('WAS', 'MIA', 30, 300),
                  ('LAX', 'SFO', 40, 200),
                  ('OAK', 'ACK', 50, 500),
                  ('NYC', 'ORF', 60, 300),
                  ('MIA', 'NYC', 70, 200),
                  ('MSP', 'MEM', 80, 400),
                  ('LEB', 'KOA', 90, 300),
                  ('JAX', 'MKL', 80, 200),
                  ('JST', 'ORL', 70, 100),
                  ('MCI', 'FLL', 60, 400),
                  ('MIA', 'FLL', 50, 700),
                  ('DTT', 'COD', 40, 300),
                  ('COS', 'AUS', 30, 200),
                  ('CLT', 'PIE', 20, 100),
                  ('CLE', 'ELD', 10, 500),
                  ('NYC', 'FLL', 20, 600),
                  ('ELP', 'DFW', 30, 400),
                  ('HNL', 'IDA', 40, 300),
                  ('JAN', 'LMT', 40, 300),
                  ('LAF', 'LMB', 60, 400),
                  ('MRY', 'SNI', 70, 500),
                  ('PSP', 'UIN', 80, 700),
                  ('SRQ', 'GEG', 90, 300),
                  ('SAN', 'TLH', 80, 200),
                  ('FLL', 'PIE', 70, 600),
                  ('VCT', 'WSX', 60, 600),
                  ('YAM', 'GNV', 50, 400),
                  ('ATL', 'LBC', 40, 300),
                  ('ELP', 'ELM', 30, 200),
                  ('JAX', 'LAX', 30, 200),
                  ('DTW', 'RDU', 10, 300),
                  ('CHO', 'BTT', 20, 200),
                  ('BKX', 'CMI', 30, 300),
                  ('OAK', 'ORD', 40, 200),
                  ('AUG', 'NYC', 50, 400),
                  ('ASE', 'MIA', 60, 500),
                  ('BOS', 'CLT', 70, 300),
                  ('ORD', 'IRC', 90, 400),
                  ('FLL', 'COU', 150, 200),
                  ('CZN', 'KCL', 80, 90)
                  ]


class Flight():
    def __init__(self, src, dst, fc, rc, prc):
        self.source = src
        self.destination = dst
        self.forwardCount = fc
        self.reverseCount = rc
        self.price = prc
        self.threadLock = threading.Lock()

    def reserveForwardTicket(self, numberOfTicket):
        self.threadLock.acquire()
        if self.forwardCount >= numberOfTicket:
            self.forwardCount -= numberOfTicket
            self.threadLock.release()
            return ("\nCongratulations! Your transaction was successful.")
        else:
            self.threadLock.release()
            return ("\nSorry! You may not buy " + str(
                numberOfTicket) + " from " + self.source + " to " + self.destination + "\nAvailable Tickets are " + str(
                self.forwardCount) + "!\n")

    def reserveReverseTicket(self, numberOfTicket):
        self.threadLock.acquire()
        if self.reverseCount >= numberOfTicket:
            self.reverseCount -= numberOfTicket
            self.threadLock.release()
            return ("\nCongratulations! Your transaction was successful.")
        else:
            self.threadLock.release()
            return ("\nSorry! You may not buy " + str(
                numberOfTicket) + " from " + self.destination + " to " + self.source + "\nAvailable Tickets are " + str(
                self.reverseCount) + "!\n")

    def reserveReturnTicket(self, numberOfTicket):
        self.threadLock.acquire()
        if self.forwardCount >= numberOfTicket:
            if self.reverseCount >= numberOfTicket:
                self.forwardCount -= numberOfTicket
                self.reverseCount -= numberOfTicket
                self.threadLock.release()
                return ("\nCongratulations! Your transaction was successful.")
        self.threadLock.release()
        return ("\nSorry! You may not buy return tickets for the route due to heavy traffic")

    def getFlightData(self):
        return ("\n " + self.source + "=>" + self.destination + ": Available Tickets = " + str(
            self.forwardCount) + "\n " + self.destination + "=>" + self.source + ": Available Tickets = " + str(
            self.reverseCount))

    def getForwardInfo(self):
        return "\n" + self.source + "=>" + self.destination + " Number of available tickects " + str(self.forwardCount)

    def getReverseInfo(self):
        return "\n" + self.destination + "=>" + self.source + " Number of available tickects " + str(self.reverseCount)


for data in flightDataList:
    flightList.append(Flight(data[0], data[1], data[2], data[2], data[3]))
# s.connect((host,port))
s.bind((host, port))
s.listen(5)
clientList = []
msgList = []
nameAddress = {}


def dealClient(c, addr):
    while True:
        # data received from client
        try:
            data = c.recv(1024)
            data = data.decode()
            data = data.upper()
            msg = 'invalid request!'
            if data:
                if data.startswith('LIST'):
                    for m in getList():
                        sendMessageToClient(m, c)
                    continue
                elif data.startswith('SEARCHD'):
                    req = data.split()
                    for m in searchDestination(req[1]):
                        sendMessageToClient(m, c)
                    continue
                elif data.startswith('SEARCHALL'):
                    req = data.split()
                    for m in searchAllDestination(req[1]):
                        sendMessageToClient(m, c)
                    continue
                elif data.startswith('SEARCHS'):
                    req = data.split()
                    for m in searchDeparture(req[1]):
                        sendMessageToClient(m, c)
                    continue
                elif data.startswith('BUY_TICKET'):
                    try:
                        req = data.split()
                        msg = reserveTicket(req[1], int(req[2]))
                    except Exception as e:
                        print(e)
                        break
                elif data.startswith('BUYRT_TICKET') or data.startswith('RETURN_TICKET') or data.startswith(
                        'RETURNRT_TICKET'):
                    try:
                        req = data.split()
                        msg = reserveReturnTicket(req[1], int(req[2]))
                    except Exception as e:
                        print(e)
                        break
                elif data.startswith('QUIT'):
                    c.close()
                    break
            sendMessageToClient(msg, c)
        except Exception as e:
            print(e)
            # print('deal client')
            c.close()
            break


def sendMessageToClient(msg, c):
    try:
        c.send(msg.encode())
    except Exception as e:
        # print('send msg')
        # print(e)
        # print('unable to send message to ',str(c),str(e))
        print(e)


def getList():
    fl = []
    for f in flightList:
        # fl = fl + f.getFlightData()
        fl.append(f.getFlightData())
    return fl


def searchDestination(dest):
    dl = []
    dest = dest[-3:]
    # print(dest)
    for f in flightList:
        if f.destination == dest:
            # dl = dl + f.getForwardInfo()
            dl.append(f.getForwardInfo())
        elif f.source == dest:
            # dl = dl + f.getReverseInfo()
            dl.append(f.getReverseInfo())
    return dl


def searchAllDestination(dest):
    dl = []
    for f in flightList:
        if f.destination == dest or f.source == dest:
            # dl = dl + f.getForwardInfo()
            # dl = dl + f.getReverseInfo()
            dl.append(f.getForwardInfo())
            dl.append(f.getReverseInfo())
    return dl


def searchDeparture(src):
    dl = []
    for f in flightList:
        if f.destination == src:
            # dl = dl + f.getReverseInfo()
            dl.append(f.getReverseInfo())
        elif f.source == src:
            # dl = dl +f.getForwardInfo()
            dl.append(f.getForwardInfo())
    return dl


def reserveTicket(info, numberOfTicket):
    src = info[0:3]
    dest = info[4:7]
    record = ''
    for f in flightList:
        if f.source == src and f.destination == dest:
            record = f.reserveForwardTicket(numberOfTicket)
            break
        elif f.destination == src and f.source == dest:
            record = f.reserveReverseTicket(numberOfTicket)
            break
    return record


def reserveReturnTicket(info, numberOfTicket):
    src = info[0:3]
    dest = info[4:7]
    record = ''
    for f in flightList:
        if f.source == src and f.destination == dest:
            record = f.reserveReturnTicket(numberOfTicket)
            break
        elif f.destination == src and f.source == dest:
            record = f.reserveReturnTicket(numberOfTicket)
            break
    return record


while True:
    print('Server is listening.......')
    c, addr = s.accept()
    threading._start_new_thread(dealClient, (c, addr))