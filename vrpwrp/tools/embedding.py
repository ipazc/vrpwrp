#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Numpy can be used to speed up comparison of embeddings.
try:
    import numpy as np
    NUMPY_LOADED = True
except Exception as ex:
    NUMPY_LOADED = False

__author__ = 'Iván de Paz Centeno'


class Embedding(object):
    """
    Represents the embeddings for a face.
    It is a set of float numbers that identifies a face.
    """

    def __init__(self, np_embedding, face_recognition=None):
        """
        Initializer for the embedding object.

        :param np_embedding: numpy array, list or string representing the numpy array of the embeddings.
        :param face_recognition: face recognition object to use when no numpy library is available. If not specified, it
        is going to use the default one.
        :return:
        """
        emb_type = type(np_embedding)

        if emb_type is str:
            if NUMPY_LOADED:
                self.np_embedding = np.fromstring(np_embedding.replace("[","").replace("]", ""), sep=" ")
            else:
                self.np_embedding = np_embedding

        elif NUMPY_LOADED and emb_type is np.ndarray:
            self.np_embedding = np_embedding

        elif emb_type is list:
            if NUMPY_LOADED:
                self.np_embedding = np.asarray(np_embedding)
            else:
                self.np_embedding = str(np_embedding).replace(",", " ")
        else:
            raise Exception("The NP-Embeddings must be a numpy array, a list of floats or a string representation.")

        if face_recognition is None:
            from vrpwrp.wrappers.face_recognition import FaceRecognition
            face_recognition = FaceRecognition()

        self.face_recognition = face_recognition

    @classmethod
    def from_dict(cls, dict_rep, face_recognition=None):
        """
        Builds the embedding from the dictionary representation.
        :param dict_rep:
        :return:
        """
        return cls(dict_rep['embedding'], face_recognition)

    def __sub__(self, other):
        """
        Subtracts other embedding to this embedding.
        :param other: Embedding object
        :return: Embedding object with the subtraction result.
        """
        if NUMPY_LOADED:
            result = float(np.sqrt(np.sum(np.square(np.subtract(self.np_embedding, other.np_embedding)))))
        else:
            result = self.face_recognition.get_embeddings_distance(self, other)

        return float(result)

    def get_embedding_np(self):
        """
        returns the internal NP_Embedding value. It might be a numpy ND-Array or a string depending on if Numpy is
        available or not.
        :return:
        """
        return self.np_embedding

    def to_dict(self):
        """
        Crafts a dictionary representation of this embedding.
        :return: dict representation of the embedding.
        """
        return {"embedding": str(self.np_embedding)}

    def __str__(self):
        """
        :return: String representation of the object.
        """
        return str(self.get_embedding_np())

    def __repr__(self):
        """
        :return: Representation of the object in the python interpreter
        """
        return str(self)