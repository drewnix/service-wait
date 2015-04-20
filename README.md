# service-wait
A script that simply blocks until a service starts and binds to a port. This 
is often useful in automation where a script or test needs to wait until a 
specific service comes on line.

Usage is:

```
service-wait.py [-t <timeout>] <host> <port>
```
