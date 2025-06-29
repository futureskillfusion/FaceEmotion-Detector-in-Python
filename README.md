# 🎭 Emotion Detector

A Python-based emotion detection system with both **GUI application** and **REST API** for real-time emotion analysis from images and webcam feeds.

## 🚀 Features

- **🖥️ Desktop GUI**: Real-time webcam + image upload analysis
- **📡 REST API**: For mobile/web integration (Flutter, React, etc.)
- **🎯 Multi-face Detection**: Analyzes multiple faces simultaneously
- **🎨 7 Emotions**: Happy, sad, angry, surprise, fear, disgust, neutral
- **🔄 Real-time Processing**: Live webcam emotion detection

## 📦 Quick Setup

### 1. Install Dependencies
```bash
# Navigate to project folder
cd C:\Users\Hamza\MoodDetector

# Create & activate virtual environment
python -m venv .venv
.venv\Scripts\activate

# Install all packages
pip install -r requirements.txt
```

### 2. Run Applications

#### 🖥️ **Desktop GUI App**
```bash
python app.py
```
- Click "Open Camera" for live detection
- Click "Upload Image" for file analysis
- Press 'q' to exit camera mode

#### � **API Server**
```bash
python api.py
```
- API runs at: `http://localhost:5000`
- Ready for Flutter/mobile integration

## 🌐 API Usage

### Endpoints
- **Health Check**: `GET /`
- **Analyze Emotion**: `POST /api/analyze-emotion`

### Example Request
```bash
curl -X POST http://localhost:5000/api/analyze-emotion \
  -H "Content-Type: application/json" \
  -d '{"image": "base64_encoded_image_string"}'
```

### Response Format
```json
{
  "status": "success",
  "face_count": 1,
  "emotions": [{
    "dominant_emotion": "happy",
    "confidence": 0.94,
    "emotion_scores": {
      "happy": 0.94,
      "neutral": 0.03,
      "sad": 0.02,
      "angry": 0.01
    },
    "region": {"x": 100, "y": 50, "w": 150, "h": 150}
  }]
}
```

## 📱 Flutter Integration

### Network URLs
```dart
// Android Emulator
String apiUrl = "http://10.0.2.2:5000";

// Physical Device (same WiFi)
String apiUrl = "http://192.168.100.4:5000";

// Production (after cloud deployment)
String apiUrl = "https://your-app.herokuapp.com";
```

### Basic Flutter Code
```dart
// Convert image to base64 and send request
final response = await http.post(
  Uri.parse('$apiUrl/api/analyze-emotion'),
  headers: {'Content-Type': 'application/json'},
  body: jsonEncode({'image': base64Image}),
);

final result = jsonDecode(response.body);
print('Dominant emotion: ${result['emotions'][0]['dominant_emotion']}');
```

## � Dependencies

```txt
opencv-python>=4.5.5.64    # Image processing
deepface>=0.0.93           # Emotion detection
tensorflow>=2.19.0         # ML backend
tf-keras>=2.19.0          # Keras compatibility
Flask>=2.3.0              # API server
flask-cors>=4.0.0         # Cross-origin requests
```

## � Project Structure

```
MoodDetector/
├── app.py              # Desktop GUI application
├── api.py              # REST API server
├── test_api.py         # API testing script
├── requirements.txt    # Dependencies
├── README.md          # This file
└── .venv/             # Virtual environment
```

## ⚠️ Troubleshooting

| Issue | Solution |
|-------|----------|
| `No module named 'cv2'` | `pip install opencv-python` |
| `No module named 'deepface'` | `pip install deepface` |
| `No module named 'tf_keras'` | `pip install tf-keras` |
| Camera not working | Check permissions & close other camera apps |
| API connection error | Ensure API server is running on correct port |

## 🎯 Quick Commands

```bash
# Complete setup and run GUI
.venv\Scripts\activate && python app.py

# Complete setup and run API
.venv\Scripts\activate && python api.py

# Test API
python test_api.py
```

## 🌐 Deployment Options

- **Local Development**: Run API on localhost
- **Cloud Hosting**: Deploy to Heroku, AWS, Google Cloud
- **Edge Computing**: Package model for mobile devices

## 📊 System Requirements

- **Python**: 3.11+
- **RAM**: 4GB minimum (8GB recommended)
- **Storage**: 2GB for model downloads
- **Camera**: Any USB/built-in webcam
- **Internet**: Required for initial setup

---

**🎭 Happy Emotion Detecting! Ready for both desktop and mobile integration! 📱💻**
