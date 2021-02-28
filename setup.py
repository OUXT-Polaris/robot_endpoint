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
        "transitions",
        "transitions-gui",
        "argparse",
        "yaml",
        "os",
        "hashlib"
    ],
    packages=[
        'package_synchronizer',
        'iot_events',
        'state_machine'
    ]
)