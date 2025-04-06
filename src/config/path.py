# -*- coding: utf-8 -*-
import os

config_path = os.path.dirname(os.path.abspath(__file__))
src_path = os.path.dirname(config_path)


if __name__ == "__main__":
    print(config_path)
    print(src_path)
