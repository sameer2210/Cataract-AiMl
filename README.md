Project Overview — SpandaVidyaAi Cataract Detection System

Project Type:

AI-Powered Eye Cataract Detection System

Core Goal:

Detect cataract severity from eye/lens images using Deep Learning

Tech Domain:

Computer Vision
Medical AI
Deep Learning
Healthcare Automation
Full System Architecture
React Native Mobile App
↓
NestJS Backend API
↓
FastAPI AI Microservice
↓
PyTorch EfficientNet-B3 Model
↓
PostgreSQL Database
↓
Cloud Storage (Optional)
Main Components

1. React Native Mobile App

Purpose:

User image upload
Camera capture
Patient history
Prediction results
Reports

Features:

Camera integration
Gallery upload
Prediction screen
History dashboard
Authentication
Multi-language support
Offline caching

Recommended Libraries:

react-native-image-picker
react-query
axios
redux-toolkit
react-navigation 2. NestJS Backend

Purpose:

Authentication
User management
API gateway
AI service communication
Database management

Responsibilities:

JWT auth
Role management
Upload validation
Rate limiting
API logging
Prediction storage

Recommended Modules:

Auth Module
Prediction Module
Patient Module
Admin Module
Analytics Module 3. FastAPI AI Service

Purpose:

Dedicated ML inference server

Responsibilities:

Image preprocessing
Model inference
Prediction generation
Confidence scoring

Why FastAPI:

extremely fast
async support
easy ML integration
OpenAPI docs
production-friendly
ML Model Details
Model Architecture
EfficientNet-B3

Framework:

PyTorch

Problem Type:

Multi-Class Image Classification

Number of Classes:

num_classes = 4

Likely Categories:

Normal
Mild Cataract
Moderate Cataract
Severe Cataract
Why EfficientNet-B3

Advantages:

high accuracy
lower computation
medical imaging friendly
optimized scaling
better feature extraction

Compared To:

ResNet
VGG
MobileNet

EfficientNet generally:

better accuracy-to-performance ratio
ML Pipeline
Step 1 — Image Upload

Input:

Eye/Lens Image
Step 2 — Lens Detection

Function:

center_black_lens_hough_from_bgr()

Technique:

Hough Circle Transform

Purpose:

detect eye lens
isolate circular region
remove unnecessary background
Step 3 — Lens Centering

Purpose:

normalize positioning
improve inference consistency
Step 4 — CLAHE Enhancement

Function:

preprocess_lens_with_mask()

Technique:

Contrast Limited Adaptive Histogram Equalization

Purpose:

improve contrast
enhance cataract visibility
highlight cloudy regions

Medical imaging me widely used.

Step 5 — Image Transformations
Resize
CenterCrop
Normalize
ToTensor

Purpose:

convert image into model-ready tensor
Step 6 — Model Inference
outputs = model(tensor)

Purpose:

predict cataract category
Step 7 — Softmax Confidence
torch.softmax()

Purpose:

probability scores

Example:

{
"prediction": "Moderate Cataract",
"confidence": 0.94
}
Existing Features In Your AI

Already Present:

Lens Detection
Automatic eye region extraction
Image Centering
Better alignment normalization
CLAHE Enhancement
Medical contrast enhancement
EfficientNet-B3 Inference
High-quality CNN prediction
Confidence Scoring
Prediction certainty
Missing Features

Currently Missing:

Grad-CAM Visualization

Purpose:

Show why AI predicted cataract

Very important in medical AI.

Dataset Metrics Dashboard

Need:

accuracy
recall
precision
F1-score
Multi-Image Validation

Use multiple eye angles.

Image Quality Validation

Reject:

blurry images
dark images
non-eye uploads
AI Explainability

Medical systems need transparency.

FastAPI Production Plan
PHASE 1 — Local Development

Goal:

Stable local inference

Tasks:

setup FastAPI
test image uploads
verify predictions
validate preprocessing

Commands:

uvicorn app.main:app --reload
PHASE 2 — Hugging Face Deployment

Goal:

Public testing environment

Why:

easy deployment
free hosting
API testing
quick iteration

Deploy:

FastAPI wrapper
model weights
requirements.txt
PHASE 3 — NestJS Integration

Flow:

React Native
↓
NestJS
↓
FastAPI ML Service

NestJS responsibilities:

auth
uploads
database
prediction storage

FastAPI responsibilities:

AI only
PHASE 4 — Database Design
PostgreSQL Tables
Users
users
Patients
patients
Predictions
predictions

Schema example:

CREATE TABLE predictions (
id UUID PRIMARY KEY,
patient_id UUID,
image_url TEXT,
prediction VARCHAR(100),
confidence FLOAT,
created_at TIMESTAMP DEFAULT NOW()
);

PHASE 5 — Production Backend Architecture
Final Architecture
React Native App
↓
NestJS API Gateway
↓
FastAPI AI Service
↓
PyTorch EfficientNet-B3
↓
PostgreSQL
↓
Cloud Storage (S3/Cloudinary)
Why Microservice Architecture

AI service alag rakhna best practice hai.

Benefits:

scalable
GPU isolation
easier deployment
independent crashes
separate optimization
API Design
FastAPI Endpoints
Health Check
GET /

Response:

{
"message": "Cataract AI Running"
}
Prediction Endpoint
POST /predict

