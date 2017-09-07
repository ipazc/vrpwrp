==============
VRPWRP 0.0.2
==============
VRPWRP (Vision-algorithm Requests Processing Wrappers) is a package that wraps an API-REST for Computer Vision deep-learning algorithms. Currently, it supports state-of-the-art a face-detection and face-recognition algorithms out-of-the-box. 

Installation
============
Currently it is only supported Python 3.4.1 onwards:

.. code:: bash
    
    sudo pip3 install vrpwrp

Face detection
===============
Face detection allows you to retrieve the location of faces inside images in the form of bounding boxes (left, top, width, height).

A simple example for retrieving the bounding boxes of faces from an image:

.. code:: python

    >>> from vrpwrp.wrappers.face_detection import FaceDetection
    >>> face_detection = FaceDetection()
    >>> bounding_boxes = face_detection.analyze_file("route/to/image.jpg")
    >>> for bb in bounding_boxes: print(bb)
    ... 
    [162, 79, 114, 146]

FaceDetection has methods for analyzing images also from bytes, URLs and pillow images directly:

.. code:: python

    >>> bounding_boxes = face_detection.analyze_bytes(image_bytes)
    >>> bounding_boxes = face_detection.analyze_url(image_url)
    >>> bounding_boxes = face_detection.analyze_pil(pillow_image)
    ... 


Face Recognition
================
Face recognition allows extracting the identity of a face within a given image of the face. The identity is a set of float numbers (since it is deep-learning-based, it is the output of the last convolution layer of a Convolutional Neural Network). In vrpwrp it is called **embeddings**.

A simple example for retrieving the embeddings of a face is:

.. code:: python

    >>> from vrpwrp.wrappers.face_recognition import FaceRecognition
    >>> face_recognition = FaceRecognition()
    >>> face_embeddings = face_recognition.get_embeddings_from_file("route/to/image_of_face.jpg")
    >>> print(face_embeddings)
    [-0.05258641 -0.14807236  0.21828972  0.00097196  0.08881456  0.01356898 -0.01393933 -0.09459263 -0.07305822  0.00354048  0.1649337  -0.05636634  0.03599492 -0.02649886 ...]

Like in FaceDetection, it allows to analyze images from different sources:

.. code:: python

    >>> embeddings = face_recognition.get_embeddings_from_bytes(image_bytes)
    >>> embeddings = face_recognition.get_embeddings_from_url(image_url)
    >>> embeddings = face_recognition.get_embeddings_from_pil(pillow_image)
    ... 



The embeddings of two faces can be easily compared to see how close they are:

.. code:: python

    >>> face1_embeddings = face_recognition.get_embeddings_from_file("route/to/image_of_face1.jpg")
    >>> face2_embeddings = face_recognition.get_embeddings_from_file("route/to/image_of_face2.jpg")
    >>> print(face1_embeddings - face2_embeddings)
    0.5634614628831894

A value close to 0 indicates that two faces might be of the same person. In this example, image_of_face1.jpg and image_of_face2.jpg are likely to be of the same person. Otherwise, a value over 1.0 might indicate that two faces are not likely to be of the same person.

This might lead to a scenario where you store lot of embeddings and want to compare a single one with each of them, resulting in a loop like the following:

.. code:: python

    faces_embeddings = [emb1, emb2, ..., embN]

    new_embedding = face_recognition.get_embeddings_from_file("route/to/image_of_face1.jpg")

    for embedding in faces_embeddings:
         distance = embedding - new_embedding

Rather than using a loop (even if it is a list-comprehension), there is an optimized and preferred way of performing such a comparison that can be used instead:

.. code:: python

    faces_embeddings = [emb1, emb2, ..., embN]

    new_embedding = face_recognition.get_embeddings_from_file("route/to/image_of_face1.jpg")
    distances = face_recognition.get_embeddings_distances(new_embedding, faces_embeddings)

