
"""
views.py
=========

This module contains views and helper functions for image classification and recognition using models like VGG16, Faster R-CNN, and Mask R-CNN.
"""
import os
import io

import gdown
import torch
import numpy as np
import matplotlib
from django.http import Http404

matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image
from skimage import measure
from torchvision import models, transforms
import torchvision.transforms.functional as TF

from django.shortcuts import render, redirect
from django.utils.translation import gettext as _
from django.core.files.base import ContentFile

from .forms import UploadImageForm
from .models import UploadedImage
from .classes import class_names


def load_model_from_google_drive(file_id, model_name, download_if_exists=False):
    """
    Downloads a model file from Google Drive and loads it into memory using PyTorch.

    Args:
        file_id (str): The unique identifier for the file on Google Drive.
        model_name (str): The name of the model file to save on the local disk.
        download_if_exists (bool): If True, the model will be re-downloaded even if it already exists locally.
                                    If False, the model will be loaded from the local disk if it exists.

    Returns:
        torch.nn.Module: The PyTorch model loaded from the specified file.

    Raises:
        RuntimeError: If the model file cannot be loaded.
    """
    model_dir = 'media/models'
    if not os.path.exists(model_dir):
        os.makedirs(model_dir)

    model_path = os.path.join(model_dir, model_name)

    try:
        if os.path.exists(model_path) and not download_if_exists:
            print(f"Model already exists at {model_path}. Loading from disk.")
        else:
            print(f"Downloading model to {model_path}...")
            gdown.download(id=file_id, output=model_path, quiet=False)

        model = torch.load(model_path, map_location=torch.device('cpu'))
        return model

    except gdown.exceptions.RequestError as e:
        raise RuntimeError(f"Failed to download the model from Google Drive. Error: {e}")
    except FileNotFoundError:
        raise RuntimeError(f"The model file was not found after download. Check if the path is correct: {model_path}")
    except RuntimeError as e:
        raise RuntimeError(f"Failed to load the model from the file. Error: {e}")
    except Exception as e:
        raise RuntimeError(f"An unexpected error occurred: {e}")



def result(request, image_id):
    """
    Retrieves an uploaded image from the database using its ID and renders a template to display the image.

    Args:
        request (HttpRequest): The HTTP request object.
        image_id (int): The unique identifier of the uploaded image in the database.

    Returns:
        HttpResponse: The rendered HTML page to display the image.

    Raises:
        Http404: If no image is found with the given ID.
    """
    try:
        uploaded_image = UploadedImage.objects.get(id=image_id)
    except UploadedImage.DoesNotExist:
        raise Http404(_("Image not found"))

    return render(request, 'recognition/recognition.html', {'uploaded_image': uploaded_image, "title": _("Пізнання")})


def index(request):
    """
    Handles image upload and processing based on the selected recognition type.
    Saves the uploaded image and its processing results in the database.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Redirects to the result page after processing the image if the request is POST.
                      Otherwise, renders the upload form.

    Raises:
        ValueError: If the recognition type is invalid or any other processing issue occurs.
    """
    if request.method == 'POST':
        form = UploadImageForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.cleaned_data['image']
            recognition_type = form.cleaned_data['recognition_type']
            confidence_threshold = form.cleaned_data['confidence_threshold']
            img = Image.open(image)

            try:
                if recognition_type == 'vgg16':
                    result = recognize_with_vgg16(img)
                    annotated_image = None
                elif recognition_type == 'faster_rcnn':
                    result, annotated_image = recognize_with_faster_rcnn(img, confidence_threshold)
                elif recognition_type == 'mask_rcnn':
                    result, annotated_image = recognize_with_mask_rcnn(img, confidence_threshold)
                else:
                    raise ValueError("Invalid recognition type selected.")

                uploaded_image = form.save(commit=False)
                uploaded_image.result = result
                if annotated_image:
                    uploaded_image.annotated_image.save(annotated_image.name, annotated_image)
                uploaded_image.save()

                return redirect('recognition:result', uploaded_image.id)
            except Exception as e:
                # Handle unexpected errors and provide a user-friendly message
                form.add_error(None, _("An error occurred during processing: ") + str(e))
        else:
            # If form is not valid, add a general error message
            form.add_error(None, _("Please correct the errors below."))

    else:
        form = UploadImageForm(initial={'recognition_type': 'vgg16'})

    return render(request, 'recognition/cognition.html', {'form': form, "title": _("Recognition"), "page": "cognition", "app": "home"})


