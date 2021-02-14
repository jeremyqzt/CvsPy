from time import time
from threading import Thread

maxCount = 50000000
def count(amt):
    while amt:
        amt-=1

start = time()
count(maxCount)
end = time()

print("How long (Non-Threaded): %f" % (end-start))

class ThreaderCounter(Thread):
    def __init__(self, count):
        Thread.__init__(self)
        self.count = count

    def run(self):
        while self.count:
            self.count-=1

thStart = time()

ThCount = 4
threadArr = []
for i in range(0,ThCount - 1):
    th = ThreaderCounter(round(maxCount/ThCount))
    th.start()
    threadArr.append(th)

for item in threadArr:
    item.join()
thEnd = time()
print("How long (Threaded): %f" % (thEnd-thStart))

