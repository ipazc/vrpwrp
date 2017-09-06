#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
from vrpwrp.config import config
from vrpwrp.tools.embedding import Embedding
from vrpwrp.wrappers.APIWrapper import APIWrapper

__author__ = 'Iván de Paz Centeno'


class FaceRecognition(APIWrapper):
    def __init__(self, API_URL=None):
        if API_URL is None:
            API_URL = config.FACE_RECOGNITION_API

        super().__init__(API_URL)

    def get_embedding(self, image_bytes):
        response = self._request("GET", data=image_bytes, is_binary=True)['embedding_data']
        embedding = Embedding(self, response['embedding'], response['val'])
        return embedding

    def get_embeddings_distance(self, embedding1, embedding2):
        return self.get_embeddings_distances(embedding1, [embedding2])[0]

    def get_embeddings_distances(self, embedding_who, embeddings_list):
        data={'who': str(embedding_who), 'subjects': [str(embedding) for embedding in embeddings_list]}
        values = self._request("PUT", data=json.dumps(data))['distances']
        return [float(val) for val in values]