def recognize_with_vgg16(img):
    """
    Recognizes the class of an image using a pre-trained VGG16 model fine-tuned on the CIFAR-10 dataset.

    Args:
        img (PIL.Image.Image): The input image to be recognized.

    Returns:
        str: The name of the predicted class and its probability as a percentage.

    Raises:
        ValueError: If the image is not in RGB mode or if any error occurs during processing.
    """
    try:
        # Ensure the image is in RGB mode
        if img.mode != 'RGB':
            img = img.convert('RGB')

        # Resize the image to match the input size used during training
        img = img.resize((32, 32))

        # Transform the image to a tensor and add a batch dimension
        img_tensor = transform(img).unsqueeze(0)

        # Perform inference without tracking gradients
        with torch.no_grad():
            output = vgg16(img_tensor)

        # Apply softmax to get probabilities and find the top prediction
        probabilities = torch.nn.functional.softmax(output[0], dim=0)
        top_prob, top_catid = torch.topk(probabilities, 1)

        # Map the predicted class ID to class name
        class_name = class_names[top_catid.item()]

        return f"{class_name}, {top_prob.item()*100:.2f}%"
    except Exception as e:
        # Handle any unexpected errors
        raise ValueError("An error occurred during recognition: " + str(e))


def recognize_with_faster_rcnn(img, confidence_threshold):
    """
    Recognizes objects in an image using Faster R-CNN and then classifies each detected object using a VGG16 model.

    Args:
        img (PIL.Image.Image): The input image to be processed.
        confidence_threshold (float): The minimum confidence score for a detection to be considered.

    Returns:
        tuple: A tuple containing:
            - str: The recognition results for all detected objects.
            - ContentFile: An image file with bounding boxes and recognition results drawn on it.

    Raises:
        ValueError: If an error occurs during image processing or model inference.
    """
    try:
        # Convert image to tensor and add batch dimension
        img_tensor = TF.to_tensor(img).unsqueeze(0)

        # Perform inference without tracking gradients
        with torch.no_grad():
            predictions = faster_rcnn(img_tensor)

        # Extract bounding boxes and scores from predictions
        boxes = predictions[0]['boxes']
        scores = predictions[0]['scores']

        # Initialize plot
        fig, ax = plt.subplots()
        ax.imshow(img)

        # Hide axes
        ax.axis('off')

        recognition_results = []

        # Iterate over detected objects
        for box, score in zip(boxes, scores):
            if score > confidence_threshold:  # Use confidence threshold
                box = box.tolist()
                cropped_img = img.crop(box)
                recognition_result = recognize_with_vgg16(cropped_img)
                recognition_results.append(recognition_result)

                # Draw bounding box and label on the image
                rect = patches.Rectangle(
                    (box[0], box[1]),
                    box[2] - box[0],
                    box[3] - box[1],
                    linewidth=1,
                    edgecolor='r',
                    facecolor='none'
                )
                ax.add_patch(rect)
                ax.text(
                    box[0],
                    box[1],
                    recognition_result,
                    color='k',
                    fontsize=12,
                    verticalalignment='top',
                    bbox=dict(facecolor='yellow', edgecolor='red', boxstyle='round,pad=0.2')
                )

        # Save the annotated image to a buffer
        buf = io.BytesIO()
        plt.savefig(buf, format='png', bbox_inches='tight')
        buf.seek(0)
        plt.close(fig)

        return "\n".join(recognition_results), ContentFile(buf.getvalue(), name='annotated_image.png')

    except Exception as e:
        # Handle any unexpected errors
        raise ValueError("An error occurred during object detection and recognition: " + str(e))


