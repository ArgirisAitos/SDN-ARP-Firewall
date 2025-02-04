# SDN-ARP-Firewall


# Description 
This project implements a Software-Defined Networking (SDN) solution to detect and prevent ARP Spoofing attacks. Using the Ryu controller and Mininet, it monitors ARP traffic and maintains a predefined ARP table to validate MAC-IP mappings. If an inconsistency is detected, the controller logs a warning and blocks the malicious packets.


# Features:

- ARP request/reply monitoring in an SDN enviroment.
- Static ARP table to prevent spoofing attacks.
- Dynamic detection of unauthorized MAC-IP changes.
- OpenFlow-based packet forwarding.


 # Requirements 

 - Mininet
 - Ryu controller



# Network Topology
 The network consists of:

 - 4 hosts (h1,h2,h3,h4)
 - 1 OpenFlow switch (s1)
 - Ryu controller managing the firewall rules.

![miniedit](https://github.com/user-attachments/assets/45d6f274-2c6c-4b2c-92a1-abeed99c72dc)


# Setup Instructions 

1. Clone this repository 
```bash 

https://github.com/ArgirisAitos/SDN-ARP-Firewall

```

2. Install Dependecies

 ```bash

  pip install ryu 

  ```
  ```bash

  sudo pip3 install mininet 
  
  ```

  3. **Start Mininet with the Custom Topology**

  ```bash

  sudo python topology.py 
  
  ```
4. Run the Ryu Controller 

  ```bash 

  ryu-managerv FirewallARP.py

  ```

  5. Test ARP Spoofing Prevention 


     # ARP Spoofing Attempt

   Try to send a fake ARP reply from  h3:

     ```bash
     mininet> h1 arpspoof -i h1-eth0 -t 10.0.0.2 10.0.0.3 
     ```
      
      ## The controller logs a warning and blocks the attack.














