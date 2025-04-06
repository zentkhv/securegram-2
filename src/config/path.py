# -*- coding: utf-8 -*-
import os

config_path = os.path.dirname(os.path.abspath(__file__))
src_path = os.path.dirname(config_path)

data_path = os.path.join(src_path, "data")
sessions_path = os.path.join(data_path, "sessions")

static_path = os.path.join(src_path, "data", "static")
templates_path = os.path.join(src_path, "data", "templates")


if __name__ == "__main__":
    print(config_path)
    print(src_path)
    print(data_path)
