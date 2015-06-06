import nettest
import json
from datetime import datetime

def report_net_speed(update_requested):

    speedstring = nettest.perform_speedtest()
    netspeed_dict = nettest.parse_speedtest(speedstring) # necessary here?
    nettest.write_speed_log(netspeed_dict)

    report = "Current Internet Speeds:\n" + speedstring

    # if an update is explictly requested or if it's 8:00 on a weekday, publish to Twitter
    if update_requested or (datetime.weekday(datetime.today().date()) < 5 and datetime.today().hour == 8):
        pass  # Twitter API call to publish report goes here 
    
    print report # debug
    print len(report) # debug

def auth_data():

    with open("auth.json", "r") as f:
        data = json.load(f)
    return(data)

def main():
    
    report_net_speed()

if __name__ == '__main__':
    main()
