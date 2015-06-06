import subprocess, os
from datetime import datetime

def perform_speedtest():

    proc = subprocess.Popen(["speedtest", "--simple"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    out, err = proc.communicate()

    return out

def parse_speedtest(speedstring):

    output_dict = {}

    items = speedstring.strip().split("\n")

    for item in items:
        key, value = item.split(": ")
        output_dict[key] = value[:value.find(" ")]
    
    rightnow = datetime.today()
    output_dict["Year"] = rightnow.year
    output_dict["Month"] = rightnow.month
    output_dict["Day"] = rightnow.day
    output_dict["Hour"] = rightnow.hour

    return output_dict

def write_speed_log(output_dict):

    logname = "netspeed.log"
    header = ""
    
    if not os.access(logname, os.F_OK):
        header = "Year,Month,Day,Hour,Ping,Upload,Download\n"

    with open(logname, "a") as f:
        
        row = "{}{},{},{},{},{},{},{}\n".format(
                                       header,
                                       output_dict["Year"],
                                       output_dict["Month"],
                                       output_dict["Day"],
                                       output_dict["Hour"],
                                       output_dict["Ping"],
                                       output_dict["Upload"],
                                       output_dict["Download"]
                                       )

        f.write(row)
