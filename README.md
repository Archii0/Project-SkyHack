# Project-SkyHack
Project SkyHack is a two part ethical drone hacking session to teach students about network vulnerabilities using drones.
The sessions are meant to be carried out on Kali Linux with the use of Wireshark, aircrack-ng and any text editor that can translate python.

## Session 1 - Drone Control Using Python
The first session teaches students about using APIs and the fundamentals of OOP.


## Session 2 - Drone WiFi Deauthentication Attacks
The second session teaches students about network vulnerabilities, where the goal is to create python script carry out WiFi deauth attacks.

The deauth script has these functionalities:
- Detect nearby data packets being sent from the drones to extract drone AP information
- Using the bssid and channel to find any stationed/client devices on the drone access point
- Sending deauthentication packets to the drone, so all client devices are disconnnected
- Connecting to the drone's access point and using APIs to take control of the drone
