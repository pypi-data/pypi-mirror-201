import paramiko
import time
from .service import debug

available_pwds = {"1": "111111", "2": "111111", "3": "0987654321", "4": "112233", "5": "111111"}

class SshNotConnected(Exception):
    """
    Rases when there is an attempt to comunicate via SSH, but no client is initialised
    """
    pass



class SSH:
    def __init__(self, /, user='youbot', ip="192.168.88.21", password=None, timeout=3, connect=True):
        """
        Connects to KUKA youbot via SSH client and starts ROS
        :param user: youbot by default
        :param ip: youbot ip address
        :param password: 111111 by default
        """
        port = 22
        self.timeout = timeout
        self.connected = connect
        self.ssh_client = paramiko.SSHClient()
        self.ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.last_status = {"ROS": -1, "RGB": -1, "depth": -1, "arm0": -1, "arm1": -1, "lidar": -1, "base": -1}
        if not password and ip[-1] in available_pwds:
            password = available_pwds[ip[-1]]
        if not self.connected:
            return
        try:
            debug("connecting to SSH")
            self.ssh_client.connect(hostname=ip, username=user, password=password, port=port)
        except Exception as err:
            debug(err)
            self.connected = False
            return
        self.ssh_var = self.ssh_client.invoke_shell()
        self.send_wait("sudo -s", "[sudo] password for")
        debug("log as root")
        self.send_wait(password, "root@youbot:")
        debug("logged in")

    def send_wait(self, msg_send, wait_msg, /, timeout=None, timeout_msg=None, verbose=0):
        """
        Sends command to ssh and waits certain for response till timeout
        :param msg_send: command to send
        :param wait_msg: message to wait
        :param timeout: time after which function will be terminated if there is nothing to read
        :param timeout_msg: message that will be printed to prompt in case of timout
        :param verbose: 0 - prints nothing; 1 - prints whole input

        return: whole received message
        """
        if not self.connected:
            raise SshNotConnected
        if not timeout:
            timeout = self.timeout
        init_time = time.time()
        msg = ''
        self.ssh_var.send(msg_send.encode("utf-8") + b"\n")
        while not msg.count(wait_msg):
            if self.ssh_var.recv_ready():
                init_time = time.time()
                read_char = self.ssh_var.recv(1).decode("utf-8")
                if read_char != chr(0):
                    msg += read_char
                    if verbose:
                        debug(read_char, end='')
            else:
                time.sleep(0.001)
            if time.time() - init_time > timeout:
                if timeout_msg != None:
                    debug(timeout_msg, end='')
                else:
                    debug(f"sent \"{msg_send}\" but didn't receive \"{wait_msg}\" in {timeout} seconds. Abort")
                break
        return msg

    def send(self, msg):
        '''
        Sends command to SSH
        '''
        self.ssh_var.send(msg.encode("utf-8") + b"\n")

    def send_recv(self, msg):
        return self.send_wait(msg, "root@youbot:")[:-12]

    def ROS_status(self, verbose=1):
        """
        Connects to KUKA youbot via SSH client and checks rostopics
        :param verbose: 0 - only return; 1 - output info in prompt; 2 - output full response in prompt
        :return ROS, RGB camera and depth camera status
        """
        if not self.connected:
            raise SshNotConnected
        ROS = False
        camera_RGB = False
        camera_depth = False
        rostopic = self.send_wait("rostopic list", "root@youbot:", timeout=10)
        if rostopic.count("ERROR: Unable"):
            if verbose:
                debug("ROS not running")
            self.last_status['ROS'] = 0
            return False, False, False
        else:
            ROS = True
            self.last_status['ROS'] = 1

        if rostopic.count("camera/rgb/image_raw"):
            camera_RGB = True
            if verbose:
                debug("RGB camera is active")
            self.last_status['RGB'] = 1
        else:
            if verbose:
                debug("WARN: RGB camera is inactive")
            self.last_status['RGB'] = 0
        if rostopic.count("camera/depth/image"):
            if verbose:
                debug("depth camera is active")
            self.last_status['depth'] = 1
            camera_depth = True
        else:
            if verbose:
                debug("WARN: depth camera is inactive")
            self.last_status['depth'] = 0
        if verbose == 2:
            debug(rostopic)
        return ROS, camera_RGB, camera_depth

    def launch_ROS(self, verbose=1):
        """
        Lunches or restarts ROS on KUKA youbot via SSH
        """
        if not self.connected:
            raise SshNotConnected
        debug("cleaning screen...")
        self.send_wait("pkill screen", "root@youbot:")
        self.send_wait("screen -S roslaunch", "root@youbot:")
        debug("launching ROS... (it may take up to 20sec)")
        ssh_msg = self.send_wait("roslaunch youbot_tl_test ytl_2arm.launch", "4rfdxc34rc3x", timeout=7, timeout_msg="",
                                 verbose=int(verbose-0.5))
        self.send_wait(chr(1) + chr(4), "root@youbot:", timeout_msg="", timeout=0.1)
        self.send_wait("echo ZaSKaR was here", "root@youbot:", timeout_msg="SSH error, please restart", timeout=1)
        if ssh_msg.count("First ROS iter OK"):
            debug("ROS started\n")
        else:
            debug("ROS startup error!\nplease restart the program")
        ssh_msg = ssh_msg.split('\r')
        ssh_msg.append('')
        ros_error_msg = True
        self.last_status['arm0'] = 1
        self.last_status['arm1'] = 1
        self.last_status['base'] = 1
        prev = False
        if verbose:
            for i in range(len(ssh_msg)):
                if "FATAL" in ssh_msg[i] or "ERROR" in ssh_msg[i]:
                    if ros_error_msg:
                        debug("ROS ERROR MASSAGES:", end='')
                        ros_error_msg = False
                    debug(ssh_msg[i], end='')
                    if "\"youbot-manipulator\"" in ssh_msg[i]:
                        self.last_status['arm0'] = 0
                    if "youbot-manipulator2" in ssh_msg[i]:
                        self.last_status['arm1'] = 0
                    if "base" in ssh_msg[i]:
                        self.last_status['base'] = 0
                    if "Hokuyo" in ssh_msg[i]:
                        self.last_status['lidar'] = 0
                    if ']' not in ssh_msg[i + 1]:
                        debug(ssh_msg[i + 1][1:], end='')
                        prev = True
                elif prev and ']' not in ssh_msg[i + 1]:
                    debug(ssh_msg[i + 1][1:], end='')
                    prev = False
                else:
                    prev = False
        debug('\r')


if __name__ == "__main__":
    test_client = SSH(ip="192.168.88.21")
    test_client.launch_ROS(verbose=1)
    test_client.ROS_status()

