from srivastav.conversion import Convert
import platform
import psutil
import socket
import os


class Server:
    def __init__(self):
        self.convert = Convert()
        pass

    def get_info(self):
        physical_memory = psutil.virtual_memory()
        load1, load5, load30 = os.getloadavg()
        load_1= round(load1, 2)
        load_5= round(load5, 2)
        load_30= round(load30, 2)

        disk_information = psutil.disk_usage('/')
        return {
            'technology': 'python2',
            'technology_version': platform.python_version(),
            'da_version': 0.1,
            'da_app_name': 'python_app',
            'os_name': platform.system(),
            'os_version': platform.version(),
            'os_arch': platform.architecture(),
            'avg_load_1_min': load_1, 
            'avg_load_5_min': load_5,
            'avg_load_30_min': load_30,
            'client_ip': socket.gethostbyname(socket.gethostname()),
            'total_memory_mb': self.convert.bytes_to_MB(physical_memory.total),
            'used_memory_mb': self.convert.bytes_to_MB(physical_memory.used),
            'user_name': (os.environ.get('USERNAME')), 
            'total_disk_mb': self.convert.bytes_to_MB(disk_information.total),
            'used_disk_mb': self.convert.bytes_to_MB(disk_information.used),
            'free_disk_mb': self.convert.bytes_to_MB(disk_information.used),
            'disk_usage_percent': disk_information.percent
        }
