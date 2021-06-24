import unittest
import sys
import requests
import json
import os
from src.main import Main
import mysql.connector as mysql


class TestStringMethods(unittest.TestCase):

    def test_simulator_up(self):
        r = requests.get(f"https://log680.vincentboivin.ca/api/health") 
        self.assertEqual("All system operational Commander !", r.text)
    
    def test_temperatureChaude_Invalide(self):
        with self.assertRaises(Exception):
            Main("f0c51c904ed6dd637b2f", 5, 33, 25)
    
    def test_nbtick_Invalide(self):
        with self.assertRaises(Exception):
            Main("f0c51c904ed6dd637b2f", -4, 22, 56)

    
if __name__ == '__main__':
    unittest.main()
