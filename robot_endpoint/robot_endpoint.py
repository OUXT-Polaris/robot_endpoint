from package_synchronizer.package_synchronizer import PackageSynchronizer
import argparse
import time
from fastapi import FastAPI

app = FastAPI()

@app.get('/')
async def synchronize_packages():
    sync = PackageSynchronizer("../example_config.yaml")
    sync.synchronize()
    return {"text": "hello world!"}