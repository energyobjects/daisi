import os, platform, subprocess, re

def get_cpuinfo():
    if platform.system() == "Linux":
        command = "cat /proc/cpuinfo"
        all_info = subprocess.check_output(command, shell=True).decode().strip().replace('\n', '<br/>')
        return all_info
    return ""

def get_cwd():
    return os.getcwd()
    
def get_df():
    if platform.system() == "Linux":
        command = "df"
        all_info = subprocess.check_output(command, shell=True).decode().strip().replace('\n', '<br/>')
        return all_info
    return ""

def get_ps():
    if platform.system() == "Linux":
        command = "ps -ef"
        all_info = subprocess.check_output(command, shell=True).decode().strip().replace('\n', '<br/>')
        return all_info
    return ""

def get_hostname():
    if platform.system() == "Linux":
        command = "hostname"
        all_info = subprocess.check_output(command, shell=True).decode().strip().replace('\n', '<br/>')
        return all_info
    return ""

def get_processor_name():
    if platform.system() == "Windows":
        return platform.processor()
    elif platform.system() == "Darwin":
        os.environ['PATH'] = os.environ['PATH'] + os.pathsep + '/usr/sbin'
        command ="sysctl -n machdep.cpu.brand_string"
        return subprocess.check_output(command).strip()
    elif platform.system() == "Linux":
        command = "cat /proc/cpuinfo"
        all_info = subprocess.check_output(command, shell=True).decode().strip()
        for line in all_info.split("\n"):
            if "model name" in line:
                return re.sub( ".*model name.*:", "", line,1)
    return ""