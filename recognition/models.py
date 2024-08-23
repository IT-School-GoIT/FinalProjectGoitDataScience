"""
models.py
=========

This module defines the models used in the image classification application. 
It includes the UploadedImage model, which is responsible for storing the uploaded 
images, annotated images, recognition types, confidence thresholds, and classification results.
"""
from django.db import models

class UploadedImage(models.Model):
    """
    UploadedImage model stores information about the uploaded images, their annotated versions,
    recognition types, confidence thresholds, and results.

    Attributes:
    ----------
    image : ImageField
        The uploaded image to be classified.
    annotated_image : ImageField
        The image with annotations after recognition (optional).
    recognition_type : CharField
        The type of recognition model used (VGG16, Faster R-CNN, Mask R-CNN).
    confidence_threshold : FloatField
        The confidence threshold used for object detection.
    result : TextField
        The result of the classification/recognition process.
    """    
    image = models.ImageField(upload_to='images/')
    annotated_image = models.ImageField(upload_to='annotated_images/', null=True, blank=True)
    recognition_type = models.CharField(max_length=11, choices=[
        ('vgg16', 'VGG16'),
        ('faster_rcnn', 'Faster R-CNN'),
        ('mask_rcnn', 'Mask R-CNN')
    ])
    confidence_threshold = models.FloatField(default=0.5)
    result = models.TextField(blank=True, null=True)

