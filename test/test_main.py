import unittest
import requests
from src.main import Main


class TestStringMethods(unittest.TestCase):


    
    def test_forcing_failure(self):
        self.assertTrue(1 == 2)
    


if __name__ == '__main__':
    unittest.main()
