# SDN-ARP-Firewall


# Description 
This project implements a Software-Defined Networking (SDN) solution to detect and prevent ARP Spoofing attacks. Using the Ryu controller and Mininet, it monitors ARP traffic and maintains a predefined ARP table to validate MAC-IP mappings. If an inconsistency is detected, the controller logs a warning and blocks the malicious packets.


# Features:

- ARP request/reply monitoring in an SDN enviroment.
- Static ARP table to prevent spoofing attacks.
- Dynamic detection of unauthorized MAC-IP changes.
- OpenFlow-based packet forwarding.


