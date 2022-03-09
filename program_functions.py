import logging
import time

from runtime_helpers.user_messenger_logging import UserMessengerHandler


def get_callback(user_messenger):
    callback_counter = 0
    callback_time = time.time()

    def _callback(x):
        nonlocal callback_counter
        nonlocal callback_time
        user_messenger.publish({'iteration': callback_counter, 'duration': time.time() - callback_time, 'params': x})
        callback_time = time.time()
        callback_counter += 1

    return _callback


def activate_logging(user_messenger, log_level, log_modules):
    if len(log_modules) == 0:
        return
    handler = UserMessengerHandler(user_messenger)
    handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
    for module in log_modules:
        logging.getLogger(module).setLevel(log_level)
        logging.getLogger(module).addHandler(handler)
