import argparse
import nettest
import json
from datetime import datetime

def reporter(update_hour):

    # update_requested = check if an update has been requested via Twitter
    # done = determine if a routine check has been performed today
    # See if the routine check has been performed by reading the logs (tail -n 1 might be easiest)
    publish = False

    if datetime.today().hour <
    routine = all([datetime.weekday(datetime.today().date()) < 5 ,datetime.today().hour == update, not done])
    
    if update_requested or routine:
        
def report_net_speed(publish):

    speedstring = nettest.perform_speedtest()
    netspeed_dict = nettest.parse_speedtest(speedstring) # necessary here?
    nettest.write_speed_log(netspeed_dict)

    report = "Current Internet Speeds:\n" + speedstring

    # if publish, then write to twitter
    
    print report # debug
    print len(report) # debug

def auth_data():

    with open("auth.json", "r") as f:
        data = json.load(f)
    return(data)

def arguments():

    parser = argparse.ArgumentParser()
    parser.add_argument('-h', '--daily-update-hour', type = int, default = 8)

    return parser.parse_args()

def main():
    
    args = arguments()
    reporter(args.update_hour)

if __name__ == '__main__':
    main()
