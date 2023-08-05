import requests
import time
import socket
import os
import tempfile
from contextlib import contextmanager
import webbrowser

from pyntcli.pynt_docker import pynt_container
from pyntcli.store import CredStore
from pyntcli.ui import report

def is_port_in_use(port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) == 0

def find_open_port() -> int:
    with socket.socket() as s:
        s.bind(('', 0))            
        return s.getsockname()[1] 

HEALTHCHECK_TIMEOUT = 10
HEALTHCHECK_INTERVAL = 0.1

def wait_for_healthcheck(address): 
    start = time.time()
    while start + HEALTHCHECK_TIMEOUT > time.time(): 
        try:
            res = requests.get(address + "/healthcheck")
            if res.status_code == 418:
                return 
        except: 
            time.sleep(HEALTHCHECK_INTERVAL)
    raise TimeoutError()


@contextmanager
def create_default_file_mounts(args):
    html_report_path = os.path.join(tempfile.gettempdir(), "results.html")
    json_report_path = os.path.join(tempfile.gettempdir(), "results.json")

    if "reporters" in args and args.reporters: 
        html_report_path = os.path.join(os.getcwd(), "pynt_results.html")
        json_report_path = os.path.join(os.getcwd(), "pynt_results.json")

    mounts = []
    with open(html_report_path, "w"), open(json_report_path, "w"):    
        mounts.append(pynt_container.create_mount(json_report_path, "/etc/pynt/results/results.json"))
        mounts.append(pynt_container.create_mount(html_report_path, "/etc/pynt/results/results.html"))
    
    mounts.append(pynt_container.create_mount(CredStore().get_path(), "/app/creds.json"))

    yield mounts
    
    webbrowser.open("file://{}".format(html_report_path))
    report.PyntReporter(json_report_path).print_summary() 