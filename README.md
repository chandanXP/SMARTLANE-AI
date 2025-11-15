---
title: SourceCode
emoji: 👀
colorFrom: red
colorTo: red
sdk: streamlit
app_port: 8501
tags:
- streamlit
pinned: false
short_description: Paranox 2.0 Hackathon
license: mit
---

# 🚦 SmartLane AI – Intelligent Traffic & Emergency Vehicle Management System

**📅 Date:** November 16, 2025  
**🏁 Event:** TechXNinjas – PARANOX 2.0 (3-Month National Level Innovation + 24-Hour Build Hackathon)  
**👥 Team:** Team SourceCode  
**🌍 Live Demo:** https://paranox-sourcecode.hf.space  
**🧠 CNN Model Training Notebook:** https://colab.research.google.com/drive/1v-TD755AdnonZuIX0nXLbM2DvF281xiu?usp=sharing

---

## 🔥 About SmartLane AI

SmartLane AI is an **AI-powered Traffic Intelligence Platform** designed to optimize 4-way traffic intersections using:

🚘 **YOLOv8 Object Detection**  
🚑 **Multimodal Ambulance/Emergency Vehicle Detection**  
🎯 **CNN Deep Learning Classification**  
📊 **Real-Time Traffic Analytics & Signal Time Optimization**

It automatically prioritizes **emergency vehicles** (Ambulance) by extending green light duration and clearing the lane using a **multi-method decision model**:

| Detection Layers (Priority Order) |
|------|
| 1️⃣ Manual Override Control |
| 2️⃣ YOLO + Color Signature Analysis |
| 3️⃣ CNN Ambulance Classifier |
| 4️⃣ Red/White Pattern Recognition |
| 5️⃣ Emergency Text/OCR Pattern Detection |

---

## 🧪 Live Demo & Results

🔗 **Live Web App:** https://paranox-sourcecode.hf.space  
📌 Upload **four road images** (North, East, South, West) → SmartLane AI detects vehicle density and prioritizes emergency lanes.

---

## 🎯 Key Features

| Feature | Description |
|--------|-------------|
| 🚗 Vehicle Detection | YOLOv8 counts Cars, Buses, Trucks, Motorcycles |
| 🚑 Emergency Recognition | CNN + YOLO + Color + Text Pattern Fusion |
| 🚦 Adaptive Traffic Signal Control | AI-driven timing & clearance logic |
| 🟢 Emergency Priority Mode | Automatically extends green light (35s) |
| 📊 Traffic Intelligence Dashboard | Vehicle matrix, charts, priority rankings |
| 📥 Export Reports | Download `.txt` traffic analysis summary |

---

## 🛠 Technology Stack

| Category | Tools |
|--------|-------|
| **AI / CV Models** | YOLOv8, TensorFlow CNN |
| **Framework** | Streamlit |
| **Language** | Python |
| **Visualization** | Matplotlib, Pandas |
| **Image Processing** | OpenCV, PIL |

---

## 📦 Project Structure

```

SMARTLANE-AI/
│
├── app.py                      # Main Streamlit Application
├── ambulance_cnn_final.keras   # Trained CNN Model
├── model/                      # Additional model assets (optional)
│   └── classes.txt
├── README.md
└── requirements.txt

````

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the repository
```bash
git clone https://github.com/lovnishverma/SMARTLANE-AI.git
cd SMARTLANE-AI
````

### 2️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

### 3️⃣ Run SmartLane AI

```bash
streamlit run app.py
```

---

## 🧠 CNN Ambulance Classifier

The system includes a **custom-trained CNN** for Ambulance vs Non-Ambulance classification.

📌 Training Notebook (Google Colab):
➡ [https://colab.research.google.com/drive/1v-TD755AdnonZuIX0nXLbM2DvF281xiu?usp=sharing](https://colab.research.google.com/drive/1v-TD755AdnonZuIX0nXLbM2DvF281xiu?usp=sharing)

Model Summary:

* Input: 192×192 RGB Image
* Output: Softmax (Ambulance / Non-Ambulance)
* Accuracy: **≈ 99.2% on Validation**

---

## 🚦 AI Signal Timing Logic

| Condition           | Green Time          |
| ------------------- | ------------------- |
| Emergency Vehicle   | ⏱ 35 seconds        |
| Normal Traffic Base | ⏱ 5 seconds         |
| Extra Time          | ➕1 sec / 2 vehicles |
| Max Green           | ⏳ 25 seconds        |

---

## 📍 Hackathon Overview (PARANOX 2.0)

> **PARANOX 2.0** is a 3-month national-level innovation event + **24-hour build hackathon** where students **BUILD · PITCH · WIN** by converting their prototypes into real-world products. SmartLane AI was developed in this challenge under **TechXNinjas**.

---

## 👨‍💻 Team SourceCode

| Member                 | Role                           |
| ---------------------- | ------------------------------ |
| 👑 Lovnish Verma       | Lead Developer / ML Engineer   |
| 🧠 [Add Teammate Name] | Computer Vision & CNN Training |
| ⚡ [Add Teammate Name]  | UI/UX & Streamlit Integration  |
| 🛰 [Add Teammate Name] | Deployment & Optimization      |

> Want to join or collaborate? PRs are welcome!

---

## 🛡 License

This project is licensed under **MIT License**. You are free to modify and use with attribution.

---

## ⭐ Support the Project

If you find this useful, please star the repo:

👉 [https://github.com/lovnishverma/SMARTLANE-AI](https://github.com/lovnishverma/SMARTLANE-AI) 🌟

---

## 📞 Contact / Connect

For research or collaboration inquiries:

📧 Email: *[Add Your Contact Email]*
🌐 GitHub: [https://github.com/lovnishverma](https://github.com/lovnishverma)
🔗 LinkedIn: *[Insert Profile]*

---

### 🚦 SmartLane AI

**Transforming traffic. Saving lives. Intelligent cities start here.**



