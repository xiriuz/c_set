# import hexatool
# from hexatool import IntelHex
import unittest
from io import StringIO

hex_32="""\
:02000004800179
:20C00000000000000000000012345678AAAAAAAABBBBBBBBCCCCCCCCDDDDDDDDEEEEEEEE1C
"""

class SimpleTestCase(unittest.TestCase):
    """! Template for all tests.
    """
    

# class TestIntelHex(SimpleTestCase):
#         ih = IntelHex()

f = StringIO(hex_32)

if __name__=="__main__":
    unittest.main()