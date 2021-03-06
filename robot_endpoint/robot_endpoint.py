from logger.logger_extension import LogRecordExtension, Extension
import argparse
import time
from fastapi import FastAPI
import os
import signal
import launch
from launch.frontend import Parser
from ament_index_python.packages import get_package_share_directory

from typing import List
from typing import Text
from typing import Tuple

import ansible_runner

class ProcessManager:
    def __init__(self):
        self.running = False
    def parse_launch_arguments(launch_arguments: List[Text]) -> List[Tuple[Text, Text]]:
        """Parse the given launch arguments from the command line, into list of tuples for launch."""
        parsed_launch_arguments = OrderedDict()  # type: ignore
        for argument in launch_arguments:
            count = argument.count(':=')
            if count == 0 or argument.startswith(':=') or (count == 1 and argument.endswith(':=')):
                raise RuntimeError(
                    "malformed launch argument '{}', expected format '<name>:=<value>'"
                    .format(argument))
            name, value = argument.split(':=', maxsplit=1)
            parsed_launch_arguments[name] = value  # last one wins is intentional
        return parsed_launch_arguments.items()
    async def call(self, package_name, launch_filename):
        if self.running:
            return
        self.launch_service = launch.LaunchService()
        launch_file_path = os.path.join(get_package_share_directory(package_name), 'launch', launch_filename)
            # argv=launch_file_arguments,
            # noninteractive=False,
            #debug=False)
        # parsed_launch_arguments = self.parse_launch_arguments(launch_file_arguments)
        launch_description = launch.LaunchDescription([
            launch.actions.IncludeLaunchDescription(
                launch.launch_description_sources.AnyLaunchDescriptionSource(
                    launch_file_path
                ),
                # launch_arguments=parsed_launch_arguments,
            ),
        ])
        self.launch_service.include_launch_description(launch_description)
        self.is_running = True
        ret = await self.launch_service.run_async()
    async def terminate(self):
        self.running = False
        await self.launch_service.shutdown()

proc_manager = ProcessManager()
app = FastAPI()

@app.get('/get/launch')
async def synchronize_packages(package_name: str, launch_filename: str):
    await proc_manager.call(package_name, launch_filename)
    return {}

@app.get('/get/terminate')
async def synchronize_packages():
    await proc_manager.terminate()
    return {}

@app.get('/get/run_playbook')
async def run_playbook(playbook_path: str):
    return {}