#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
from urllib.request import urlopen
from vrpwrp.helpers import image_helper
from vrpwrp.config import config
from vrpwrp.tools.embedding import Embedding
from vrpwrp.wrappers.APIWrapper import APIWrapper

__author__ = 'Iván de Paz Centeno'


class FaceRecognition(APIWrapper):
    """
    Wrapper for FaceRecognition API, from Iván de Paz Centeno API-REST service.
    """
    def __init__(self, API_URL=None):
        """
        API URL for the Face recognition algorithm.
        :param API_URL: URL for the face recognition algorithm. By default it is going to use the public one.
        :return:
        """
        if API_URL is None:
            API_URL = config.FACE_RECOGNITION_API

        super().__init__(API_URL)

    def get_embedding_from_bytes(self, image_bytes):
        """
        Retrieves the face embedding for the given raw array of bytes of an image file.

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

        :param image_bytes: array of bytes of the image to process.
        :return: embedding string representing the image of the face.
        """
        response = self._request("GET", data=image_bytes, is_binary=True)['embedding_data']
        embedding = Embedding(self, response['embedding'], response['val'])
        return embedding

    def get_embeddings_from_file(self, filename):
        """
        Analyzes a file image and returns the embeddings of the face.

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
        :return: embedding string representing the image of the face.
        """
        image_bytes = image_helper.get_file_binary_content(filename)

        return self.get_embedding_from_bytes(image_bytes)

    def get_embedding_from_url(self, url):
        """
        Retrieves the face embedding for the image hosted in the given url.

        :param url: url pointing to an image.
        :return: embedding string representing the image of the face.
        """
        image_bytes = urlopen(url).read()
        response = self._request("GET", data=image_bytes, is_binary=True)['embedding_data']
        embedding = Embedding(self, response['embedding'], response['val'])
        return embedding

    def get_embedding_from_pil(self, pillow_image):
        """
        Retrieves the face embedding for the given pillow image.

        :param pillow_image: pillow image to process..
        :return: embedding string representing the image of the face.
        """
        image_bytes = image_helper.to_byte_array(pillow_image)
        response = self._request("GET", data=image_bytes, is_binary=True)['embedding_data']
        embedding = Embedding(self, response['embedding'], response['val'])
        return embedding

    def get_embeddings_distance(self, embedding1, embedding2):
        """
        Computes the distance between two embeddings. The distance is a float number.
        The closest the distance (nearest to 0), the most likely to belong to the same face.
        Generally it can be considered that a distance over 1.0 might indicate that the faces are from different
        persons.

        :param embedding1: embedding string for face 1.
        :param embedding2: embedding string for face 2.
        :return: the distance between both embeddings, in float format.
        """
        return self.get_embeddings_distances(embedding1, [embedding2])[0]

    def get_embeddings_distances(self, embedding_who, embeddings_list):
        """
        Computes the distances between an embedding and a list of embeddings. This method is optimal for processing a
        comparison against multiple embeddings, rather than going in a loop one by one.
        :param embedding_who: embedding that wants to be compared.
        :param embeddings_list: the list of embeddings to compare to.
        :return: an array of the distances between the embedding_who and each of the embeddings in the embeddings_list.
        """
        data={'who': str(embedding_who), 'subjects': [str(embedding) for embedding in embeddings_list]}
        values = self._request("PUT", data=json.dumps(data))['distances']
        return [float(val) for val in values]

