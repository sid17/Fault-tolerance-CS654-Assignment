Github link for the project [https://github.com/sid17/Fault-tolerance-CS654-Assignment]

#Problem Statement 
## Fault-tolerance-CS654-Assignment
Fault Detection:	
Implement two availability tactics for fault detection:
1. ping-echo: Machine A continuously ping to machine B and machine B responds within predefined time. If machine A fails to get an echo from machine B, it reports the fault. 
2. heartbeat: A component periodically emits a heartbeat message, and another component listens to it. If the listening component does not find the heartbeat message within predefined time, it reports the fault. 

# Dependencies:
python-pip [sudo apt-get install python-pip] <br />
python-dev [sudo apt-get install python-dev] <br />
twisted    [sudo pip install twisted] <br />


# Running Instructions
### ping-echo: 
the machine running the client continuously pings the machine with the specified IP address at a predefined time interval. It returns positive resposnse in case the ping was successful else prints an error message. The given functionality uses the pre-defined system command 'ping'. The client is built upon twisted (python based network module) and schedules an event at specific interval of time to provide the desired functionality.

### Usage:
	 python client.py host:port --job ping <br /> <br />
	where host refers to the host for the machine to ping and any random valid port for the port. (Note: The choice of the port does not 		matter since ping does not require a port. Since the given client also provides an option to check heartbeat, we sticked to the given 		format)
<br />
###heartbeat:
	 machine A sends a heartbeat to machine B at predefined interval and machine B continuously listens the heartbeat to detect fault in machine B. If a process id is pre-specified then machine A send the heartbeat for this process else it sends the heartbeat for the VM in general.
<br />
### Usage:
### Machine B:
       python client.py host:port --job hb --pid 1234 (if pid is known) <br />
       python client.py host:port --job hb --pid chrome (to monitor by name) <br />
	<br /> 
	where host:port refers to the machine to monitor and pid refers to the process id/name of the process to monitor.
	(Note: pid is an optional field) <br />

### Machine A: 
	python server.py --port [port no] --iface [IP] <br /> <br />
	the port and iface are optional arguements <br />
	default port is a random port availabale to the process <br />
	default IP adress for the server is 127.0.0.1 [localhost] <br />
<br />
To run both the utilities simultaneously at the client,  <br />
	Usage: <br />
	python client.py host:port --job all --pid 1234 <br />
	python client.py host:port --job all --pid chrome <br /> <br />
	(Note pid is an optional field)
	