Request:

image file

Response:

{
"prediction": "Moderate Cataract",
"confidence": 0.947
}
Recommended Response Format

Production response should be richer.

Example:

{
"success": true,
"prediction": {
"class": "Moderate Cataract",
"confidence": 94.7
},
"metadata": {
"model": "EfficientNet-B3",
"processing_time_ms": 421
}
}
NestJS Production Flow
Upload Flow
Mobile Upload
↓
NestJS Validation
↓
Cloud Storage Upload
↓
FastAPI Inference Request
↓
Store Prediction
↓
Return Result
Recommended NestJS Modules
src/modules/
│
├── auth/
├── ai/
├── patient/
├── prediction/
├── admin/
├── analytics/
└── uploads/
Recommended Database Tables
users
CREATE TABLE users (
id UUID PRIMARY KEY,
name TEXT,
email TEXT UNIQUE,
password TEXT,
role TEXT,
created_at TIMESTAMP DEFAULT NOW()
);
patients
CREATE TABLE patients (
id UUID PRIMARY KEY,
user_id UUID,
full_name TEXT,
age INTEGER,
gender TEXT,
created_at TIMESTAMP DEFAULT NOW()
);
predictions
CREATE TABLE predictions (
id UUID PRIMARY KEY,
patient_id UUID,
image_url TEXT,
prediction TEXT,
confidence FLOAT,
created_at TIMESTAMP DEFAULT NOW()
);
AI Model Technical Details
Framework
PyTorch
CNN Backbone
EfficientNet-B3
Image Processing Stack

Libraries:

OpenCV
PIL
torchvision
numpy
Preprocessing Pipeline
Lens Detection

Technique:

Hough Circle Detection

Purpose:

isolate eye lens
remove noise
Contrast Enhancement

Technique:

CLAHE

Purpose:

enhance cataract patterns
improve visibility
Tensor Conversion
transforms.Compose()

Purpose:

convert image into model tensor
Inference
model(tensor)

Purpose:

classification prediction
Confidence Calculation
torch.softmax()

Purpose:

probability estimation
Existing Strong Points In Your Model
Advanced Preprocessing

Most beginner projects skip:

CLAHE
lens centering
circular masking

Tumhare project me ye already hai.

EfficientNet-B3

Good choice because:

high accuracy
efficient inference
optimized CNN scaling
Proper Medical Image Enhancement

CLAHE:

medical-grade preprocessing technique

used in:

radiology
retinal imaging
MRI enhancement
Current Weaknesses
No Explainability

Missing:

Grad-CAM

Important for:

doctor trust
medical transparency
No Dataset Metrics

Need:

confusion matrix
recall
sensitivity
specificity
No Quality Validation

Should reject:

blurry images
low-light images
non-eye images
Recommended Future Features
AI Heatmap

Show:

where cataract detected
PDF Report Generation

Generate:

prediction
confidence
timestamp
patient details
Doctor Dashboard

Features:

patient history
image comparisons
analytics
Multi-Language Support

Useful for:

rural healthcare
clinics
government usage
Offline Inference

Future:

ONNX / TensorFlow Lite

for mobile inference.

Performance Optimization Plan
Current
PyTorch inference

Good for:

testing
MVP
initial users
Future Optimization
TorchScript
torch.jit.trace()
ONNX Export
torch.onnx.export()

Benefits:

faster inference
smaller memory
TensorRT

For:

GPU optimization
Security Plan
NestJS Side

Add:

JWT auth
file validation
rate limiting
upload size limits
FastAPI Side

Add:

MIME validation
temp cleanup
inference timeout
exception handling
Deployment Plan
Stage 1 — Local Testing
uvicorn app.main:app --reload

Goal:

verify predictions
validate preprocessing
Stage 2 — Hugging Face

Purpose:

public testing
API validation
rapid iteration

Good for:

MVP
demos
testing
Stage 3 — Docker

Add:

FROM python:3.11

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8002"]
Stage 4 — VPS/AWS

Deploy:

FastAPI container
PostgreSQL
NestJS backend

Options:

AWS EC2
DigitalOcean
Railway
Render
Stage 5 — GPU Deployment

For high traffic:

NVIDIA GPU
CUDA containers
autoscaling
Hugging Face Production Notes

Good for:

testing
demos
MVP

Not ideal for:

large-scale production
guaranteed uptime
heavy traffic
Recommended Production Stack
Mobile
React Native
Backend
NestJS
AI Service
FastAPI + PyTorch
Database
PostgreSQL
Deployment
Docker + VPS
Estimated System Capability

Current setup likely supports:

10–50 concurrent requests

on decent VPS CPU.

With optimization:

hundreds of requests
GPU acceleration
queue workers

possible.

Final Technical Summary
Current State

You already have:

trained AI model
preprocessing pipeline
inference logic
scalable architecture direction

Most difficult part:

model training

already completed.

Current Missing Parts

Need:

FastAPI production hardening
monitoring
analytics
explainability
security
cloud deployment
Project Classification

This is NOT beginner-level anymore.

This qualifies as:

Intermediate-to-Advanced Medical AI System

because:

custom preprocessing
EfficientNet-B3
microservice architecture
medical image enhancement
FastAPI integration
scalable deployment path

already exist.
