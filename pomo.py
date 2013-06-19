#! /usr/bin/env python
# -*- encoding: utf8 -*-

"""
A simple command line pomodoro clock. Enter a number of tomatoes, and durations for working and taking breaks. Default durations:

    * Work period: 25 minutes
    * Short rest: 5 minutes
    * Long rest: 15 minutes
"""

import argparse, datetime, time, sys, subprocess
import objc

class Notify(object):
    
    def __init__(self, subtitle, message, title='Pomo'):
        self.title = title
        self.subtitle = subtitle
        self.message = message
        self.NSUserNotification = objc.lookUpClass('NSUserNotification')
        self.NSUserNotificationCenter = objc.lookUpClass('NSUserNotificationCenter')

    def messenger(self):
        notification = self.NSUserNotification.alloc().init()
        notification.setTitle_(self.title)
        notification.setSubtitle_(self.subtitle)
        notification.setInformativeText_(self.message)

        return self.NSUserNotificationCenter.defaultUserNotificationCenter().scheduleNotification_(notification)



class Pomo(object):

    # pass dictionary of paramaters to class, and assign key:value to local variables
    # then, convert time quantifies to seconds
    def __init__(self,params = None):
        self.__dict__.update(params)
        self.work = self.work*60
        self.rest = self.rest*60
    
    def countdown(self,secs):
        while secs >= 0:
            sys.stdout.write("\r%s" % str(datetime.timedelta(seconds=secs)))
            sys.stdout.flush()
            secs -= 1
            time.sleep(1)
        sys.stdout.write("\a")
        sys.stdout.flush()

    def timer_set(self):
        Notify(subtitle='Do it.', message="Get to work.").messenger()
        if self.num > 1:
            for i in range(0,self.num-1):
                self.countdown(self.work)
                Notify(subtitle="Did it.", message="Take a break!", title="Pomo").messenger()
                self.countdown(self.rest)
                Notify(subtitle="Do it again.", message="Back to work!", title="Pomo").messenger()
        self.countdown(self.work)
        Notify(subtitle="Done.", message="Finished {0} pomodoros.".format(self.num), title="Pomo").messenger()
        print "\n\n\n\n"
        

p = argparse.ArgumentParser()

p.add_argument("num", type=int, help="Number of pomodoros. Defaults to 4.", default=4, nargs="?")
p.add_argument("work", type=int, help="Duration of work period. Defaults to 25 minutes.", default=25, nargs="?")
p.add_argument("rest", type=int, help="Duration of rest period. Defaults to 5 minutes.", default=5, nargs="?")

opts = vars(p.parse_args())

if __name__ == "__main__":
    subprocess.call(['clear'])
    pomoTimer = Pomo(opts)
    pomoTimer.timer_set()

