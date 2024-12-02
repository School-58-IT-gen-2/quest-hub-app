import sys
sys.path.append("./")
import unittest
import os
from dotenv import load_dotenv
import time
from datetime import datetime, timezone
from adapters.db_source import DBSource
from net_config import envirements
load_dotenv()


class TestUserModel(unittest.TestCase):
    def test_smth(self):
        pass