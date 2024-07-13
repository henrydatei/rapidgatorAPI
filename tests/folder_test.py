import unittest
from rapidgatorAPI import RapidgatorAPI
import os
from dotenv import load_dotenv

load_dotenv()

class TestFolder(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rg = RapidgatorAPI(os.getenv("RAPIDGATOR_USERNAME"), os.getenv("RAPIDGATOR_PASSWORD"))
        cls.folder_ids = []
        
    def test_folder_create(self):
        folder = self.rg.folder_create("test")
        self.folder_ids.append(folder.folder_id)
        self.assertIsNotNone(folder)
        
    def test_folder_info(self):
        folder = self.rg.folder_create("test2")
        self.folder_ids.append(folder.folder_id)
        folder = self.rg.folder_info(folder.folder_id)
        self.assertIsNotNone(folder)
        
    def test_folder_content(self):
        folder = self.rg.folder_create("test3")
        self.folder_ids.append(folder.folder_id)
        folder, pager = self.rg.folder_content(folder.folder_id)
        self.assertIsNotNone(folder)
        
    def test_folder_rename(self):
        folder = self.rg.folder_create("test4")
        self.folder_ids.append(folder.folder_id)
        folder = self.rg.folder_rename(folder.folder_id, "test5")
        self.assertIsNotNone(folder)
        
    def test_folder_copy(self):
        folder = self.rg.folder_create("test6")
        folder2 = self.rg.folder_create("test7")
        self.folder_ids.append(folder.folder_id)
        self.folder_ids.append(folder2.folder_id)
        result = self.rg.folder_copy(folder.folder_id, folder2.folder_id)
        self.assertEqual(result["result"]["success"], 1)
        
    def test_folder_move(self):
        folder = self.rg.folder_create("test8")
        folder2 = self.rg.folder_create("test9")
        self.folder_ids.append(folder.folder_id)
        self.folder_ids.append(folder2.folder_id)
        result = self.rg.folder_move(folder.folder_id, folder2.folder_id)
        self.assertEqual(result["result"]["success"], 1)
        
    def test_folder_delete(self):
        folder = self.rg.folder_create("test10")
        result = self.rg.folder_delete(folder.folder_id)
        self.assertEqual(result["result"]["success"], 1)
        
    # def test_folder_change_mode(self):
    #     folder = self.rg.folder_create("test11")
    #     self.folder_ids.append(folder.folder_id)
    #     folder = self.rg.folder_change_mode(folder.folder_id, 1)
    #     self.assertIsNotNone(folder)
        
    def tearDown(self) -> None:
        for folder_id in self.folder_ids:
            self.rg.folder_delete(folder_id)