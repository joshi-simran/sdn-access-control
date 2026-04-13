# SDN-Based Access Control System
**Computer Networks | SDN Mininet Simulation**

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

### Test 1: Authorized Hosts Communication (h1 → h2)
> h1 and h2 successfully ping each other — whitelist rule working correctly.
<img width="663" height="209" alt="image" src="https://github.com/user-attachments/assets/b8d5333d-6942-4349-b154-7e7461bd8659" />

### Test 2: Unauthorized Host Blocked (h3 → h1)
> h3 gets 100% packet loss — deny rule working correctly.
<img width="749" height="230" alt="image" src="https://github.com/user-attachments/assets/50c49cdb-d40a-4f35-b7a8-577003fee26c" />

### Test 3: Full Network Ping Test (pingall)
> h1 ↔ h2 reachable, h3 completely blocked — 66% dropped as expected.
<img width="426" height="139" alt="image" src="https://github.com/user-attachments/assets/75854eea-461e-4f31-b6be-d1ad076263ac" />

### Test 4: OpenFlow Flow Table (ovs-ofctl dump-flows s1)
> Flow rules installed by POX controller on switch s1.
<img width="745" height="544" alt="image" src="https://github.com/user-attachments/assets/2d8e676f-69a1-42bf-832c-3e014f180000" />

## References
- Mininet: http://mininet.org
- POX Controller: https://github.com/noxrepo/pox
- OpenFlow 1.0 Specification
