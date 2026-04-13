# SDN-Based Access Control System
**Course Project | SDN Mininet Simulation**

## Problem Statement
Implement an SDN-based Access Control System where only whitelisted 
hosts can communicate. Unauthorized hosts are blocked using OpenFlow 
flow rules installed by a POX controller.

## Topology
- h1 (10.0.0.1) - AUTHORIZED
- h2 (10.0.0.2) - AUTHORIZED
- h3 (10.0.0.3) - BLOCKED
- s1 - OVS Switch
- POX Controller (127.0.0.1:6633)

## Setup & Execution Steps

### Requirements
- Ubuntu with Mininet installed
- POX Controller (https://github.com/noxrepo/pox)
- Python 3

### Installation
```bash
git clone https://github.com/noxrepo/pox
cp access_control.py ~/pox/ext/
```

### Run Controller (Terminal 1)
```bash
cd ~/pox
python3 pox.py log.level --DEBUG access_control
```

### Run Topology (Terminal 2)
```bash
sudo python3 topology.py
```

## Test Scenarios

### Test 1 - Allowed Traffic (h1 <-> h2)
```bash
mininet> h1 ping -c 3 h2
```
Expected: Ping succeeds

### Test 2 - Blocked Traffic (h3 blocked)
```bash
mininet> h3 ping -c 3 h1
```
Expected: 100% packet loss

### Test 3 - Flow Table
```bash
mininet> sh ovs-ofctl dump-flows s1
```

## Expected Output
- h1 <-> h2: reachable
- h3 -> anyone: BLOCKED
- pingall shows 66% dropped (only h3 traffic blocked)

## Proof of Execution
[Add your screenshots here]

## References
- Mininet: http://mininet.org
- POX Controller: https://github.com/noxrepo/pox
- OpenFlow 1.0 Specification
