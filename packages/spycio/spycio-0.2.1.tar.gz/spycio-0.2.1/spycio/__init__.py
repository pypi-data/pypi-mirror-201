""" Package Eule  """

# -*- coding: utf-8 -*-

from __future__ import annotations

from .spycio import distance, pNorm, \
    pNormDistance, sphereCentralAngle, centralAngle, \
    greatCircleDistance, nSphereDistance, travelTime

from .utils import hav, spherToCart, \
    isSpherical, throw, hasKey
    

__author__ = """Bruno Peixoto"""
__email__ = 'brunolnetto@gmail.com'
