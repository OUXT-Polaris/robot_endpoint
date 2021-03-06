from setuptools import setup, find_packages
 
setup(
    name='robot_endpoint',
    version="0.0.1",
    description="FOTA tools for ROS/ROS2 packages",
    long_description="",
    author='masaya kataoka',
    license='MIT',
    classifiers=[
        "Development Status :: 1 - Planning"
    ],
    install_requires=[
        "boto3",
        "awsiotsdk",
        "argparse",
        "yaml",
        "os",
        "hashlib",
        "fastapi",
        "uvicorn"
    ],
    packages=[
        'package_synchronizer',
        'iot_events',
        'robot_endpoint'
    ]
)