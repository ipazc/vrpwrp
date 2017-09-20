#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
from vrpwrp.tools.boundingbox import BoundingBox


__author__ = 'Iván de Paz Centeno'


class TestBoundingBox(unittest.TestCase):
    """
    Unitary tests for the BoundingBox class.
    """

    def setUp(self):
        """
        Definition of some common rect values for the tests.
        """
        #                   rect1              rect2                 area_intersection  percentage
        self.rect_sets = [[[80, 60, 250, 170], [200, 130, 200, 170], 13000,             38.24],
                          [[80, 60, 40, 170], [200, 130, 200, 170],  0,                 0.00]]

    def test_expand(self):
        """
        Tests the expansion of bounding box.
        """
        box1 = BoundingBox(3,3,100,100)
        box1.expand() # expand a default of 20%
        self.assertEqual(box1.get_box(), [-7,-7,120,120])   # If you see something weird here,
                                                            # remember that it is the width and height and not coords

    def test_bounding_box_from_string(self):
        """
        Tests the creation a bounding box from a string.
        """
        bbox_string = "22,34,122,432"
        bbox = BoundingBox.from_string(bbox_string)

        self.assertEqual(bbox.get_box(), [22, 34, 122, 432])

        bbox_string = "22, 34,122,432"
        bbox = BoundingBox.from_string(bbox_string)

        self.assertEqual(bbox.get_box(), [22, 34, 122, 432])

        bbox_string = "22, 34, 122, 432"
        bbox = BoundingBox.from_string(bbox_string)

        self.assertEqual(bbox.get_box(), [22, 34, 122, 432])

        bbox_string = "   22, 34, 122, 432   "
        bbox = BoundingBox.from_string(bbox_string)

        self.assertEqual(bbox.get_box(), [22, 34, 122, 432])

        with self.assertRaises(Exception):
            bbox_string = "22,34,122 432"
            bbox = BoundingBox.from_string(bbox_string)

        with self.assertRaises(Exception):
            bbox_string = "22,34  122 432"
            bbox = BoundingBox.from_string(bbox_string)

    def test_fit_in_size(self):
        """
        Tests that bounding box is able to adapt itself to specified bounds.
        """
        image_size = [300, 300]

        # Case1 all out of bounds
        box1 = BoundingBox(-1, -1, 302, 302)
        box1.fit_in_size(image_size)
        self.assertEqual(box1.get_box(), [0, 0, 300, 300])

        # Case2 top left out of bounds
        box1 = BoundingBox(-1,-1,301,301)
        box1.fit_in_size(image_size)
        self.assertEqual(box1.get_box(), [0, 0, 300, 300])

        # Case left out of bounds
        box1 = BoundingBox(-15, 10, 100, 100)
        box1.fit_in_size(image_size)
        self.assertEqual(box1.get_box(), [0, 10, 85, 100])

        # Case top out of bounds
        box1 = BoundingBox(15, -10, 100, 100)
        box1.fit_in_size(image_size)
        self.assertEqual(box1.get_box(), [15, 0, 100, 90])

        # Case width out of bounds
        box1 = BoundingBox(15, 0, 290, 100)
        box1.fit_in_size(image_size)
        self.assertEqual(box1.get_box(), [15, 0, 285, 100])

        # Case height out of bounds
        box1 = BoundingBox(15, 15, 200, 290)
        box1.fit_in_size(image_size)
        self.assertEqual(box1.get_box(), [15, 15, 200, 285])

    def test_get_box(self):
        """
        Tests that bounding box successfully returns the array of the box dimensions.
        """
        box = BoundingBox(15, 16, 17, 18)
        self.assertEqual(box.get_box(), [15, 16, 17, 18])

    def test_get_box_coord(self):
        """
        Tests that bounding box successfully returns the array of the box in coordinates version.
        """
        box = BoundingBox(15, 16, 17, 18)
        self.assertEqual(box.get_box_coord(), [[15, 16], [32, 16], [15, 34], [32, 34]])

    def test_get_components(self):
        """
        Tests that bounding box isolated components are accessible.
        """
        box = BoundingBox(15, 16, 17, 18)
        self.assertEqual(box.get_x(), 15)
        self.assertEqual(box.get_y(), 16)
        self.assertEqual(box.get_width(), 17)
        self.assertEqual(box.get_height(), 18)

    def test_get_numpy_format(self):
        """
        Tests that bounding box numpy format is correct.
        """
        box = BoundingBox(15, 16, 17, 18)
        self.assertEqual(box.get_numpy_format(), [16, 34, 15, 32])

    def test_str(self):
        """
        Tests that bounding box describes itself correctly.
        """
        box = BoundingBox(15, 16, 17, 18)
        self.assertEqual(box.__str__(), "[15, 16, 17, 18]")

    def test_intersection_with_other_boundingbox(self):
        """
        Tests that bounding box intersects itself with other bounding boxes.
        """
        for rect_set in self.rect_sets:
            rect1 = rect_set[0]
            rect2 = rect_set[1]
            expectedArea = rect_set[2]
            expectedPercentage = rect_set[3]

            box1 = BoundingBox(*rect1)
            box2 = BoundingBox(*rect2)

            intersection = box1.intersect_with(box2)
            number_of_common_pixels = intersection.get_area()

            # Which one is the smaller rectangle?
            area_box1 = box1.get_area()
            area_box2 = box2.get_area()

            lesser_area = min(area_box1, area_box2)
            percentage = round((number_of_common_pixels / lesser_area) * 100, 2)

            self.assertEqual(number_of_common_pixels, expectedArea)
            self.assertEqual(percentage, expectedPercentage)

    def test_center(self):
        """
        Tests that bounding box knows its center point.
        """
        box = BoundingBox(10, 10, 20, 20)
        self.assertEqual(box.get_center(), [20, 20])

    def test_area(self):
        """
        Tests that bounding box knows its area.
        """
        box = BoundingBox(10, 10, 20, 20)
        self.assertEqual(box.get_area(), 400)

if __name__ == '__main__':
    unittest.main()
