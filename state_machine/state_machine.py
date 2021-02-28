from transitions_gui import WebMachine
import time
from transitions.extensions.states import Timeout, Tags, add_state_features

from package_synchronizer.package_synchronizer import PackageSynchronizer

@add_state_features(Timeout, Tags)
class CustomMachine(WebMachine):
    pass

class Model:

    def shutdown(self):
        pass

    def create_report(self):
        pass

    def notify(self):
        pass

    def reset(self):
        pass

    def is_valid(self):
        return True

    def abort_triggered(self):
        return False

class StateMachine(object):
    states = [
        'wakeup',
        'ready',
        'running',
        'error'
    ]

    transitions = [
        {
            'trigger': 'synchronize',
            'source': 'wakeup',
            'dest':'ready',
            'conditions': 'is_valid',
            'unless': 'abort_triggered'
        },
        {
            'trigger': 'launch',
            'source': 'ready',
            'dest':'running'
        },
        {
            'trigger': 'terminate',
            'source': 'running',
            'dest':'wakeup'
        },
        {
            'trigger': 'clash',
            'source': 'running',
            'dest': 'error'
        },
        {
            'trigger': 'retry',
            'source': 'error',
            'dest': 'running'
        },
        {
            'trigger': 'shutdown',
            'source': 'error',
            'dest': 'wakeup'
        }
    ]
    def __init__(self, name):
        self.name = name
        self.machine = CustomMachine(
            Model(),
            states=self.states,
            transitions=self.transitions,
            initial='wakeup',
            name=self.name,
            ignore_invalid_triggers=True,
            auto_transitions=False)

if __name__ == '__main__':
    state_machine = StateMachine("robot_endpoint")