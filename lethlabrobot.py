import argparse
import nettest
import json
import subprocess
import tweepy
from datetime import datetime

def last_update_time(column = "hour"):
    """Retrieves the last time at which the program was run.
    
    Uses tail from coreutils to get the last line of the log.

    Which log column to return is passed in as string parameter.
    """
    times = {"year": 0, "month": 1, "day": 2, "hour":3}

    proc = subprocess.Popen(["tail", "-n 1", "netspeed.log"],
                            stdout = subprocess.PIPE,
                            stderr = subprocess.PIPE
                            )

    proc_out, proc_err = proc.communicate()
    l = proc_out.strip().split(',')
    
    col = times[column]
    out = int(l[col])

    return out

def check_requested():
    
    # To do:
    #   read most recent Twitter post
    #   If "Update Netspeed" is in the last post, then check the time stamp
    #   If time stamp is > last_update_time(), then return True
    #   Else: return False
    pass

def reporter(api, update_hour):
    """Handles checks as to whether a published update is required or not."""
    
    done = last_update_time("hour") >= update_hour
    
    routine = all([datetime.weekday(datetime.today().date()) < 5,
                   datetime.today().hour == update,
                   not done])
    
    report_net_speed(api, routine or update_requested)

def report_net_speed(api, publish):
    """Publishes to Twitter if publish == True
    
    Calls functions from nettest for checking and parsing net speed. 
    """

    speedstring = nettest.perform_speedtest()
    netspeed_dict = nettest.parse_speedtest(speedstring)
    nettest.write_speed_log(netspeed_dict)

    report = "Current Internet Speeds:\n" + speedstring

    if publish:
        api.update_status(report)

    print(report) # debug
    print (len(report)) # debug

def authenticate():
    """Loads user credentials from auth.json in the same directory

    and returns the Twitter API object.
    """

    with open("auth.json", "r") as f:
        data = json.load(f)
    
    auth = tweepy.OAuthHandler(data["consumer_key"], data["consumer_secret"])

    auth.set_access_token(data["access_key"], data["access_secret"])

    api = tweepy.API(auth)

    return api

def arguments():
    """Terminal arguments."""

    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--daily-update-hour', type = int, default = 8)

    return parser.parse_args()

def main():
    
    args = arguments()
    api = authenticate()
    reporter(api, args.update_hour)

if __name__ == '__main__':
    main()

