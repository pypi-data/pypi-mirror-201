import unittest
from test_utils import CliTest


class TestContext(CliTest):
    def test1_default_help(self):
        self.verify("hcs context", CliTest.NON_EMPTY_STRING)
        self.verify("hcs context --help", CliTest.NON_EMPTY_STRING)

    def test2_invalid_set(self):
        self.verify("hcs context set a b", "", 1, False)

    def test3_happy(self):
        self.verify("hcs context list", [])

        self.verify("hcs context set a k1=v1", "")
        self.verify("hcs context list", ["a"])

        self.verify("hcs context get a", {"k1": "v1"})
        self.verify("hcs context get a k1", "v1")
        self.verify("hcs context set a k1=v1", "")
        self.verify("hcs context set a k2=v2", "")
        self.verify("hcs context get a", {"k1": "v1", "k2": "v2"})
        self.verify("hcs context set a k1=33", "")
        self.verify("hcs context get a", {"k1": "33", "k2": "v2"})
        self.verify("hcs context get a k1", "33")
        self.verify("hcs context get a k2", "v2")
        self.verify("hcs context set a k1=", "")
        self.verify("hcs context get a", {"k1": "", "k2": "v2"})
        self.verify("hcs context delete a", "")
        self.verify("hcs context get a", "")
        self.verify("hcs context delete a", "")
        self.verify("hcs context list", [])


if __name__ == "__main__":
    unittest.main()
