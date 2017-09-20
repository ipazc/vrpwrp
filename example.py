#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from vrpwrp.helpers import image_helper

__author__ = 'Iván de Paz Centeno'


with open("vrpwrp/samples/subject2_2.jpg", "rb") as f:
    bytes = f.read()

image = image_helper.get_image(bytes)

for x in image_helper.segment_image(image, 200, 200):
    x.show()
    print(x.size)

