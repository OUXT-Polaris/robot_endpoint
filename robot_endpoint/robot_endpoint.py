from package_synchronizer.package_synchronizer import PackageSynchronizer
from logger.logger_extension import LogRecordExtension, Extension
import argparse
import time
from fastapi import FastAPI

app = FastAPI()

@app.get('/get/{synchronize_packages}')
async def synchronize_packages(force_update: bool):
    sync = PackageSynchronizer("../example_config.yaml")
    return {"result" : sync.synchronize(force_update)}