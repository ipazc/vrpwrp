#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
from vrpwrp.wrappers.face_detection import FaceDetection

__author__ = 'Iván de Paz Centeno'


class TestFaceDetection(unittest.TestCase):
    """
    Unit tests for the class FaceDetection
    """
    def test_detect_faces_file(self):
        """
        Tests the detection of faces from a file.
        """
        face_detection = FaceDetection()
        bounding_boxes = face_detection.analyze_file("vrpwrp/examples/subject3_3.jpg")
        self.assertEqual(len(bounding_boxes), 1)


if __name__ == '__main__':
    unittest.main()
