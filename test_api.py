import requests
import base64
import json

def test_api():
    """
    Test script for the Emotion Detection API
    """
    # API endpoint
    api_url = "http://localhost:5000/api/analyze-emotion"
    
    # Test with a sample image (you can replace this with any image path)
    image_path = "test_image.jpg"  # Replace with your test image path
    
    try:
        # Read and encode image to base64
        with open(image_path, "rb") as image_file:
            encoded_image = base64.b64encode(image_file.read()).decode('utf-8')
        
        # Prepare the request data
        request_data = {
            "image": encoded_image
        }
        
        # Send POST request
        print("🔄 Sending request to API...")
        response = requests.post(api_url, json=request_data)
        
        # Print response
        print(f"📊 Status Code: {response.status_code}")
        print(f"📋 Response:")
        print(json.dumps(response.json(), indent=2))
        
    except FileNotFoundError:
        print(f"❌ Image file '{image_path}' not found!")
        print("📝 Please update the 'image_path' variable with a valid image file.")
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to API!")
        print("📝 Make sure the API server is running on http://localhost:5000")
    except Exception as e:
        print(f"❌ Error: {e}")

def test_health_check():
    """
    Test the health check endpoint
    """
    try:
        response = requests.get("http://localhost:5000/")
        print("🏥 Health Check Response:")
        print(json.dumps(response.json(), indent=2))
    except Exception as e:
        print(f"❌ Health check failed: {e}")

if __name__ == "__main__":
    print("🧪 Testing Emotion Detection API")
    print("=" * 40)
    
    # Test health check first
    test_health_check()
    print("\n" + "=" * 40)
    
    # Test emotion analysis
    test_api()
