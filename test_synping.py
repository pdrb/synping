#!/usr/bin/env python3

import unittest
from unittest.mock import patch

from synping import synping


@patch("sys.argv", ["synping.py", "localhost", "-n", "1"])
class TestSynping(unittest.TestCase):
    def test_cli(self):
        synping.cli()


if __name__ == "__main__":
    unittest.main()
