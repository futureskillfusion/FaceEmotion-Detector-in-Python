from flask import Flask, request, jsonify
from flask_cors import CORS
import cv2
from deepface import DeepFace
import numpy as np
import base64
import io
from PIL import Image
import traceback
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for Flutter app

def analyze_emotion_api(image_array):
    """
    Analyze emotions from image array and return results
    """
    try:
        results = DeepFace.analyze(image_array, actions=['emotion'], enforce_detection=False)
        
        emotions_data = []
        
        if isinstance(results, list):
            for result in results:
                emotion_data = {
                    'dominant_emotion': result['dominant_emotion'],
                    'emotion_scores': result['emotion'],
                    'region': {
                        'x': int(result['region']['x']),
                        'y': int(result['region']['y']),
                        'w': int(result['region']['w']),
                        'h': int(result['region']['h'])
                    },
                    'confidence': float(max(result['emotion'].values()))
                }
                emotions_data.append(emotion_data)
        else:
            # Single result
            emotion_data = {
                'dominant_emotion': results['dominant_emotion'],
                'emotion_scores': results['emotion'],
                'region': {
                    'x': int(results['region']['x']),
                    'y': int(results['region']['y']),
                    'w': int(results['region']['w']),
                    'h': int(results['region']['h'])
                },
                'confidence': float(max(results['emotion'].values()))
            }
            emotions_data.append(emotion_data)
            
        return emotions_data
        
    except Exception as e:
        print(f"Error in emotion analysis: {e}")
        traceback.print_exc()
        return []

def base64_to_image(base64_string):
    """
    Convert base64 string to OpenCV image
    """
    try:
        # Remove header if present
        if ',' in base64_string:
            base64_string = base64_string.split(',')[1]
            
        # Decode base64 to bytes
        image_bytes = base64.b64decode(base64_string)
        
        # Convert to PIL Image
        pil_image = Image.open(io.BytesIO(image_bytes))
        
        # Convert PIL to OpenCV format
        opencv_image = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)
        
        return opencv_image
        
    except Exception as e:
        print(f"Error converting base64 to image: {e}")
        return None

@app.route('/', methods=['GET'])
def home():
    """
    API health check endpoint
    """
    return jsonify({
        'status': 'success',
        'message': 'Emotion Detection API is running!',
        'version': '1.0.0',
        'endpoints': {
            'analyze_emotion': '/api/analyze-emotion (POST)',
            'health': '/ (GET)'
        }
    })

@app.route('/api/analyze-emotion', methods=['POST'])
def analyze_emotion_endpoint():
    """
    Main endpoint for emotion analysis
    Accepts base64 encoded image
    """
    try:
        # Check if request has JSON data
        if not request.is_json:
            return jsonify({
                'status': 'error',
                'message': 'Request must be JSON format'
            }), 400
            
        data = request.get_json()
        
        # Check if image data is provided
        if 'image' not in data:
            return jsonify({
                'status': 'error',
                'message': 'No image data provided. Send base64 encoded image in "image" field.'
            }), 400
            
        # Convert base64 to image
        image = base64_to_image(data['image'])
        
        if image is None:
            return jsonify({
                'status': 'error',
                'message': 'Invalid image format. Please send valid base64 encoded image.'
            }), 400
            
        # Analyze emotions
        emotions = analyze_emotion_api(image)
        
        if not emotions:
            return jsonify({
                'status': 'success',
                'message': 'No faces detected in the image',
                'emotions': [],
                'face_count': 0
            })
            
        return jsonify({
            'status': 'success',
            'message': 'Emotion analysis completed successfully',
            'emotions': emotions,
            'face_count': len(emotions)
        })
        
    except Exception as e:
        print(f"API Error: {e}")
        traceback.print_exc()
        return jsonify({
            'status': 'error',
            'message': f'Internal server error: {str(e)}'
        }), 500

@app.route('/api/test', methods=['POST'])
def test_endpoint():
    """
    Test endpoint to check if API is receiving data correctly
    """
    try:
        data = request.get_json()
        return jsonify({
            'status': 'success',
            'message': 'Test successful',
            'received_data': data
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Test failed: {str(e)}'
        }), 500

if __name__ == '__main__':
    # Print startup information
    print("🎭 Emotion Detection API Starting...")
    print("📡 Endpoints available:")
    print("   GET  /                     - Health check")
    print("   POST /api/analyze-emotion  - Analyze emotions in image")
    print("   POST /api/test             - Test endpoint")
    print("\n📋 How to use from Flutter:")
    print("   1. Convert image to base64")
    print("   2. Send POST request to /api/analyze-emotion")
    print("   3. Include base64 image in JSON: {'image': 'base64_string'}")
    print("\n🚀 Starting server...")
    
    # Run the Flask app
    app.run(
        host='0.0.0.0',  # Allow external connections
        port=5000,       # Default Flask port
        debug=True       # Enable debug mode for development
    )
