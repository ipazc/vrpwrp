#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import io
from PIL import Image
from vrpwrp.tools.boundingbox import BoundingBox

__author__ = 'Iván de Paz Centeno'


HORIZONTAL = 0
VERTICAL = 1

def get_file_binary_content(uri):
    with open(uri, "rb") as f:
        c = f.read()

    return c

def get_file_image(URI):
    image = Image.open(URI).convert("RGB")
    return image

def get_image(image_bytes):
    return Image.open(io.BytesIO(image_bytes)).convert("RGB")

def to_byte_array(pil_image):
    bytes_io = io.BytesIO()
    pil_image.save(bytes_io, "PNG")
    bytes_io.seek(0)
    return bytes_io

def crop_by_bbox(pil_image, bbox):

    box = bbox.get_box()
    box[2] += box[0]
    box[3] += box[1]

    crop_result = pil_image.crop((box[0], box[1], box[2], box[3]))

    return crop_result

def get_cropped_faces(image_bytes, bounding_boxes):
    return [crop_by_bbox(image_bytes, bounding_box) for bounding_box in bounding_boxes]

def segment_image(pil_image, segment_width, segment_height, iteration=HORIZONTAL):
    width, height = pil_image.size

    horizontal_segment_count = width // segment_width + int(width % segment_width > 0)
    vertical_segment_count = height // segment_height + int(height % segment_height > 0)

    if iteration==VERTICAL:
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