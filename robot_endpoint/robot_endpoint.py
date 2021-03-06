from package_synchronizer.package_synchronizer import PackageSynchronizer
import argparse
import time

class RobotEndppoint:
    def __init__(self, config_path):
        self.config_path = config_path
    def run(self):
        while True:
            try:
                time.sleep(1)
            except KeyboardInterrupt:
                break


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Endpoint for ROS2 robot')
    parser.add_argument('config_path', help='path to the config yaml path')
    args = parser.parse_args()
    endpoint = RobotEndppoint(args.config_path)
    endpoint.run()