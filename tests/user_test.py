import unittest
from rapidgatorAPI import RapidgatorAPI
import os
from dotenv import load_dotenv

load_dotenv()

class TestUser(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rg = RapidgatorAPI(os.getenv("RAPIDGATOR_USERNAME"), os.getenv("RAPIDGATOR_PASSWORD"))
        
    def test_info(self):
        user = self.rg.info()
        self.assertIsNotNone(user)