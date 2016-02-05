# Fault-tolerance-CS654-Assignment
Fault Detection:	
Implement two availability tactics for fault detection:   
1. ping-echo: Machine A continuously ping to machine B and machine B responds within predefined time. If machine A fails to get an echo from machine B, it reports the fault.    
2. heartbeat: A component periodically emits a heartbeat message, and another component listens to it. If the listening component does not find the heartbeat message within predefined time, it reports the fault. 
