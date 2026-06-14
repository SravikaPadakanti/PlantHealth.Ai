# 🌿 PlantHealth.AI — Plant Disease Detection System

> **Neural Phytopathology Scanner for Smart Farms**  
> Upload a crop leaf image and get instant disease diagnosis with treatment recommendations.

---

## 📌 Project Overview

PlantHealth.AI is a deep learning-powered web application that detects whether a plant leaf is **healthy or diseased**. It classifies crop leaf images into **38 disease categories** across multiple plant species and provides scientific pathology details along with treatment and prevention protocols.

### What it does:
- Upload a leaf image (JPG, JPEG, PNG)
- CNN model analyzes the image in under 1.5 seconds
- Returns: disease name, crop type, scientific cause, symptoms, and remedies
- Displays training accuracy curves and dataset statistics

---

## 🖥️ Demo Screenshots

| Feature | Description |
|---|---|
| Home Hub | Landing page with project overview and stats |
| Leaf Diagnosis | Upload leaf and get instant prediction |
| Dataset & Curves | Training/validation accuracy and loss graphs |
| Disease Report | Full pathology report with treatment protocol |

---

## 📊 Model Performance

| Metric | Value |
|---|---|
| Training Accuracy | ~97.9% |
| Classes | 38 (disease + healthy) |
| Prediction Speed | < 1.5 seconds |
| Training Set | 70,295 images |
| Validation Set | 17,572 images |
| Test Set | 33 images |

---

## 🗂️ Project Structure

```
Plant_Disease_Prediction-project/
│
├── train/                          # Training dataset (70,295 images, 38 classes)
├── valid/                          # Validation dataset (17,572 images)
├── New Plant Diseases Dataset(Augmented)/  # Full augmented dataset
│
├── Train_plant_disease.ipynb       # Model training notebook (CNN architecture)
├── Test_plant_disease.ipynb        # Model evaluation and testing notebook
│
├── trained_plant_disease_model.keras  # Saved trained model (generated after training)
├── training_hist.json              # Training history (accuracy & loss per epoch)
│
├── main.py                         # Flask web app (original)
├── train.py                        # Training script
├── test.py                         # Testing script
├── remedies.py                     # Disease-to-remedy mapping database
│
├── home_page.jpeg                  # App home page image
├── requirement.txt                 # Python dependencies
└── README.md                       # This file
```

---

## 🧠 Model Architecture

The CNN model is built using **TensorFlow / Keras** with the following design:

- **10-Layer Convolutional Network**
- Conv2D blocks with Batch Normalization and Dropout layers
- Detects color anomalies, vein patterns, and mold spotting
- Input image size: **128 × 128 pixels (RGB)**
- Output: Softmax over **38 disease classes**

### Deep Learning Pipeline:
```
01. Image Capture     →  High-res crop leaf uploaded via browser
02. Preprocessing     →  Resized to 128×128 and normalized
03. Inference Pass    →  10-layer CNN extracts color/texture descriptors
04. Remedy Synthesis  →  Disease mapping database yields treatment protocols
```

---

## 🌱 Supported Crops & Diseases (38 Classes)

Includes diseases for: **Apple, Blueberry, Cherry, Corn, Grape, Orange, Peach, Pepper, Potato, Raspberry, Soybean, Squash, Strawberry, Tomato**

Example classes:
- Apple — Apple Scab, Black Rot, Cedar Apple Rust, Healthy
- Tomato — Leaf Mold, Late Blight, Early Blight, Mosaic Virus, Healthy
- Corn — Gray Leaf Spot, Common Rust, Northern Leaf Blight, Healthy
- Potato — Early Blight, Late Blight, Healthy
- *(and many more...)*

---

## ⚙️ Installation & Setup

### Prerequisites
- Python **3.10** (required — TensorFlow 2.10 does not support Python 3.11+)
- Git
- VS Code (recommended) or Jupyter Notebook

### Step 1 — Clone or download the project
```bash
git clone https://github.com/animesh1012/machineLearning
cd Plant_Disease_Prediction
```

### Step 2 — Create a virtual environment with Python 3.10
```bash
py -3.10 -m venv venv310
venv310\Scripts\activate        # Windows
# source venv310/bin/activate   # Mac/Linux
```

### Step 3 — Install dependencies
```bash
pip install -r requirement.txt
```

### Step 4 — Download the dataset
Download the **New Plant Diseases Dataset** from Kaggle:
👉 https://www.kaggle.com/datasets/vipoooool/new-plant-diseases-dataset

Extract and place the `train/` and `valid/` folders in the project root.

---

## 🚀 How to Run

### Step 1 — Train the Model
Open and run all cells in:
```
Train_plant_disease.ipynb
```
This will generate: `trained_plant_disease_model.keras`

> Training time: ~30 min (GPU) to ~2-5 hours (CPU only)

### Step 2 — Test the Model
Open and run:
```
Test_plant_disease.ipynb
```
Evaluates accuracy on the validation/test set.

### Step 3 — Launch the Web App
```bash
python main.py
```
Open your browser at: **http://127.0.0.1:5000**

---

## 📦 Dependencies

```
tensorflow==2.10.0
scikit-learn==1.3.0
numpy==1.24.3
matplotlib==3.7.2
seaborn==0.13.0
pandas==2.1.0
streamlit
librosa==0.10.1
flask
pillow
```

> ⚠️ **Important:** Use Python 3.10. TensorFlow 2.10.0 is not compatible with Python 3.11 or higher.

---

## 📈 Training Results

The model was trained for ~10 epochs and achieved:

- Training accuracy steadily increased from ~60% → ~98%
- Validation accuracy started high (~85%) and converged to ~96%
- Cross-entropy loss dropped from ~1.35 to near 0 (training) and ~0.1 (validation)

The learning curves confirm the model generalizes well with no significant overfitting.

---

## 🔬 Disease Diagnosis Output

For each uploaded leaf image, the app returns:

| Field | Example |
|---|---|
| Disease Name | Tomato — Leaf Mold |
| Status | 🔴 DISEASED / 🟢 HEALTHY |
| Crop Category | Tomato |
| Scientific Cause | Fungus (Passalora fulva) |
| Pathology & Symptoms | Yellow spots on upper surface, olive-green mold on undersides |
| Treatment Protocol | Grow resistant cultivars, improve ventilation, ensure leaves dry |

---

## 🤝 Acknowledgements

- Dataset: [PlantVillage Dataset](https://www.kaggle.com/datasets/vipoooool/new-plant-diseases-dataset) (87K images, 38 classes)
- Framework: TensorFlow / Keras
- Web Framework: Flask / Streamlit

---

## 📄 License

This project is for educational and research purposes. Dataset sourced from Kaggle under its respective license.
