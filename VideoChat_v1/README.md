# SLIC3D

Collab: Elastic Spaces<br>
Fall 2020<br>
Parsons School of Design x UC Boulder<br>

## Installation

To install required libraries run
```
pip3 install -r requirements.txt
```

### In one session
```
python server.py
```

### Another session
```
python client.py [optional ip]
```

For example, if you are doing locally
```
python client.py
```

If the server is on a remote machine
```
python client.py {server-ip}
```

### List Available Cameras
```
python client.py
```

Sample Output
```
Port 0 is working and reads images (720.0 x 1280.0)
Port 1 for camera ( 720.0 x 1280.0) is present but does not reads.
OpenCV: out device of bound (0-1): 2
OpenCV: camera failed to properly initialize!
Port 2 is not working.
```