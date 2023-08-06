""" Base class that instantiate robot control """
from abc import ABC
from covmatic_stations.station import Station, instrument_loader, labware_loader
from .robot import Robot


class RobotStationABC(Station, ABC):
    def __init__(self,
                 ot_name: str,
                 robot_manager_host: str = None,
                 robot_manager_port: int = None,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._ot_name = ot_name
        self._robot_manager_host = robot_manager_host
        self._robot_manager_port = robot_manager_port

    @instrument_loader(0, "_robot")
    def load_robot(self):
        self._robot = Robot(robot_name=self._ot_name,
                            robot_manager_host=self._robot_manager_host,
                            robot_manager_port=self._robot_manager_port,
                            simulate=self._ctx.is_simulating())

    @instrument_loader(0, "_robot_trash")
    def load_robot_trash(self):
        self._robot_trash = Robot(robot_name="TRASH",
                            robot_manager_host=self._robot_manager_host,
                            robot_manager_port=self._robot_manager_port,
                            simulate=self._ctx.is_simulating())

    def robot_pick_plate(self, slot, plate_name):
        if self._run_stage:
            self.home()
            self.watchdog_stop()
            try:
                self._robot.pick_plate(slot, plate_name)
            except Exception as e:
                self.logger.error("Error requesting pick plate {} from slot {}: {}".format(plate_name, slot, e))
                self.pause("Error in plate transfer. Please transfer manually plate {} from slot {}".format(plate_name, slot),
                           home=False)
            self.watchdog_start()
        else:
            self.logger.info("Skipping pick plate {} from slot {} because previous stage not run.".format(plate_name, slot))

    def robot_drop_plate(self, slot, plate_name):
        if self._run_stage:
            self.home()
            self.watchdog_stop()
            try:
                self._robot.drop_plate(slot, plate_name)
            except Exception as e:
                self.logger.error("Error requesting drop plate {} to slot {}: {}".format(plate_name, slot, e))
                self.pause("Error in plate transfer. Please transfer manually plate {} to slot {}".format(plate_name, slot),
                           home=False)
            self.watchdog_start()
        else:
            self.logger.info("Skipping drop plate {} from slot {} because previous stage not run.".format(plate_name, slot))

    def robot_trash_plate(self, pick_slot, trash_slot, plate_name="TRASH"):
        if self._run_stage:
            self.logger.info("Trashing requested from slot {} to trash slot {} for plate {}".format(pick_slot, trash_slot, plate_name))

            self.home()
            self.watchdog_stop()
            try:
                self._robot_trash.drop_plate(trash_slot, plate_name, wait=False)
                self._robot.pick_plate(pick_slot, plate_name)

            except Exception as e:
                self.logger.error("Error requesting trash plate {} from slot {} to slot {}: {}".format(plate_name, pick_slot, trash_slot, e))
                self.pause("Error in plate transfer. Please move manually plate {} on slot {} to trash".format(plate_name, pick_slot),
                           home=False)
            self.watchdog_start()
        else:
            self.logger.info("Skipping trash plate {} from slot {} to slot {} because previous stage not run.".format(
                plate_name, pick_slot, trash_slot))

    def robot_transfer_plate_internal(self, pick_slot, drop_slot, plate_name="INTERNAL"):
        if self._run_stage:
            self.logger.info("Transferring plate {} from internal slot {} to slot {}".format(plate_name, pick_slot, drop_slot))

            self.home()
            self.watchdog_stop()
            try:
                self._robot.transfer_plate_internal(pick_slot, drop_slot, plate_name)
            except Exception as e:
                self.logger.error("Error in plate transfer for plate {} from slot {} to slot {}. Error: {}".format(
                    plate_name, pick_slot, drop_slot, e))
                self.pause("Error in plate transfer. Please transfer manually plate {} from slot {} to slot {}".format(
                    plate_name, pick_slot, drop_slot), home=False)
            self.watchdog_start()
        else:
            self.logger.info("Skipping transfer plate {} from slot {} to slot {} because previous stage not run.".format(
                plate_name, pick_slot, drop_slot))
