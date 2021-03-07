from package_synchronizer.package_synchronizer import PackageSynchronizer
from logger.logger_extension import LogRecordExtension, Extension
import argparse
import time
from fastapi import FastAPI
import os
import signal
from subprocess import Popen, PIPE

class ProcessManager:
    def call(self, package_name, launch_filename):
        self.p = Popen(['ros2', 'launch', package_name, launch_filename], shell=False)
    def terminate(self):
        os.kill(self.p.pid, signal.SIGINT)
        # self.p.kill()

proc_manager = ProcessManager()
app = FastAPI()

@app.get('/get/synchronize_packages')
async def synchronize_packages(force_update: bool):
    sync = PackageSynchronizer("../example_config.yaml")
    return {"result" : sync.synchronize(force_update)}

@app.get('/get/launch')
async def synchronize_packages(package_name: str, launch_filename: str):
    proc_manager.call(package_name, launch_filename)
    return {}
    # sync = PackageSynchronizer("../example_config.yaml")
    # return {"result" : sync.synchronize(force_update)}

@app.get('/get/terminate')
async def synchronize_packages():
    proc_manager.terminate()
    return {}