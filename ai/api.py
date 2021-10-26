import io
import json
from PIL import Image
from flask import Flask, jsonify, request
import hashlib
import yaml

import torch
from torchvision import models
import torchvision.transforms as transforms

from ai.utils.model import CustomModel
import os


app = Flask(__name__)


@app.route('/')
def hello():
    hello = "Hello API"
    return hello


# AI Models
print(f"Loading model ... ", end='')
model = CustomModel()
model.eval()
device = 'cpu'
print(f"Done!!")


def to_RGB(image:Image, file_name='./tmp/tmp.jpg'):

    os.makedirs('./tmp/', exist_ok=True)
    
    if image.mode == 'RGB': return image
    image.load() # required for png.split()
    background = Image.new("RGB", image.size, (255, 255, 255))
    background.paste(image, mask=image.split()[3]) # 3 is the alpha channel

    background.save(file_name, 'JPEG', quality=80)
    return Image.open(file_name)


def api_auth(api_key):
    hash_key = hashlib.sha256(api_key.encode('utf-8')).hexdigest()
    with open('ai/api_true_hash_key.yaml', 'r') as f:
        secret = yaml.safe_load(f)
    true_hash_key = secret['AI']['API_TRUE_HASH_KEY']
    if true_hash_key == hash_key:
        return True
    else:
        return False


def transform_image(image_bytes):
    my_transforms = transforms.Compose([transforms.Resize((512, 512)),
                                        transforms.ToTensor(),
                                        transforms.Normalize(
                                            [0.485, 0.456, 0.406],
                                            [0.229, 0.224, 0.225])])
    image = Image.open(io.BytesIO(image_bytes))
    image = to_RGB(image)
    return my_transforms(image).unsqueeze(0)


def get_vector(tensor):
    print(f"Predicting ... ", end='')
    with torch.no_grad():
        out = model(tensor)
    print(f"Done!!")
    out = out.to('cpu').detach().numpy().tolist()[0]
    return out


@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        file = request.files['file']
        if api_auth(request.headers.get('api_key')):
            image_bytes = file.read()
            tensor = transform_image(image_bytes=image_bytes)
            tensor = tensor.to(device)
            vector = get_vector(tensor)
            return jsonify({'authentication': 'ok', 'vector': vector})
        else:
            return jsonify({'authentication': 'no'})


def main():
    app.run(debug=True, port=7775)


if __name__ == "__main__":
    main()
