import unittest
from unittest.mock import patch, MagicMock

from src.covmatic_robotstation.robot_api import RobotManagerHTTP, RobotManagerHTTPException

FAKE_ACTION_ID = "fakeactionid"
FAKE_HOST = "HOST"
FAKE_PORT = 1234

ACTION_PICK = {
            "action": "pick",
            "machine": "OT1",
            "position": "SLOT1",
            "plate_name": "REAGENT"
        }
ACTION_EXPECTED_URL = "http://{host}:{port}/action/pick/OT1/SLOT1/REAGENT".format(host=FAKE_HOST, port=FAKE_PORT)
ACTION_ANSWER = {
    "action_id": FAKE_ACTION_ID
}
MALFORMED_ACTION_ANSWER = {
    "wrong": "field"
}

CHECK_EXPECTED_URL = "http://{host}:{port}/action/check/{id}".format(host=FAKE_HOST, port=FAKE_PORT, id=FAKE_ACTION_ID)
CHECK_EXPECTED_ANSWER = {
    "state": "finished"
}
CHECK_MALFORMED_ANSWER = {
    "some": "thing"
}
CHECK_DATA_RETURNED = {
    "state": "finished"
}

DEFAULT_TIMEOUT = 5.0


class TestAPI(unittest.TestCase):
    def setUp(self) -> None:
        self._requests_patcher = patch('src.covmatic_robotstation.robot_api.requests')
        self._mock_requests = self._requests_patcher.start()
        self._mock_response = MagicMock()
        self._mock_requests.post.return_value = self._mock_response
        self._mock_requests.get.return_value = self._mock_response
        self._api = RobotManagerHTTP(FAKE_HOST, FAKE_PORT)

    def tearDown(self) -> None:
        self._requests_patcher.stop()


class TestActionRequest(TestAPI):
    def setUp(self) -> None:
        super().setUp()
        self._mock_response.json.return_value = ACTION_ANSWER
        self._mock_response.status_code = 200

    def test_request_calls_get(self):
        self._api.action_request(ACTION_PICK)
        self._mock_requests.post.assert_called_once()

    def test_request_return_value(self):
        self.assertEqual(FAKE_ACTION_ID, self._api.action_request(ACTION_PICK))

    def test_request_get_404(self):
        self._mock_response.json.side_effect = Exception("We shouldn't look for this json answer")
        self._mock_response.status_code = 404

        with self.assertRaises(RobotManagerHTTPException):
            self._api.action_request(ACTION_PICK)
        self._mock_requests.post.assert_called_once()

    def test_wrong_answer_raises(self):
        self._mock_response.json.return_value = MALFORMED_ACTION_ANSWER
        with self.assertRaises(RobotManagerHTTPException):
            self._api.action_request(ACTION_PICK)

    def test_request_url(self):
        self._api.action_request(ACTION_PICK)
        self._mock_requests.post.assert_called_once()
        args = self._mock_requests.post.call_args[0]
        self.assertEqual((ACTION_EXPECTED_URL, ), args)

    def test_request_json_data(self):
        self._api.action_request(ACTION_PICK)
        self._mock_requests.post.assert_called_once()
        kwargs = self._mock_requests.post.call_args[1]
        self.assertTrue('json' in kwargs)


class TestCheckOk(TestAPI):
    def setUp(self) -> None:
        super().setUp()
        self._mock_response.json.return_value = CHECK_EXPECTED_ANSWER
        self._mock_response.status_code = 200

    def test_calls_get(self):
        self._api.check_action(FAKE_ACTION_ID)
        self._mock_requests.get.assert_called_once()

    def test_called_url(self):
        self._api.check_action(FAKE_ACTION_ID)
        self._mock_requests.get.assert_called_once_with(CHECK_EXPECTED_URL, timeout=DEFAULT_TIMEOUT)

    def test_return_value(self):
        # self._mock_requests.get.side_effect = [CHECK_EXPECTED_ANSWER]
        self.assertEqual(CHECK_DATA_RETURNED, self._api.check_action(FAKE_ACTION_ID))

    def test_calls_get_404(self):
        self._mock_response.json.side_effect = Exception("We shouldn't look for this json answer")
        self._mock_response.status_code = 404

        with self.assertRaises(RobotManagerHTTPException):
            self._api.check_action(FAKE_ACTION_ID)
        self._mock_requests.get.assert_called_once()

    def test_calls_get_wrong_answer(self):
        self._mock_response.json.side_effect = [CHECK_MALFORMED_ANSWER]

        with self.assertRaises(RobotManagerHTTPException):
            self._api.check_action(FAKE_ACTION_ID)
        self._mock_requests.get.assert_called_once()
