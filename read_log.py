# -*- coding: utf-8 -*-
"""
Created on Thu Aug  4 20:17:23 2022

@author: atgol
"""

import numpy as np
import pandas as pd

deal_log = pd.read_csv("D:/game_plan/FFXIV/Jomusse_first.csv")
deal_log = deal_log.fillna(0)