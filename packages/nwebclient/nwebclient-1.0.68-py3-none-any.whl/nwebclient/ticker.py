import time
import os
import os.path

class Process:
    name = 'process'
    cpu = None
    def __init__(self, name='Process'):
        self.name = name
    def tick(self):
        pass
    def cmd(self, args):
        return False

class CmdEcho(Process):
    def __init__(self):
        super().__init__('CmdEcho')
    def cmd(self, args):
        print("CMD: " + ' '.join(args))
        return False

class Ticker(Process):
    last = 0
    interval = 10
    def __init__(self, name = 'ticker', interval = 15):
        super().__init__(name) 
        self.interval = interval
    def tick(self):
        t = int(time.time())
        dur = t - self.last;
        if dur > self.interval:
            self.last = t
            self.execute()
    def cmd(self, args):
        if args[0]==self.name and args[1]=='set_interval':
            self.interval = int(args[2])
            return true
        return super().cmd(args)
    def execute(self):
        pass

class FileExtObserver(Ticker):
    def __init__(self, name = 'ext_observer', ext='.sdjob', interval = 15):
        super().__init__(name=name, interval=interval) 
        self.ext = ext
    def processFile(self, filename):
        pass
    def execute(self):
        filelist = [ f for f in os.listdir('.') if f.endswith(self.ext) ]
        for f in filelist:
            print(self.name + ": Found file: "+ f)
            self.processFile(f)

class UrlDownloader(Ticker):
    """
      Laedt periodisch eine URL in eine Datei
    """
    def __init__(self, name = 'UrlDownloader', interval = 3600, url='https://bsnx.net/4.0/', filename='data.txt', fail_on_exists = True):
        super().__init__(name, interval) 
        self.url = url
        self.filename = filename
        self.fail_on_exists = fail_on_exists
    def execute(self):
        res = requests.get(self.url)
        if not (os.path.isfile(self.filename) and self.fail_on_exists):
            with open(self.filename, 'w') as f:
                f.write(self.filename)


class UrlPostShTicker(Ticker):
    """
      Sendet Daten an einen POST-Endpoint
    """
    uptime_counter = 0
    def __init__(self, name = 'UrlPostShTicker', interval = 7200, url='https://bsnx.net/4.0/'):
        super().__init__(name, interval) 
        self.url = url  
    def execute(self):
        self.uptime_counter = self.uptime_counter + self.interval
        t = time.localtime()
        current_time = time.strftime("%H:%M:%S", t)
        requests.post(self.url, data={'uptime': str(self.uptime_counter)+"s up, "+current_time})


class Cpu:
    processes = []
    sleep_time = 1
    def __init__(self, *args):
        for arg in args:
            self.add(arg)
    def __iter__(self):
        return self.processes.__iter__()
    def add(self, process):
        process.cpu = self
        self.processes.append(process)
    def tick(self):
        for p in self.processes:
            p.tick()
        if self.sleep_time > 0:
            time.sleep(self.sleep_time)
    def cmd(self, args):
        for p in self.processes:
            p.cmd(args)
    def loop(self):
        while True:
            self.tick()
    def runTicks(self, count=100) :
        for i in range(count):
             self.tick()

