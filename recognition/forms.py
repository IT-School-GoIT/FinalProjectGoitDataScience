from django import forms
from .models import UploadedImage


class UploadImageForm(forms.ModelForm):
    recognition_type = forms.ChoiceField(
        choices=[
            ('vgg16', 'Custom VGG16 (Full Image)'),
            ('faster_rcnn', 'Faster R-CNN + Custom VGG16 (Segmented)'),
            ('mask_rcnn', 'Mask R-CNN + Custom VGG16 (Segmented)'),
        ],
        initial='vgg16',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    confidence_threshold = forms.FloatField(min_value=0.1, max_value=1.0, initial=0.5,
                                            widget=forms.NumberInput(attrs={'step': '0.05'}))

    class Meta:
        model = UploadedImage
        fields = ['image', 'recognition_type', 'confidence_threshold']
        widgets = {
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
