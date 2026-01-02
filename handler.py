import runpod
import requests
import numpy as np
import cv2
import os
from PIL import Image
from io import BytesIO

try:
    import face_recognition
except ImportError:
    print("face_recognition não instalado")

EXPECTED_API_KEY = "1234567890"

def download_image(url):
    """Baixa a imagem da URL fornecida"""
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        image = Image.open(BytesIO(response.content))
        return np.array(image)
    except Exception as e:
        raise Exception(f"Erro ao baixar imagem: {str(e)}")

def process_face(image_array):
    """Processa a imagem e detecta faces usando face_recognition"""
    try:
        if len(image_array.shape) == 2:
            image_array = cv2.cvtColor(image_array, cv2.COLOR_GRAY2RGB)
        elif image_array.shape[2] == 4:
            image_array = cv2.cvtColor(image_array, cv2.COLOR_RGBA2RGB)
        
        face_locations = face_recognition.face_locations(image_array)
        face_encodings = face_recognition.face_encodings(image_array, face_locations)
        face_landmarks_list = face_recognition.face_landmarks(image_array, face_locations)
        
        results = []
        for i, (location, encoding, landmarks) in enumerate(zip(face_locations, face_encodings, face_landmarks_list)):
            top, right, bottom, left = location
            
            face_data = {
                "face_id": i,
                "bounding_box": {
                    "top": int(top),
                    "right": int(right),
                    "bottom": int(bottom),
                    "left": int(left),
                    "width": int(right - left),
                    "height": int(bottom - top)
                },
                "face_encoding": encoding.tolist(),
                "landmarks": {
                    key: [(int(x), int(y)) for x, y in points]
                    for key, points in landmarks.items()
                }
            }
            results.append(face_data)
        
        return {
            "success": True,
            "faces_detected": len(results),
            "faces": results
        }
    
    except Exception as e:
        raise Exception(f"Erro ao processar faces: {str(e)}")

def handler(event):
    """Handler principal do RunPod Serverless"""
    try:
        input_data = event.get("input", {})
        
        if "url" not in input_data:
            return {"error": "Campo 'url' é obrigatório", "status": "failed"}
        
        if "apiKey" not in input_data:
            return {"error": "Campo 'apiKey' é obrigatório", "status": "failed"}
        
        if input_data["apiKey"] != EXPECTED_API_KEY:
            return {"error": "API Key inválida", "status": "unauthorized"}
        
        image_url = input_data["url"]
        image_array = download_image(image_url)
        result = process_face(image_array)
        
        return {"status": "success", "data": result}
    
    except Exception as e:
        return {"error": str(e), "status": "failed"}

if __name__ == "__main__":
    runpod.serverless.start({"handler": handler})
