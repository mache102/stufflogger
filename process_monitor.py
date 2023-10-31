import datetime
import logging
import os  
import psutil 
import time 
import threading 

class ProcessMonitor:
    def __init__(self, logger, interval):
        """
        monitor processes and log when processes are updated
        """
        self.logger = logger
        self.interval = interval

        self.username = os.getlogin()
        self.processes = self.get_processes()

        self._active = False 
        self.thread = threading.Thread(target=self.main)

    def get_processes(self, initial=False):
        """
        Retrieve list of processes
        if initial=True, log all processes and their status
        """
        processes = {}

        if initial:
            logging.info("Outputting initial process list!")

        for p in psutil.process_iter(["pid", "ppid", "name", "status", "username"]):
            process = {k:v for k,v in p.__dict__.items()} # copy process info
            process.update(process["info"])
            del process["info"]
            if process["username"] != self.username: # not current user
                continue 
            if process["ppid"] == 0 or process["ppid"] == 1: # system process
                continue

            pid = process.pop("pid")
            if initial:
                logging.info(f"{pid}: {process}")
            processes[pid] = process

        return processes

    @property 
    def active(self):
        return self._active

    def start(self):
        if not self._active:
            self._active = True 
            self.thread.start()
            self.logger.info("Start process monitor")

    def stop(self):
        if self._active:
            self._active = False 
            self.thread.join()
            self.logger.info("Stop process monitor")

    def main(self):
        """Monitor processes"""
        while True:
            if not self._active:
                continue
            new_plist = self.get_processes()

            new_pids = [pid for pid in new_plist if pid not in self.processes]
            removed_pids = [pid for pid in self.processes if pid not in new_plist]

            if len(new_pids) > 0:
                self.logger.info("New processes: ")
                for pid in new_pids:
                    process = new_plist[pid]
                    # from unix timestamp to datetime object
                    create_time = datetime.datetime.fromtimestamp(process["_create_time"])
                    seconds_since_created = (datetime.datetime.now() - create_time).seconds
                    self.logger.info(f"{pid} - {process['name']} - {process['status']} - created {seconds_since_created} seconds ago")

            if len(removed_pids) > 0:
                self.logger.info("Removed processes: ")
                for pid in removed_pids:
                    process = self.processes[pid]
                    uptime = datetime.datetime.now() - datetime.datetime.fromtimestamp(process["_create_time"])
                    self.logger.info(f"{pid} - {process['name']} - uptime {uptime}")

            self.processes = new_plist
            time.sleep(self.interval)

