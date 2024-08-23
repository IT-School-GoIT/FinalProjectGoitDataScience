
import io
import os
import gdown
import torch
from django.shortcuts import render, redirect
from torchvision import models, transforms
from PIL import Image
import torchvision.transforms.functional as TF
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from django.core.files.base import ContentFile
import numpy as np
from skimage import measure
from .forms import UploadImageForm
from .models import UploadedImage
from .classes import class_names


def load_model_from_google_drive(file_id, model_name, download_if_exists=False):
    # Створення папки, якщо вона не існує
    model_dir = 'media/models'
    if not os.path.exists(model_dir):
        os.makedirs(model_dir)

    model_path = os.path.join(model_dir, model_name)

    # Перевірка наявності моделі
    if os.path.exists(model_path) and not download_if_exists:
        print(f"Model already exists at {model_path}. Loading from disk.")
    else:
        print(f"Downloading model to {model_path}...")
        gdown.download(id=file_id, output=model_path, quiet=False)

    # Завантаження моделі
    model = torch.load(model_path, map_location=torch.device('cpu'))
    return model


def result(request, image_id):
    uploaded_image = UploadedImage.objects.get(id=image_id)
    return render(request, 'recognition/recognition.html', {'uploaded_image': uploaded_image})


def index(request):
    if request.method == 'POST':
        form = UploadImageForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.cleaned_data['image']
            recognition_type = form.cleaned_data['recognition_type']
            confidence_threshold = form.cleaned_data['confidence_threshold']
            img = Image.open(image)

            if recognition_type == 'vgg16':
                result = recognize_with_vgg16(img)
                annotated_image = None
            elif recognition_type == 'faster_rcnn':
                result, annotated_image = recognize_with_faster_rcnn(img, confidence_threshold)
            elif recognition_type == 'mask_rcnn':
                result, annotated_image = recognize_with_mask_rcnn(img, confidence_threshold)

            uploaded_image = form.save(commit=False)
            uploaded_image.result = result
            if annotated_image:
                uploaded_image.annotated_image.save(annotated_image.name, annotated_image)
            uploaded_image.save()

            return redirect('recognition:result', uploaded_image.id)

    else:
        form = UploadImageForm(initial={'recognition_type': 'vgg16'})
    return render(request, 'recognition/cognition.html', {'form': form})


# def recognize_with_vgg16(img):
#     img = img.convert('RGB')  # Переконайтеся, що зображення має 3 канали (RGB)
#     img_tensor = transform(img).unsqueeze(0)
#     with torch.no_grad():
#         output = vgg16(img_tensor)
#     probabilities = torch.nn.functional.softmax(output[0], dim=0)
#     top_prob, top_catid = torch.topk(probabilities, 1)
#     class_name = class_names[top_catid.item()]
#     return f"{class_name}, {top_prob.item()*100:.2f}%"
def recognize_with_vgg16(img):
    img = img.convert('RGB')  # Переконайтеся, що зображення має 3 канали (RGB)
    img = img.resize((32, 32))  # Масштабування до розміру, який використовувався під час тренування
    img_tensor = transform(img).unsqueeze(0)
    with torch.no_grad():
        output = vgg16(img_tensor)
    probabilities = torch.nn.functional.softmax(output[0], dim=0)
    top_prob, top_catid = torch.topk(probabilities, 1)
    class_name = class_names[top_catid.item()]
    return f"{class_name}, {top_prob.item()*100:.2f}%"




def recognize_with_faster_rcnn(img, confidence_threshold):
    img_tensor = TF.to_tensor(img).unsqueeze(0)
    with torch.no_grad():
        predictions = faster_rcnn(img_tensor)
    boxes = predictions[0]['boxes']
    scores = predictions[0]['scores']

    fig, ax = plt.subplots()
    ax.imshow(img)

    recognition_results = []

    for box, score in zip(boxes, scores):
        if score > confidence_threshold:  # використання порогового значення
            box = box.tolist()
            cropped_img = img.crop(box)
            recognition_result = recognize_with_vgg16(cropped_img)
            recognition_results.append(recognition_result)

            rect = patches.Rectangle((box[0], box[1]), box[2] - box[0], box[3] - box[1], linewidth=1, edgecolor='r',
                                     facecolor='none')
            ax.add_patch(rect)
            ax.text(box[0], box[1], recognition_result, color='k', fontsize=12, verticalalignment='top',
                    bbox=dict(facecolor='yellow', edgecolor='red', boxstyle='round,pad=0.2'))

    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight')
    buf.seek(0)
    plt.close(fig)

    return "\n".join(recognition_results), ContentFile(buf.getvalue(), name='annotated_image.png')

