""" Module to manage EVA robot operations with RobotManager """
import logging
import time

from .robot_api import RobotManagerHTTP, RobotManagerSimulator


class RobotException(Exception):
    pass


class Robot:
    """ Main Robot class to interface with a RobotManager instance
        :param robot_name: name of the current pipetting robot;
        :param robot_manager_host: hostname or ip address of the RobotManager instance;
        :param simulate: whether to simulate action requests and check results;
        :param check_wait_time: delay between *check_action* calls waiting for the action to be completed;
    """
    def __init__(self,
                 robot_name: str,
                 robot_manager_host: str,
                 robot_manager_port: int,
                 simulate: bool = False,
                 check_wait_time: float = 0.5):
        if not robot_name.isalnum():
            raise RobotException("Robot name not aphanumeric: {}".format(robot_name))
        self._robot_name = robot_name
        self._logger = logging.getLogger(__name__)
        self._logger.info("Simulate is {}".format(simulate))
        self._check_wait_time = 0 if simulate else check_wait_time
        self._api = RobotManagerSimulator() if simulate else RobotManagerHTTP(robot_manager_host, robot_manager_port)

    def build_request(self, action: str, slot: str, plate_name: str, ):
        return {
            "action": action,
            "machine": self._robot_name,
            "position": slot,
            "plate_name": plate_name
        }

    def pick_plate(self, slot: str, plate_name: str, wait: bool = True):
        return self.execute_action("pick", slot, plate_name, wait=wait)

    def drop_plate(self, slot: str, plate_name: str, wait: bool = True):
        return self.execute_action("drop", slot, plate_name, wait=wait)

    def transfer_plate_internal(self, from_slot, to_slot, plate_name: "INTERNAL_PLATE"):
        """ Function to transfer a plate internally to an OT.
            Since v0.0.4 robotmanager needs both pick and drop place before doing a transfer, so here we will wait
            for completion only after have launched both actions
        """
        id1 = self.execute_action("pick", from_slot, plate_name, wait=False)
        id2 = self.execute_action("drop", to_slot, plate_name, wait=False)
        self.wait_for_action_to_finish(id1)
        self.wait_for_action_to_finish(id2)

    def execute_action(self, action, slot, plate_name, wait: bool = True):
        action_id = self._api.action_request(self.build_request(action, slot, plate_name))
        if wait:
            self.wait_for_action_to_finish(action_id)
        return action_id

    def wait_for_action_to_finish(self, action_id):
        self._logger.info("Waiting for action to finish with id: {}".format(action_id))
        while True:
            res = self._api.check_action(action_id)
            self._logger.info("Received {}".format(res))
            if res["state"] != "pending":
                break
            else:
                if self._check_wait_time:
                    time.sleep(self._check_wait_time)
