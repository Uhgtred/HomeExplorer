#!/usr/bin/env python3
# @author: Markus Kösters

import os
from dataclasses import dataclass
from typing import Optional


@dataclass
class SerializerConfig:
    """
    Todo: This makes no sense. Delete it, it overcomplicates things.
    """
    storageFile: Optional[os.PathLike | str] = ''
