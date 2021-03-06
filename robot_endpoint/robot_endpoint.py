from package_synchronizer.package_synchronizer import PackageSynchronizer
from logger.logger_extension import LogRecordExtension, Extension
import argparse
import time
from fastapi import FastAPI

from pydantic import BaseModel
from typing import Optional, List

class SynchronizePackagesParameters(BaseModel):
    force_update: False

app = FastAPI()

@app.post('/')
async def synchronize_packages(params: SynchronizePackagesParameters):
    sync = PackageSynchronizer("../example_config.yaml")
    return sync.synchronize()