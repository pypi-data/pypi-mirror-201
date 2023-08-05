import argparse
import time
import os

from pyntcli.pynt_docker import pynt_container
from pyntcli.ui import ui_thread
from pyntcli.ui.progress import connect_progress_ws, wrap_ws_progress
from pyntcli.commands import sub_command, util

def har_usage():
    return ui_thread.PrinterText("Integration with static har file testing") \
            .with_line("") \
            .with_line("Usage:", style=ui_thread.PrinterText.HEADER) \
            .with_line("\tpynt har [OPTIONS]") \
            .with_line("") \
            .with_line("Options:", style=ui_thread.PrinterText.HEADER) \
            .with_line("\t--har - Path to har file") \
            .with_line("\t--reporters output results to json") 

class HarSubCommand(sub_command.PyntSubCommand):
    def __init__(self, name) -> None:
        super().__init__(name)

    def usage(self, *args):
        ui_thread.print(har_usage())

    def add_cmd(self, parent: argparse._SubParsersAction) -> argparse.ArgumentParser:
        har_cmd = parent.add_parser(self.name)
        har_cmd.add_argument("--har", type=str, required=True)
        har_cmd.add_argument("--reporters", action='store_true')
        har_cmd.print_usage = self.usage
        har_cmd.print_help = self.usage
        return har_cmd
    
    def run_cmd(self, args: argparse.Namespace):
        port = str(util.find_open_port())
        docker_type , docker_arguments = pynt_container.get_container_with_arguments(pynt_container.PyntDockerPort(src=port, dest=port, name="--port"))
        mounts = []

        if not os.path.isfile(args.har): 
            ui_thread.print(ui_thread.PrinterText("Could not find the provided har path, please provide with a valid har path", ui_thread.PrinterText.WARNING))
            return

        har_name = os.path.basename(args.har)
        docker_arguments += ["--har", har_name]
        mounts.append(pynt_container.create_mount(os.path.abspath(args.har), "/etc/pynt/{}".format(har_name)))

        with util.create_default_file_mounts(args) as m:

            mounts += m

            if "insecure" in args and args.insecure:
                docker_arguments.append("--insecure")
            
            if "dev_flags" in args: 
                docker_arguments += args.dev_flags.split(" ")
            
            har_docker = pynt_container.PyntContainer(image_name=pynt_container.PYNT_DOCKER_IMAGE,
                                                     tag="har-latest",
                                                     detach=True,
                                                     mounts=mounts,
                                                     args=docker_arguments)

            har_docker.run(docker_type)
        
            util.wait_for_healthcheck("http://localhost:{}".format(port))
            ui_thread.print_generator(ui_thread.AnsiText.wrap_gen(har_docker.stdout))
        
            with ui_thread.progress(wrap_ws_progress(connect_progress_ws("ws://localhost:{}/progress".format(port))), "scan in progress..."):
                while har_docker.is_alive():
                    time.sleep(1)


