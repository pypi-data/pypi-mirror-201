import pandas as pd
from . import module1

def test_package():
    print("This is module2's package test")

def test_module1_package():
    module1.test_package()