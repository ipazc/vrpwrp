#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from vrpwrp.config import config
from vrpwrp.tools.boundingbox import BoundingBox
from vrpwrp.wrappers.APIWrapper import APIWrapper

__author__ = 'Iván de Paz Centeno'



class FaceDetection(APIWrapper):
    def __init__(self, API_URL=None):
        if API_URL is None:
            API_URL = config.FACE_DETECTION_API

        super().__init__(API_URL)

    def analyze(self, image_bytes):
        response = self._request("PUT", data=image_bytes, is_binary=True)['bounding_boxes']

        bounding_boxes = []

        for bbox in response:
            bbox_elements = [int(element) for element in bbox.replace("[","").replace("]", "").split(",")]
            bounding_boxes.append(BoundingBox(*bbox_elements))

        return bounding_boxes

