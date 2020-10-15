### How to launch and use the system

Use ubuntu servers for the storage. 
For each of them:
- install python3 (if it is missing)
- load file_server.py (it is better to load it as a service so it would start automatically when the machine starts to work)
- run file_server.py

In the name server:
- install python3 (if it is missing)
- load start.py
- run start.py (it will create some config files)
- load name_server.py
- run name_server.py

On the client machine, write the "python 3 client.py (name server ip as a parameter)" in the prompt shell.


### Design choices

We used flat naming in the storage servers.

Replication is done on each creation/upload/deletion of the files. Replicas are sent to all the active storage servers. To check if the service is active we try to connect to its socket. If it denies the connection, we treat the server as unactive.

We used python sockets as a mean of communication between all the parts of our distributed system.

Fault tolerance was not implemented.


### Problems with Google Cloud Platform

We were unable to run the application on the servers because we were unable to open the required ports.

We tried to use utilities netstat and iptables.


### Participants’ contribution

We were both equally involved in thinking through the architecture of the project. Roughly speaking of the actual development of it, Vyacheslav did the client and the storage servers side, Nadezhda did the naming server. However, we did not divide these tasks explicitly, and, instead, worked together on them.