
##    pip install paramiko scp

#
#
# 
#

import paramiko
from scp import SCPClient
import sys

def progress(filename, size, sent):
    sys.stdout.write("%s's progress: %.2f%%   \r" % (filename, float(sent)/float(size)*100))
    sys.stdout.flush()

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy()) # Or use WarningPolicy for stricter security

# Path to your private key file
private_key_path = "/home/a/.ssh/id_rsa" 

# Load the private key
private_key = paramiko.RSAKey.from_private_key_file(private_key_path) 

# Connect to the remote server
ssh.connect(hostname="192.168.1.250", username="a", pkey=private_key)


# Create SCPClient instance with a progress callback
# with SCPClient(ssh.get_transport(), progress=progress) as scp:
with SCPClient(ssh.get_transport()) as scp:
    scp.put('/home/a/vision_movement_files/10_22_14_29_57_Movement.avi', 'D:/Tree_video')
    print("\nFile copy complete!") # Newline after progress updates

ssh.close()