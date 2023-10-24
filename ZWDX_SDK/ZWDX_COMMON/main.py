from folder1 import addmodule
from folder2 import submodule
from folder2.folder21 import mulmodule  # 作为运行文件的时候不能这么写“from .folder2.folder21 import mulmodule”
import numpy as np
import matplotlib.pyplot as plt
from wave import wavemodule


if __name__ == '__main__':
    print(addmodule.add(1, 2))
    print(submodule.sub(5, 3))
    print(mulmodule.mul(5, 3))

    x, y = wavemodule.sin(1, 500, 50000, 0, 5/500)
    plt.plot(x, y)
    plt.show()
