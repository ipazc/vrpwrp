#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import io
from PIL import Image
from vrpwrp.tools.boundingbox import BoundingBox

__author__ = 'Iván de Paz Centeno'


HORIZONTAL = 0
VERTICAL = 1

def get_file_binary_content(uri):
    """
    Retrieves the binary content of a file URI.
    :param uri: path to the file to be loaded
    :return: raw bytes list of the file content.
    """
    with open(uri, "rb") as f:
        c = f.read()

    return c

def get_file_image(uri):
    """
    Retrieves the file as a PIL image.
    :param uri: path to the file to be loaded
    :return: PIL image representing the loaded image.
    """
    with Image.open(uri) as im:
        image = im.convert("RGB")
    return image

def get_image(image_bytes):
    """
    Retrieves the PIL image from the given array of bytes.
    :param image_bytes: bytes to convert into a PIL image.
    :return: PIL image.
    """
    with Image.open(io.BytesIO(image_bytes)) as im:
        image = im.convert("RGB")
    return image

def to_byte_array(pil_image):
    """
    converts the PIL image into a bytes array.
    :param pil_image: PIL image to convert to
    :return: Bytes array representing the image.
    """
    with io.BytesIO() as bytes_io:
        pil_image.save(bytes_io, "PNG")
        bytes_io.seek(0)
        result = bytes_io.read()

    return result

def crop_by_bbox(pil_image, bbox):
    """
    Crops the specified PIL image with the given bounding box
    :param pil_image: PIL image to crop
    :param bbox: bounding box object to crop by
    :return: PIL image cropped.
    """
    box = bbox.get_box()
    box[2] += box[0]
    box[3] += box[1]

    crop_result = pil_image.crop((box[0], box[1], box[2], box[3]))

    return crop_result

def get_cropped_faces(pil_image, bounding_boxes):
    """
    Crops the specified PIL image by the specified bounding boxes
    :param pil_image: PIL image to crop by
    :param bounding_boxes: bounding boxes list to crop image.
    :return: A list of cropped images.
    """
    return [crop_by_bbox(pil_image, bounding_box) for bounding_box in bounding_boxes]

def segment_image(pil_image, segment_width, segment_height, iteration_order=HORIZONTAL):
    """
    Generator of segments of a PIL image. This generator breaks the PIL image into a
    subset of PIL images. Like in a Puzzle, it returns one by one on each iteration_order. The iteration_order order can be
     HORIZONTAL (going from TOP-LEFT to TOP-RIGHT) or VERTICAL (going from TOP-LEFT to BOTTOM-LEFT).
    :param pil_image: Image to segment.
    :param segment_width: the width of the fragment.
    :param segment_height: the height of the fragment.
    :param iteration_order: order of the iteration_order.
    :return:
    """
    width, height = pil_image.size

    horizontal_segment_count = width // segment_width + int(width % segment_width > 0)
    vertical_segment_count = height // segment_height + int(height % segment_height > 0)

    if iteration_order==VERTICAL:
        for x in range(horizontal_segment_count):
            for y in range(vertical_segment_count):
                bounding_box = BoundingBox(x * segment_width, y * segment_height,
                                           min(segment_width, width - x * segment_width),
                                           min(segment_height, height - y * segment_height))

                yield crop_by_bbox(pil_image, bounding_box)
    else:
        for y in range(horizontal_segment_count):
            for x in range(vertical_segment_count):
                bounding_box = BoundingBox(x * segment_width, y * segment_height,
                                           min(segment_width, width - x * segment_width),
                                           min(segment_height, height - y * segment_height))

                yield crop_by_bbox(pil_image, bounding_box)
