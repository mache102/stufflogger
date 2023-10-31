import configargparse 
import os 
import threading 

from keylogger import KeyLogger
from process_monitor import ProcessMonitor
from screenshotter import Screenshotter

from util import setup_logger, get_monitor

def parse_args():
    parser = configargparse.ArgumentParser(description='stuff logger')

    parser.add_argument("--config", is_config_file=True,
                        help="Path to config file")
    parser.add_argument("--log_path", type=str, default="logs/",
                        help="Path to save logs")
    
    # keylogger
    parser.add_argument("--keylog", action="store_true",
                        help="Enable keylogger")
    
    # screenshotter
    parser.add_argument("--ss", action="store_true",
                        help="Enable screenshotter")
    parser.add_argument("--ss_path", type=str, default="screenshots/",
                        help="Path to save screenshots")
    parser.add_argument("--ss_interval", type=int, default=5,
                        help="Interval between screenshots")
    parser.add_argument("--ss_resolution_factor", type=float, default=0.05,
                        help="Screenshot resolution factor")
    
    # process monitor
    parser.add_argument("--pm", action="store_true",
                        help="Enable process monitor")
    parser.add_argument("--pm_interval", type=int, default=1,
                        help="Interval between process monitor checks")
    
    return parser.parse_args()

def keylogger_thread():
    logger = setup_logger(args.log_path, "keylogger")
    kl = KeyLogger(logger)
    kl.start()
    kl.keyboard_listener.join()

def main():
    os.makedirs(args.log_path, exist_ok=True)

    # keylogger
    if args.keylog:
        kl = threading.Thread(target=keylogger_thread)
        kl.start()

    # screenshotter
    if args.ss:
        os.makedirs(args.ss_path, exist_ok=True)
        ss_logger = setup_logger(args.log_path, name='screenshotter')
        m = get_monitor()
        ssman = Screenshotter(logger=ss_logger, save_path=args.ss_path, 
                            interval=args.ss_interval, resolution=(m.width, m.height), 
                            resolution_factor=args.ss_resolution_factor)
        ssman.start()

    # process monitor
    if args.pm:
        pm_logger = setup_logger(args.log_path, name='process_monitor')
        pm = ProcessMonitor(logger=pm_logger, interval=args.pm_interval)
        pm.start()

if __name__ == '__main__':
    args = parse_args()
    main()