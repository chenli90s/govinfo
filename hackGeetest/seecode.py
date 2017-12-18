import re
from .charlib import lib

class SeeCode:


    def __init__(self):
        self.r_file = open('geetest.js', 'r')
        self.w_file = open('res.js', 'r')

    def parse(self, str):
        res = re.findall(r'm3CC.W2v\(\d+\)', str)
        if res:
            pass


    def main(self):
        while True:
            str = self.r_file.readline()
            if not str:
                return
            res_str = self.parse(str)
            self.w_file.write(res_str)


    def __del__(self):
        self.r_file.close()
        self.w_file.close()






