# Cognition Creators - Image Classification Web Service
- [Читати українською](README_uk.md)

## Project Description

Cognition Creators is a multifunctional web service that utilizes modern AI technologies for image classification and user interaction. The core of the project is based on convolutional neural networks (CNN), which allow images to be classified based on trained models. The service provides users with the ability to upload images, train models, receive highly accurate classification results, and interact with the service through additional features.

The project also includes an interactive chat, built on GPT-4, that allows users to get answers to their questions and engage in conversations with artificial intelligence. For user authentication, an innovative solution using Face ID has been implemented, ensuring secure access to the service. Additionally, users can play an interactive game that demonstrates the capabilities of neural networks in real-time.

The service is intended for researchers, developers, and AI enthusiasts, as well as any user who wants to explore the possibilities of machine learning and AI in a convenient and accessible web interface.

## Key Features

- **Image Uploading:** Users can upload images for classification.
- **Model Training:** The CNN model is trained based on the CIFAR-10 dataset.
- **Image Verification:** The model classifies images and displays the results with high accuracy.
- **Containerization:** The project is fully containerized with Docker, providing easy deployment.
- **Authentication:** Users can register, log in, and log out of the system.
- **Face ID:** Implemented functionality for registration and authentication using Face ID based on camera images.
- **Game:** Interactive game using a neural network.
- **GPT-4 Chat:** Interactive chat using GPT-4 AI, available only to authorized users.

## Technologies Used

- **Python:** The main programming language for logic and neural network implementation.
- **Django:** Web framework for building the backend and managing the web interface.
- **Convolutional Neural Networks (CNN):** Used for image classification.
- **PostgreSQL:** Database management system for storing classification results and user data.
- **Docker:** Tool for containerizing the application.
- **GitHub:** Platform for collaboration and version control.
- **Agile:** Project development methodology.
- **HTML/CSS/JavaScript:** For building the frontend, including interactive elements like modals and the language switcher.
- **Bootstrap:** Framework for creating responsive web design.
- **face_recognition:** A library for recognizing faces and implementing Face ID based on camera images.
- **Pillow (PIL):** Python library for image processing, including resizing and formatting.
- **GPT-4 API:** Used to implement the interactive chat with artificial intelligence.
- **Koyeb:** Platform for hosting and deploying the application.

## Installation instructions

1. Clone the repository:
    ```bash
    git clone https://github.com/IT-School-GoIT/final_data_science_goit.git
    cd final_data_science_goit

2. Create and activate the virtual environment:
    ```bash
    python3 -m venv env
    source env/bin/activate # On Windows, use the `env\Scripts\activate` command

3. Set the dependency:
    ```bash
    pip install -r requirements.txt

4. Configure the database:
    Create an .env file with your data
    Edit the root/settings.py file (if necessary) to configure the PostgreSQL connection.

5. Migration databases:
    ```bash
    python manage.py migrate

6. Start the development server:
    ```bash
    python manage.py runserver
