#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json

__author__ = 'Iván de Paz Centeno'


class BoundingBox(object):
    """
    Represents a virtual bounding box and offers some basics operations on it, like
    calculating the area, the intersection with other bounding box or the center.
    """

    def __init__(self, x, y, width, height):
        """
        Builds a bounding box object wrapping the coordinates of the top-left corner of the rect and its width and
        height.

        :param x: top-left x coordinate
        :param y: top-left y coordinate
        :param width: size of the width.
        :param height: size of the height.
        """
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def get_box(self):
        """
        :return:
        Returns the top-left position of the box and its width and height, as a vector of 4 positions.
        """
        return [self.x, self.y, self.width, self.height]

    def get_box_coord(self):
        """
        Computes the coordinates of the four corners of the rect.
        The coordinates of each corner are wrapped inside a vector.


        :return: the coordinates of each corner of the rect as a vector of 4 positions.
        """
        return [[self.x, self.y], [self.x+self.width, self.y],
                [self.x, self.y+self.height], [self.x+self.width, self.y+self.height]]

    def get_x(self):
        """
        Getter for x coord
        :return:
        """
        return self.x

    def get_y(self):
        """
        Getter for y coord
        :return:
        """
        return self.y

    def get_width(self):
        """
        Getter for width
        :return:
        """
        return self.width

    def get_height(self):
        """
        Getter for height
        :return:
        """
        return self.height

    def get_numpy_format(self):
        """
        Computes a numpy format.
        :return: array of [y, y+height, x, x+width]
        """
        return [self.y, self.y+self.height, self.x, self.x + self.width]

    def intersect_with(self, other_bounding_box):
        """
        Builds the intersection box from this box with the specified bounding box.

        :param other_bounding_box: the bounding box to intersect with.
        :return: the bounding box that corresponds to the intersection box. If the specified box does not intersect
        with the current box, the result will be a bounding box with an area of 0.
        """
        bbox1_coords = self.get_box_coord()
        bbox2_coords = other_bounding_box.get_box_coord()

        bbox1_first_coord = bbox1_coords[0]
        bbox2_first_coord = bbox2_coords[0]

        bbox1_last_coord = bbox1_coords[3]
        bbox2_last_coord = bbox2_coords[3]

        intersection_first_coord = [0, 0]
        intersection_last_coord = [0, 0]

        if bbox1_first_coord[0] >= bbox2_first_coord[0]:
            intersection_first_coord[0] = bbox1_first_coord[0]
        else:
            intersection_first_coord[0] = bbox2_first_coord[0]

        if bbox1_first_coord[1] >= bbox2_first_coord[1]:
            intersection_first_coord[1] = bbox1_first_coord[1]
        else:
            intersection_first_coord[1] = bbox2_first_coord[1]

        if bbox1_last_coord[0] <= bbox2_last_coord[0]:
            intersection_last_coord[0] = bbox1_last_coord[0]
        else:
            intersection_last_coord[0] = bbox2_last_coord[0]

        if bbox1_last_coord[1] <= bbox2_last_coord[1]:
            intersection_last_coord[1] = bbox1_last_coord[1]
        else:
            intersection_last_coord[1] = bbox2_last_coord[1]

        # condition: intersectionFirstCoord never can be greater than intersectionLastCoord
        if intersection_first_coord[0] >= intersection_last_coord[0] \
                or intersection_first_coord[1] >= intersection_last_coord[1]:
            intersection_bounding_box = BoundingBox(0, 0, 0, 0)
        else:
            intersection_bounding_box = BoundingBox(intersection_first_coord[0], intersection_first_coord[1],
                                                    intersection_last_coord[0] - intersection_first_coord[0],
                                                    intersection_last_coord[1] - intersection_first_coord[1])

        return intersection_bounding_box

    def get_area(self):
        """
            Computes the area of the current box.

        :return: the area of the current box.
        """
        return self.width*self.height

    def get_center(self):
        """
        Computes the center of the bounding box
        :return: array (point 2D) of the center.
        """
        return [int(self.x + self.width/2), int(self.y + self.height/2)]

    def expand(self, proportion=0.2):
        """
        Expands the current box area in a given proportion.
        The size expanded is applied to all the limits of the box

        WARNING: The box may end up out of bounds. Call fit_in_size with the boundings to adapt it.
        :param proportion:
        """
        horizontally = int((self.width * proportion) / 2)
        vertically = int((self.height * proportion) / 2)
        self.x -= horizontally
        self.y -= vertically
        self.width += horizontally * 2
        self.height += vertically * 2

    def fit_in_size(self, size_limit):
        """
        Adapts the size of the box in order to avoid exceeding the bounds specified in size_limit

        :param size_limit: bound limits. For example [300, 400] for a maximum width of 300 and 400 for maximumg height.
        """
        if self.x < 0:
            self.width += self.x   # self.x is negative
            self.x = 0

        elif self.x >= size_limit[0]: # Invalid box
            self.x = 0
            self.width = 0

        if self.x + self.width >= size_limit[0]:
            self.width = size_limit[0] - self.x

        if self.y < 0:
            self.height += self.y   # self.y is negative
            self.y = 0

        elif self.y >= size_limit[1]: # Invalid box
            self.y = 0
            self.height = 0

        if self.y + self.height >= size_limit[1]:
            self.height = size_limit[1] - self.y

    def to_dict(self):
        """
        :return: JSON-Compatible dictionary representation of the age.
        """
        return [self.x, self.y, self.width, self.height]

    def __str__(self):
        """
        :return: string representation of the age.
        """
        return json.dumps(self.to_dict())

    def __repr__(self):
        """
        :return: representation string to display in console directly, rather than "BoundingBox object".
        """
        return "BoundingBox: {}".format(self.to_dict())

    @classmethod
    def from_string(cls, bounding_box_string):
        """
        Creates an instance of the bounding box by giving a string.
        :param bounding_box_string: string of the format "x,y,width,height"
        :return: instance of boundingbox matching the string.
        """
        bbox_elements = bounding_box_string.split(",")

        if len(bbox_elements) != 4:
            raise Exception("bounding box string doesn't contain a bounding box.")

        x = int(bbox_elements[0].strip())
        y = int(bbox_elements[1].strip())
        width = int(bbox_elements[2].strip())
        height = int(bbox_elements[3].strip())

        result = cls(x, y, width, height)

        return result