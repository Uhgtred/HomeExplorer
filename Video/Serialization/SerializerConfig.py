#!/usr/bin/env python3
# @author: Markus Kösters

import os
from dataclasses import dataclass


@dataclass
class SerializerConfig:
    storageFile: os.PathLike