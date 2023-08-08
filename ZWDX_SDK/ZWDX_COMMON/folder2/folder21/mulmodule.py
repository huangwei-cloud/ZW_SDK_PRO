import os
import sys

sys.path.append(r'E:\Hw_work\Python\ZW_SDK_PRO\ZWDX_SDK\ZWDX_COMMON')
print(sys.path)

from folder2 import submodule


def mul(a, b):
    return a * b


if __name__ == '__main__':
    print(submodule.sub(8, 7))
