from threading import Timer, Thread, Event

class MyThread(Thread):
    def __init__(self, event):
        Thread.__init__(self)
        self.stopped = event

    def run(self):
        while not self.stopped.wait(10):
            print("my thread")
            # call a function


if __name__ == '__main__':
    stopFlag1 = Event()
    thread1 = MyThread(stopFlag1)

    thread1.start()

    print("other")
    stopFlag2 = Event()
    thread2 = MyThread(stopFlag2)

    thread2.start()    
    # this will stop the timer
    # stopFlag.set()