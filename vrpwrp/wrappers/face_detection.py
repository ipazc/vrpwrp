#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from urllib.request import urlopen
from vrpwrp.helpers import image_helper
from vrpwrp.config import config
from vrpwrp.tools.boundingbox import BoundingBox
from vrpwrp.wrappers.APIWrapper import APIWrapper

__author__ = 'Iván de Paz Centeno'


class FaceDetection(APIWrapper):
    """
    Wrapper for FaceDetection API, from Iván de Paz Centeno API-REST service.
    """
    def __init__(self, API_URL=None):
        """
        API URL for the Face detection algorithm.
        :param API_URL: URL for the face detection algorithm. By default it is going to use the public one.
        :return:
        """
        if API_URL is None:
            API_URL = config.FACE_DETECTION_API

        super().__init__(API_URL)

    def analyze_bytes(self, image_bytes):
        """
        Analyzes an incoming set of raw bytes corresponding to an image file and returns the bounding boxes detected.

        Supported extensions:
            Windows bitmaps - *.bmp, *.dib
            JPEG files - *.jpeg, *.jpg, *.jpe
            JPEG 2000 files - *.jp2
            Portable Network Graphics - *.png
            WebP - *.webp
            Portable image format - *.pbm, *.pgm, *.ppm *.pxm, *.pnm (always supported)
            Sun rasters - *.sr, *.ras
            TIFF files - *.tiff, *.tif
            OpenEXR Image files - *.exr
            Radiance HDR - *.hdr, *.pic

        :param image_bytes: array of bytes of an image.
        :return: list of bounding boxes detected inside the image.
        """

        response = self._request("PUT", data=image_bytes, is_binary=True)['bounding_boxes']

        bounding_boxes = []

        for bbox in response:
            bbox_elements = [int(element) for element in bbox.replace("[","").replace("]", "").split(",")]
            bounding_boxes.append(BoundingBox(*bbox_elements))

        return bounding_boxes

    def analyze_file(self, filename):
        """
        Analyzes a file image and returns the bounding boxes detected.

        Supported extensions:
            Windows bitmaps - *.bmp, *.dib
            JPEG files - *.jpeg, *.jpg, *.jpe
            JPEG 2000 files - *.jp2
            Portable Network Graphics - *.png
            WebP - *.webp
            Portable image format - *.pbm, *.pgm, *.ppm *.pxm, *.pnm (always supported)
            Sun rasters - *.sr, *.ras
            TIFF files - *.tiff, *.tif
            OpenEXR Image files - *.exr
            Radiance HDR - *.hdr, *.pic

        :param filename: URI pointing to the filename to analyze..
        :return: list of bounding boxes detected inside the image.
        """
        image_bytes = image_helper.get_file_binary_content(filename)

        return self.analyze_bytes(image_bytes)

    def analyze_url(self, url):
        """
        Downloads a URL resource and analyzes its content with @analyze_bytes()..

        :param url: url pointing to an image.
        :return: list of bounding boxes detected inside the image.
        """

        image_bytes = urlopen(url).read()
        bounding_boxes = self.analyze_bytes(image_bytes)
        return bounding_boxes

    def analyze_pil(self, pillow_image):
        """
        Analyzes the content of a Pillow image and returns the detected bounding boxes..

        :param pillow_image: pillow object representing an image..
        :return: list of bounding boxes detected inside the image.
        """

        image_bytes = image_helper.to_byte_array(pillow_image)
        bounding_boxes = self.analyze_bytes(image_bytes)
        return bounding_boxes
