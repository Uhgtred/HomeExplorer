#!/usr/bin/env python3
# @author: Markus Kösters

from Video.Compressor.CompressorZlib import CompressorZlib


class CompressorFactory:

    @staticmethod
    def produceCompressorZlib():
        return CompressorZlib()