def recognize_with_mask_rcnn(img, confidence_threshold):
    """
    Recognizes objects in an image using Mask R-CNN, then classifies each detected object using a VGG16 model,
    and visualizes the segmentation masks with contours.

    Args:
        img (PIL.Image.Image): The input image to be processed.
        confidence_threshold (float): The minimum confidence score for a detection to be considered.

    Returns:
        tuple: A tuple containing:
            - str: The recognition results for all detected objects.
            - ContentFile: An image file with bounding boxes, segmentation masks, and recognition results drawn on it.

    Raises:
        ValueError: If an error occurs during image processing or model inference.
    """
    try:
        # Convert image to tensor and add batch dimension
        img_tensor = TF.to_tensor(img).unsqueeze(0)

        # Perform inference without tracking gradients
        with torch.no_grad():
            predictions = mask_rcnn(img_tensor)

        # Extract bounding boxes, masks, and scores from predictions
        boxes = predictions[0]['boxes']
        masks = predictions[0]['masks']
        scores = predictions[0]['scores']

        # Initialize plot
        fig, ax = plt.subplots()
        ax.imshow(img)

        # Hide axes
        ax.axis('off')

        recognition_results = []

        # Iterate over detected objects
        for box, mask, score in zip(boxes, masks, scores):
            if score > confidence_threshold:  # Use confidence threshold
                box = box.tolist()
                mask = mask[0].mul(255).byte().cpu().numpy()
                mask = np.array(mask, dtype=np.uint8)

                # Find contours of the mask
                contours = measure.find_contours(mask, 0.5)

                # Plot contours
                for contour in contours:
                    contour = np.fliplr(contour)  # Flip coordinates for display
                    ax.plot(contour[:, 0], contour[:, 1], linewidth=2, color='r')

                # Crop the image to the bounding box
                cropped_img = img.crop(box).convert('RGB')
                recognition_result = recognize_with_vgg16(cropped_img)
                recognition_results.append(recognition_result)

                # Draw bounding box and label on the image
                ax.text(
                    box[0],
                    box[1],
                    recognition_result,
                    color='k',
                    fontsize=12,
                    verticalalignment='top',
                    bbox=dict(facecolor='yellow', edgecolor='red', boxstyle='round,pad=0.2')
                )

        # Save the annotated image to a buffer
        buf = io.BytesIO()
        plt.savefig(buf, format='png', bbox_inches='tight')
        buf.seek(0)
        plt.close(fig)

        return "\n".join(recognition_results), ContentFile(buf.getvalue(), name='annotated_image.png')

    except Exception as e:
        # Handle any unexpected errors
        raise ValueError("An error occurred during object detection, segmentation, and recognition: " + str(e))


file_id = '17v6ng5QSMOShyzJeRblkTNpU4H7mzAb6'
model_name = 'vgg16_cifar10.pth'

# Load VGG16 model without pretraining
vgg16 = torch.hub.load('pytorch/vision:v0.10.0', 'vgg16', weights=None)
vgg16.classifier[6] = torch.nn.Linear(vgg16.classifier[6].in_features, 10)

try:
    # Set download_if_exists=True to force re-download of the model
    vgg16.load_state_dict(load_model_from_google_drive(file_id, model_name, download_if_exists=False))
except ValueError as e:
    print(f"Error loading model: {e}")
vgg16.eval()

# Load Faster R-CNN with pre-trained COCO_V1 weights
faster_rcnn = models.detection.fasterrcnn_resnet50_fpn(weights=models.detection.FasterRCNN_ResNet50_FPN_Weights.COCO_V1)
faster_rcnn.eval()

# Load Mask R-CNN with pre-trained COCO_V1 weights
mask_rcnn = models.detection.maskrcnn_resnet50_fpn(weights=models.detection.MaskRCNN_ResNet50_FPN_Weights.COCO_V1)
mask_rcnn.eval()

# Transformations for VGG16
transform = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])
