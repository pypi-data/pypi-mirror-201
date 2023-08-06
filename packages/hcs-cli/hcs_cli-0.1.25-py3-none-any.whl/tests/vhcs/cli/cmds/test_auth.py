import unittest
from test_utils import CliTest


class TestAuth(CliTest):
    def test_not_initialized(self):
        self.verify("hcs auth", "", 1, False)

    def test_details(self):
        self.verify("hcs auth --details", "", 1, False)


if __name__ == "__main__":
    unittest.main()
