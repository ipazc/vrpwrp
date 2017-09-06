#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from urllib.request import urlopen
from vrpwrp.helpers import image_helper
from vrpwrp.wrappers.face_detection import FaceDetection
from vrpwrp.wrappers.face_recognition import FaceRecognition

__author__ = 'Iván de Paz Centeno'


class FaceBundle(object):

    def __init__(self, face_detection=None, face_recognition=None):
        if face_detection is None:
            face_detection = FaceDetection()

        if face_recognition is None:
            face_recognition = FaceRecognition()

        self.face_detection = face_detection
        self.face_recognition = face_recognition

    def process_file(self, uri):
        bounding_boxes = self.face_detection.analyze_file(uri)
        image = image_helper.get_image(image_bytes)
        cropped_images = [image_helper.crop_by_bbox(image, bb) for bb in bounding_boxes]
        embeddings = [self.face_recognition.get_embedding_from_pil(cropped).get_embedding_np() for cropped in cropped_images]

        return embeddings

    def process_url(self, url):
        image_bytes = urlopen(url).read()
        bounding_boxes = self.face_detection.analyze_bytes(image_bytes)
        image = image_helper.get_image(image_bytes)
        cropped_images = [image_helper.crop_by_bbox(image, bb) for bb in bounding_boxes]
        embeddings = [self.face_recognition.get_embedding_from_pil(cropped).get_embedding_np() for cropped in cropped_images]

        return embeddings