import unittest
from test_utils import CliTest


class TestProfile(CliTest):
    def test1(self):
        self.verify("hcs profile", CliTest.NON_EMPTY_STRING)

    def test2_happy(self):
        self.verify("hcs profile list", CliTest.NON_EMPTY_JSON)
        self.verify("hcs profile file", CliTest.NON_EMPTY_STRING)
        self.verify("hcs profile get", CliTest.NON_EMPTY_JSON)
        self.verify("hcs profile create", "", 2, False)
        self.verify("hcs profile delete _inexist_profile_ut", "")


if __name__ == "__main__":
    unittest.main()
