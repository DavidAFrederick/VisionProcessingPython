import paramiko
from scp import SCPClient, SCPException
import socket
import sys

# Replace with your own connection details
hostname = '192.168.1.250'
username = 'a'
private_key_path = "/home/a/.ssh/id_rsa" 
local_directory ='/home/a/vision_movement_files/'
local_file_name = '10_18_22_30_39_Movement.avi'
local_path = local_directory + local_file_name
remote_path = 'D:/Tree_video'

ssh_client = paramiko.SSHClient()
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
private_key = paramiko.RSAKey.from_private_key_file(private_key_path) 


def progress(filename, size, sent):
    sys.stdout.write("%s's progress: %.2f%%   \r" % (filename, float(sent)/float(size)*100))
    sys.stdout.flush()

try:
    # 1. Establish the SSH connection
    ssh_client.connect(hostname, username=username, pkey=private_key)
    print("SSH connection established.")

    # 2. Create an SCP client using the SSH transport
    with SCPClient(ssh_client.get_transport(), progress=progress) as scp:
        # 3. Transfer the file
        print(f"Transferring {local_path} to {remote_path}...")
        scp.put(local_path, remote_path)
        print("File transfer successful.")

except paramiko.ssh_exception.AuthenticationException as e:
    print(f"Authentication failed: {e}")
except paramiko.ssh_exception.SSHException as e:
    print(f"SSH connection error: {e}")
except SCPException as e:
    print(f"SCP transfer failed: {e}")
except FileNotFoundError:
    print(f"Local file not found: {local_path}")
except socket.timeout:
    print("Connection timed out.")
except Exception as e:
    print(f"An unexpected error occurred: {e}")

finally:
    # 4. Ensure the SSH connection is closed
    if ssh_client:
        ssh_client.close()
        print("SSH connection closed.")