# def recognize_with_faster_rcnn(img, confidence_threshold):
#     img_tensor = TF.to_tensor(img)
#     with torch.no_grad():
#         predictions = faster_rcnn([img_tensor])  # Передаємо список тензорів
#     boxes = predictions[0]['boxes']
#     scores = predictions[0]['scores']
#
#     fig, ax = plt.subplots()
#     ax.imshow(img)
#
#     recognition_results = []
#
#     for box, score in zip(boxes, scores):
#         if score > confidence_threshold:
#             box = box.tolist()
#             cropped_img = img.crop(box).convert('RGB')  # Конвертація в RGB
#             recognition_result = recognize_with_vgg16(cropped_img)
#             recognition_results.append(recognition_result)
#
#             rect = patches.Rectangle((box[0], box[1]),
#                                      box[2] - box[0],
#                                      box[3] - box[1],
#                                      linewidth=1, edgecolor='r',
#                                      facecolor='none')
#             ax.add_patch(rect)
#             ax.text(box[0], box[1], recognition_result, color='k', fontsize=12,
#                     verticalalignment='top',
#                     bbox=dict(facecolor='yellow', edgecolor='red', boxstyle='round,pad=0.2'))
#
#     buf = io.BytesIO()
#     plt.savefig(buf, format='png', bbox_inches='tight')
#     buf.seek(0)
#     plt.close(fig)
#
#     return "\n".join(recognition_results), ContentFile(buf.getvalue(), name='annotated_image.png')



def recognize_with_mask_rcnn(img, confidence_threshold):
    img_tensor = TF.to_tensor(img).unsqueeze(0)
    with torch.no_grad():
        predictions = mask_rcnn(img_tensor)
    boxes = predictions[0]['boxes']
    masks = predictions[0]['masks']
    scores = predictions[0]['scores']

    fig, ax = plt.subplots()
    ax.imshow(img)

    recognition_results = []

    for box, mask, score in zip(boxes, masks, scores):
        if score > confidence_threshold:  # використання порогового значення
            box = box.tolist()
            mask = mask[0].mul(255).byte().cpu().numpy()
            mask = np.array(mask, dtype=np.uint8)

            # Виділення контурів маски
            contours = measure.find_contours(mask, 0.5)

            for contour in contours:
                contour = np.fliplr(contour)  # зміна координат для відображення
                ax.plot(contour[:, 0], contour[:, 1], linewidth=2, color='r')

            cropped_img = img.crop(box).convert('RGB')  # Переконайтеся, що зображення має 3 канали (RGB)
            recognition_result = recognize_with_vgg16(cropped_img)
            recognition_results.append(recognition_result)

            ax.text(box[0], box[1], recognition_result, color='k', fontsize=12, verticalalignment='top',
                    bbox=dict(facecolor='yellow', edgecolor='red', boxstyle='round,pad=0.2'))

    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight')
    buf.seek(0)
    plt.close(fig)

    return "\n".join(recognition_results), ContentFile(buf.getvalue(), name='annotated_image.png')


# def recognize_with_mask_rcnn(img, confidence_threshold):
#     img_tensor = TF.to_tensor(img)
#     with torch.no_grad():
#         predictions = mask_rcnn([img_tensor])  # Передаємо список тензорів
#     boxes = predictions[0]['boxes']
#     masks = predictions[0]['masks']
#     scores = predictions[0]['scores']
#
#     fig, ax = plt.subplots()
#     ax.imshow(img)
#
#     recognition_results = []
#
#     for box, mask, score in zip(boxes, masks, scores):
#         if score > confidence_threshold:
#             box = box.tolist()
#             mask = mask[0].mul(255).byte().cpu().numpy()
#             mask = np.array(mask, dtype=np.uint8)
#
#             contours = measure.find_contours(mask, 0.5)
#
#             for contour in contours:
#                 contour = np.fliplr(contour)
#                 ax.plot(contour[:, 0], contour[:, 1], linewidth=2, color='r')
#
#             cropped_img = img.crop(box).convert('RGB')  # Конвертація в RGB
#             recognition_result = recognize_with_vgg16(cropped_img)
#             recognition_results.append(recognition_result)
#
#             ax.text(box[0], box[1], recognition_result, color='k', fontsize=12,
#                     verticalalignment='top',
#                     bbox=dict(facecolor='yellow', edgecolor='red', boxstyle='round,pad=0.2'))
#
#     buf = io.BytesIO()
#     plt.savefig(buf, format='png', bbox_inches='tight')
#     buf.seek(0)
#     plt.close(fig)
#
#     return "\n".join(recognition_results), ContentFile(buf.getvalue(), name='annotated_image.png')






file_id = '17v6ng5QSMOShyzJeRblkTNpU4H7mzAb6'
model_name = 'vgg16_cifar10.pth'

# Завантаження моделей
vgg16 = torch.hub.load('pytorch/vision:v0.10.0', 'vgg16', pretrained=False)
vgg16.classifier[6] = torch.nn.Linear(vgg16.classifier[6].in_features, 10)

try:
    # Встановіть download_if_exists=True, щоб примусово завантажити модель заново
    vgg16.load_state_dict(load_model_from_google_drive(file_id, model_name, download_if_exists=False))
except ValueError as e:
    print(f"Error loading model: {e}")
vgg16.eval()

faster_rcnn = models.detection.fasterrcnn_resnet50_fpn(pretrained=True)
faster_rcnn.eval()

mask_rcnn = models.detection.maskrcnn_resnet50_fpn(pretrained=True)
mask_rcnn.eval()

# Трансформації для VGG16
transform = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])

