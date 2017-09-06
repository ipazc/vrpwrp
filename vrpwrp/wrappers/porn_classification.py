#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from vrpwrp.config import config
from vrpwrp.helpers import image_helper
from vrpwrp.wrappers.APIWrapper import APIWrapper

__author__ = 'Iván de Paz Centeno'


class PornClassification(APIWrapper):
    def __init__(self, API_URL=None):
        if API_URL is None:
            API_URL = config.PORN_CLASSIFICATION_API

        super().__init__(API_URL)

    def get_score(self, image_bytes):
        try:
            response = self._request("PUT", data=image_bytes, is_binary=True)['Image Result']
            porn_score = float(response['Porn Score'])
        except:
            porn_score = 0.0

        return porn_score

    def get_score_segmented(self, image_bytes, segments_width=1024, segments_height=1024):
        porn_scores = []

        image = image_helper.get_image(image_bytes)

        try:
            for pil_image in image_helper.segment_image(image, segments_width, segments_height):
                response = self._request("PUT", data=image_helper.to_byte_array(pil_image), is_binary=True)['Image Result']
                score = float(response['Porn Score'])
                porn_scores.append(score)
                print(score)

        except:
            pass

        return porn_scores

    def is_porn(self, image_bytes):
        scores = self.get_score_segmented(image_bytes)
        return any([score >= 0.5 for score in scores])