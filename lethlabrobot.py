import argparse
import nettest
import json
import subprocess
import tweepy
from datetime import datetime

def last_update_time():

    proc = subprocess.Popen(["tail", "-n 1", "netspeed.log"],
                            stdout = subprocess.PIPE,
                            stderr = subprocess.PIPE
                            )

    proc_out, proc_err = proc.communicate()
    l = proc_out.strip().split(',')

    out = int(l[3])

    return out

def check_requested():
    
    # To do:
    #   read most recent Twitter post
    #   If "Update Netspeed" is in the last post, then check the time stamp
    #   If time stamp is > last_update_time(), then return True
    #   Else: return False
    pass

def reporter(api, update_hour):

    # update_requested = check if an update has been requested via Twitter
    # done = determine if a routine check has been performed today
    # See if the routine check has been performed by reading the logs (tail -n 1 might be easiest)
    
    done = last_update_time() >= update_hour
    routine = all([datetime.weekday(datetime.today().date()) < 5 ,datetime.today().hour == update, not done])
    
    report_net_speed(api, routine or update_requested)

def report_net_speed(api, publish):

    speedstring = nettest.perform_speedtest()
    netspeed_dict = nettest.parse_speedtest(speedstring) # necessary here?
    nettest.write_speed_log(netspeed_dict)

    report = "Current Internet Speeds:\n" + speedstring

    # if publish is True, then write to twitter
    if publish:
        api.update_status(report)

    print report # debug
    print len(report) # debug

def authenticate():

    with open("auth.json", "r") as f:
        data = json.load(f)
    
    auth = tweepy.OAuthHandler(data["consumer_key"], data["consumer_secret"])

    auth.set_access_token(data["access_key"], data["access_secret"])

    api = tweepy.API(auth)

    return api

def arguments():

    parser = argparse.ArgumentParser()
    parser.add_argument('-h', '--daily-update-hour', type = int, default = 8)

    return parser.parse_args()

def main():
    
    args = arguments()
    api = authenticate()
    reporter(api, args.update_hour)

if __name__ == '__main__':
    main()
