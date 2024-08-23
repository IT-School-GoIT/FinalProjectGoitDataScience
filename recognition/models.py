from django.db import models

class UploadedImage(models.Model):
    image = models.ImageField(upload_to='images/')
    annotated_image = models.ImageField(upload_to='annotated_images/', null=True, blank=True)
    recognition_type = models.CharField(max_length=11, choices=[
        ('vgg16', 'VGG16'),
        ('faster_rcnn', 'Faster R-CNN'),
        ('mask_rcnn', 'Mask R-CNN')
    ])
    confidence_threshold = models.FloatField(default=0.5)
    result = models.TextField(blank=True, null=True)

