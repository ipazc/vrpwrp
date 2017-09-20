#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import unittest
from PIL import Image
from vrpwrp.helpers import image_helper
import io
from vrpwrp.tools.boundingbox import BoundingBox

__author__ = 'Iván de Paz Centeno'


class TestImageHelper(unittest.TestCase):
    """
    Unit tests for the class FaceRecognition
    """

    def setUp(self):
        """
        Sets up the testing subject!
        """
        self.subject = "vrpwrp/samples/subject2_2.jpg" # Hello MR Trump

    def test_get_file_binary_content(self):
        """
        Tests that the image helper can retrieve content from a file.
        """
        content = image_helper.get_file_binary_content(self.subject)

        self.assertGreater(len(content), 0)

        with open(self.subject, "rb") as f:
            original_content = f.read()

        self.assertEqual(content, original_content)

    def test_get_file_image(self):
        """
        Tests that the image helper can retrieve the PIL image from the file.
        """
        image = image_helper.get_file_image(self.subject)

        self.assertEqual(image.size, (800, 450))

    def test_get_image(self):
        """
        Tests that the image helper can retrieve the image from an array of bytes
        """
        with open(self.subject, "rb") as f:
            content = f.read()

        image = image_helper.get_image(content)

        self.assertEqual(image.size, (800, 450))

    def test_to_byte_array(self):
        """
        Tests that the image helper can convert PIL image to a byte array.
        """
        with Image.open(self.subject) as im:
            image = im.convert("RGB")

        byte_array = image_helper.to_byte_array(image)

        self.assertGreater(len(byte_array), 0)

    def test_get_image_and_to_byte_array_are_compatible(self):
        """
        Tests that the helper's got image can be converted to a byte array that can be converted back to an image with same
        format.
        """

        with open(self.subject, "rb") as f:
            content = f.read()

        image = image_helper.get_image(content)

        self.assertEqual(image.size, (800, 450))

        bytes_array = image_helper.to_byte_array(image)

        image = image_helper.get_image(bytes_array)

        self.assertEqual(image.size, (800, 450))

    def test_crop_by_bbox(self):
        """
        Tests that the image helper can crop an image successfully by a bounding box.
        """
        with Image.open(self.subject) as im:
            image = im.convert("RGB")

        cropped = image_helper.crop_by_bbox(image, BoundingBox(0,0,15,15))

        self.assertEqual(cropped.size, (15, 15))

    def test_get_cropped_faces(self):
        """
        Tests that the image helper can crop an image successfully by multiple bounding boxes.
        """
        with Image.open(self.subject) as im:
            image = im.convert("RGB")

        cropped_list = image_helper.get_cropped_faces(image, [BoundingBox(0,0,15,15), BoundingBox(20,20,45,45)])

        self.assertEqual(cropped_list[0].size, (15, 15))
        self.assertEqual(cropped_list[1].size, (45, 45))

    def test_segment_image(self):
        """
        Tests that the image helper can segment an image successfully.
        """
        with Image.open(self.subject) as im:
            image = im.convert("RGB")

        segment_generator = image_helper.segment_image(image, 200, 200)

        sizes = [
            ((200, 200), next(segment_generator)),
            ((200, 200), next(segment_generator)),
            ((200, 200), next(segment_generator)),
            ((200, 200), next(segment_generator)),
            ((200, 200), next(segment_generator)),
            ((200, 200), next(segment_generator)),
            ((200, 200), next(segment_generator)),
            ((200, 200), next(segment_generator)),
            ((200, 50), next(segment_generator)),
            ((200, 50), next(segment_generator)),
            ((200, 50), next(segment_generator)),
            ((200, 50), next(segment_generator))
        ]

        for size, segment in sizes:
            self.assertEqual(size, segment.size)


if __name__ == '__main__':
    unittest.main()