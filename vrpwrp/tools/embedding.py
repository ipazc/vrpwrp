#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Iván de Paz Centeno'

PRINT_VALUE = 1
PRINT_NP_EMBEDDINGS = 2


class Embedding(object):

    def __init__(self, face_recognition, np_embedding, np_val, display_format=PRINT_NP_EMBEDDINGS):
        self.face_recognition = face_recognition
        self.np_embedding = np_embedding
        self.np_val = np_val
        self.display_format = display_format

    def get_val(self):
        """
        Returns the value of this embedding
        :return: a single float number representing this embedding.
        """
        return float(self.np_val)

    def __sub__(self, other):
        """
        Substracts other embedding to this embedding.
        :param other: Embedding object
        :return: Embedding object with the substraction result.
        """
        value = self.face_recognition.get_embeddings_distance(self, other)
        return Embedding(self.face_recognition, None, value, display_format=PRINT_VALUE)

    def get_embedding_np(self):
        return self.np_embedding

    def __float__(self):
        return float(str(self))

    def __int__(self):
        return int(float(self))

    def to_dict(self):
        return {"embedding": str(self.np_embedding), 'val': self.get_val()}

    def __str__(self):
        return str(self.get_val()) if self.display_format == PRINT_VALUE else self.get_embedding_np()
