import unittest
from unittest.mock import patch, MagicMock, call
from src.covmatic_robotstation.robot_station import RobotStationABC, Station
from .common import logger

TEST_SLOT = "SLOT1"
TEST_SLOT2 = "SLOT2"
TEST_PLATE = "PLATE"


class FakeStation(RobotStationABC):
    def _tipracks(self) -> dict:
        return {}


class TestBaseClass(unittest.TestCase):
    def setUp(self) -> None:
        self._robot_patcher = patch('src.covmatic_robotstation.robot_station.Robot')
        self._mock_robot = self._robot_patcher.start()
        self._s = FakeStation(ot_name="OTTEST", logger=logger)
        self._s._ctx = MagicMock()                  # Mocking OT context calls
    def tearDown(self) -> None:
        self._robot_patcher.stop()


class TestRobotStation(TestBaseClass):
    def test_creation(self):
        self.assertTrue(self._s)

    def test_robot_is_loaded(self):
        self._s.load_robot()
        self.assertEqual(1, self._mock_robot.call_count)


class TestFunctions(TestBaseClass):
    def setUp(self) -> None:
        super().setUp()
        self._s.load_robot()

    @patch.object(Station, "home")
    def test_robot_pick_called(self, mock_home):
        self._s.robot_pick_plate(TEST_SLOT, TEST_PLATE)
        self._mock_robot().pick_plate.assert_called_once()

    @patch.object(Station, "home")
    def test_robot_pick_called_after_home(self, mock_home):
        mock_manager = MagicMock()
        mock_manager.attach_mock(mock_home, "home")
        mock_manager.attach_mock(self._mock_robot(), "robot")

        self._s.robot_pick_plate(TEST_SLOT, TEST_PLATE)

        expected_calls = [call.home(), call.robot.pick_plate(TEST_SLOT, TEST_PLATE)]

        self.assertEqual(expected_calls, mock_manager.mock_calls)

    @patch.object(Station, "home")
    def test_robot_drop_called_after_home(self, mock_home):
            mock_manager = MagicMock()
            mock_manager.attach_mock(mock_home, "home")
            mock_manager.attach_mock(self._mock_robot(), "robot")

            self._s.robot_drop_plate(TEST_SLOT, TEST_PLATE)

            expected_calls = [call.home(), call.robot.drop_plate(TEST_SLOT, TEST_PLATE)]

            self.assertEqual(expected_calls, mock_manager.mock_calls)

    @patch.object(Station, "home")
    def test_transfer_internal_plate(self, mock_home):
        mock_manager = MagicMock()
        mock_manager.attach_mock(mock_home, "home")
        mock_manager.attach_mock(self._mock_robot(), "robot")

        self._s.robot_transfer_plate_internal(TEST_SLOT, TEST_SLOT2, TEST_PLATE)

        expected_calls = [call.home(), call.robot.transfer_plate_internal(TEST_SLOT, TEST_SLOT2, TEST_PLATE)]
        self.assertEqual(expected_calls, mock_manager.mock_calls)

    @patch.object(Station, "home")
    @patch.object(Station, "pause")
    def test_if_error_ask_to_move_manually_pick(self, mock_pause, mock_home):
        self._mock_robot().pick_plate.side_effect = Exception("Unwanted exception")
        self._s.robot_pick_plate(TEST_SLOT, TEST_PLATE)
        mock_pause.assert_called()

    @patch.object(Station, "home")
    @patch.object(Station, "pause")
    def test_if_error_ask_to_move_manually_drop(self, mock_pause, mock_home):
        self._mock_robot().drop_plate.side_effect = Exception("Unwanted exception")
        self._s.robot_drop_plate(TEST_SLOT, TEST_PLATE)
        mock_pause.assert_called()

    @patch.object(Station, "watchdog_stop")
    @patch.object(Station, "watchdog_start")
    @patch.object(Station, "home")
    def test_pick_stop_watchdog(self, mock_home, mock_wd_start, mock_wd_stop):
        self._s.robot_pick_plate(TEST_SLOT, TEST_PLATE)
        mock_wd_start.assert_called()
        mock_wd_stop.assert_called()

    @patch.object(Station, "watchdog_stop")
    @patch.object(Station, "watchdog_start")
    @patch.object(Station, "home")
    @patch.object(Station, "pause")
    def test_pick_exception_watchdog_started(self, mock_pause, mock_home, mock_wd_start, mock_wd_stop):
        self._mock_robot().pick_plate.side_effect = Exception("Unwanted exception")
        self._s.robot_pick_plate(TEST_SLOT, TEST_PLATE)
        mock_wd_start.assert_called()
        mock_wd_stop.assert_called()

    @patch.object(Station, "watchdog_stop")
    @patch.object(Station, "watchdog_start")
    @patch.object(Station, "home")
    def test_drop_stop_watchdog(self, mock_home, mock_wd_start, mock_wd_stop):
        self._s.robot_drop_plate(TEST_SLOT, TEST_PLATE)
        mock_wd_start.assert_called()
        mock_wd_stop.assert_called()

    @patch.object(Station, "watchdog_stop")
    @patch.object(Station, "watchdog_start")
    @patch.object(Station, "home")
    @patch.object(Station, "pause")
    def test_drop_exception_watchdog_started(self, mock_pause, mock_home, mock_wd_start, mock_wd_stop):
        self._mock_robot().drop_plate.side_effect = Exception("Unwanted exception")
        self._s.robot_drop_plate(TEST_SLOT, TEST_PLATE)
        mock_wd_start.assert_called()
        mock_wd_stop.assert_called()

    @patch.object(Station, "watchdog_stop")
    @patch.object(Station, "watchdog_start")
    @patch.object(Station, "home")
    def test_transfer_internal_stop_watchdog(self, mock_home, mock_wd_start, mock_wd_stop):
        self._s.robot_transfer_plate_internal(TEST_SLOT, TEST_SLOT)
        mock_wd_start.assert_called()
        mock_wd_stop.assert_called()

    @patch.object(Station, "watchdog_stop")
    @patch.object(Station, "watchdog_start")
    @patch.object(Station, "home")
    @patch.object(Station, "pause")
    def test_transfer_internal_exception_watchdog_started(self, mock_pause, mock_home, mock_wd_start, mock_wd_stop):
        self._mock_robot().transfer_plate_internal.side_effect = Exception("Unwanted exception")
        self._s.robot_transfer_plate_internal(TEST_SLOT, TEST_SLOT, TEST_PLATE)
        mock_wd_start.assert_called()
        mock_wd_stop.assert_called()

class TestTrashRobot(TestBaseClass):
    def setUp(self) -> None:
        super().setUp()
        self._s.load_robot()
        self._s.load_robot_trash()

    @patch.object(Station, "watchdog_stop")
    @patch.object(Station, "watchdog_start")
    @patch.object(Station, "home")
    def test_trash_stop_watchdog(self, mock_home, mock_wd_start, mock_wd_stop):
        self._s.robot_trash_plate(TEST_SLOT, TEST_SLOT, TEST_PLATE)
        mock_wd_start.assert_called()
        mock_wd_stop.assert_called()

    @patch.object(Station, "watchdog_stop")
    @patch.object(Station, "watchdog_start")
    @patch.object(Station, "home")
    @patch.object(Station, "pause")
    def test_trash_exception_watchdog_started(self, mock_pause, mock_home, mock_wd_start, mock_wd_stop):
        self._mock_robot().drop_plate.side_effect = Exception("Unwanted exception")
        self._s.robot_trash_plate(TEST_SLOT, TEST_SLOT, TEST_PLATE)
        mock_wd_start.assert_called()
        mock_wd_stop.assert_called()

