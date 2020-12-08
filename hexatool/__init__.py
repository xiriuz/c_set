import re
import sys


class HexIntel():
    def __init__(self, fname):
        self.fname = fname
        self.str_con = rfile(self.fname)

    def editHexStr_intelHex(self, strStartAddr, strSetValue, matchExactAddr=False):
        """! Edit Hex String with Intel Hex format
        @param strStartAddr     start Address of the value
        @param strSetValue      value to set
        @param matchExactAddr   [False] (default) get value from 
                                address-search with offset-calculation
                                [True]  exact searchAddr_low 
        @return                 None
        @TODO                   edit multi line (only can edit single line now)
        """
        assert len(strStartAddr) == 8, "strStartAddr Length should be 8"

        searchAddr_high, strAddr_low = strStartAddr[:4], strStartAddr[4:]

        if matchExactAddr:
            searchAddr_low = strAddr_low
        else:
            searchAddr_low = strHexToRoundDown(strAddr_low)[:3] + r"[A-F0-9]"

        def editValue_matchGroup(m):
            """! Return Edited value from matched group
            @param m
                group(2) : len
                group(3) : addr
                group(4) : type
                group(5) : data
                group(6) : chksum
                group(7) : whitespace
            """
            startOffst = (int(strAddr_low, 16) - int(m.group(3), 16)) * 2
            edited_data = m.group(5)[:startOffst] + strSetValue \
                + m.group(5)[startOffst+len(strSetValue):]
            edited_line = m.group(2) + m.group(3) + m.group(4) + edited_data
            return m.group(1) + edited_line + getChecksum_intelHex(edited_line) + m.group(7)

        self.str_con = re.sub(r"(:02000004{0}[A-F0-9]{{2}}\s[:A-F0-9\s]*?:)([A-F0-9]{{2}})({1})(00)([A-F0-9]*)([A-F0-9]{{2}})(\s*)"
                              .format(searchAddr_high, searchAddr_low),
                              editValue_matchGroup,
                              self.str_con,
                              re.DOTALL | re.VERBOSE)

    def getHexStr_intelHex(self, strStartAddr, intByteSize, matchExactAddr=False):
        """! Get dictionary of Hex String info data with Intel Hex format
        @param strStartAddr     start Address of the value
        @param intByteSize      Byte Size of the value
        @param matchExactAddr   [False] (default) get value from 
                                address-search with offset-calculation
                                [True]  exact searchAddr_low 
        @return                 dict of hex info
        @retval["hexstr"]       value of hex str
        @retval["pos_data"]     start position of data in self.str_con
        @retval["pos_chks"]     start position of chksum in self.str_con
        """
        assert len(strStartAddr) == 8, "strStartAddr Length should be 8"

        intFullSize = intByteSize * 2
        searchAddr_high, strAddr_low = strStartAddr[:4], strStartAddr[4:]

        if matchExactAddr:
            searchAddr_low = strAddr_low
        else:
            searchAddr_low = strHexToRoundDown(strAddr_low)[:3] + r"[A-F0-9]"

        m = re.search(rf"""
                        :02000004{searchAddr_high}[A-F0-9]{{2}}\s
                        [:A-F0-9\s]*?
                        :[A-F0-9]{{2}}(?P<foundAddr>{searchAddr_low})00
                        (?P<foundData>[A-F0-9]*)
                        (?P<foundChks>[A-F0-9]{{2}})
                        \s*
                        """,
                      self.str_con, re.DOTALL | re.VERBOSE)

        if m:
            found_addr = m.group("foundAddr")
            addressOffset = (int(strAddr_low, 16) - int(found_addr, 16)) * 2
            found_data = m.group("foundData")
            rest_size = int((intFullSize - len(found_data) + addressOffset)//2)

            chks_addr = m.start("foundChks")
            data_addr = m.start("foundData") + addressOffset
            
            dictReturn = {"hexstr"  :found_data[addressOffset:addressOffset+intFullSize],
                          "pos_data":data_addr,
                          "pos_chks":chks_addr
                          }

            if rest_size > 0:
                # return position info only if data is in a single line
                next_start_addr = searchAddr_high + intToHex(int(found_addr, 16) + len(found_data)//2)
                dictReturn["hexstr"] += self.getHexStr_intelHex(next_start_addr, rest_size, matchExactAddr=True)["hexstr"]            
            return dictReturn
        sys.exit("[Error] Not found {0} address in {1}".format(strStartAddr, self.fname))

    def saveHexStr(self, strCon=None, fname=None):
        if not strCon:
            strCon = self.str_con
        if not fname:
            fname = self.fname
        wfile(fname, strCon)

def intToHex(intVal, n=2):
    """! return hex string converted from int 
    @param intVal   int value 
    @param n        define len of return value
    @return         hex string 
    """
    assert type(intVal) == int, "argument should be int."
    return "{0:0{i}X}".format(intVal & 0xFF, i=n)


def strHexToRoundDown(strHex, base=32):
    """! return hex string with round down by base from hex string (ex) 0065 -> 0060, 0090 -> 0080
    @param strHex   hex string
    @param base     define base num
    @return         hex string 
    """
    assert type(strHex) == str, "argument should be string."
    return hex(int(int(strHex, 16)/base) * base)[2:].upper()


def getTwosComplement_hexStr(strHex):
    import binascii
    intList_data = list(binascii.unhexlify(strHex))
    return "%02X" % (((~sum(intList_data) & 0xFF) + 1) & 0xFF)


def getChecksum_intelHex(data):
    assert len(data) % 2 == 0, "data should be muptiples of 2"
    return getTwosComplement_hexStr(data)


def rfile(fname):
    with open(fname, "r") as f:
        return f.read()


def wfile(fname, strCon):
    with open(fname, "w") as f:
        f.write(strCon)


