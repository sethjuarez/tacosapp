from json import loads
import os
import json
import time
import logging
import requests
import datetime
import numpy as np
from PIL import Image
from io import BytesIO
import onnxruntime as rt
from torchvision import transforms

import azure.functions as func

session = None
transform = None
classes = None
input_name = None


def main(context: func.Context, req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Initiating prediction routine')
    global session, transform, classes, input_name

    prev_time = time.time()
    response = {}


    # load model if not already in global memory
    if session == None or transform == None or classes == None or input_name == None:
        logging.info('=========================>Loading model, transorms and classes')
        try:
            model_path = os.path.join(context.function_directory, 'model.onnx')
            classes = ['burrito', 'tacos']
            session = rt.InferenceSession(model_path)
            input_name = session.get_inputs()[0].name
            transform = transforms.Compose([
                    transforms.Resize(256),
                    transforms.CenterCrop(224),
                    transforms.ToTensor(),
                    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
                ])
        except Exception as error:
            logging.exception('Python Error')
            response['error'] = { 
                'code': '500',
                'message': f'{type(error).__name__}: {str(error)}'
            }
            return func.HttpResponse(json.dumps(response), status_code=200, mimetype='text/json')

    try:
        image_url = ""
        if req.method == "GET":
            image_url = req.params['image']
        else:
            image_url = req.get_json()['image']
        
        logging.info(f'=====> Loading {image_url}')

        response = requests.get(image_url)

        img = Image.open(BytesIO(response.content))
        v = transform(img)
        pred_onnx = session.run(None, {input_name: v.unsqueeze(0).numpy()})[0][0]

        current_time = time.time()
        inference_time = datetime.timedelta(seconds=current_time - prev_time)

        predictions = {}
        for i in range(len(classes)):
            predictions[classes[i]] = str(pred_onnx[i])

        response = {
            'time': str(inference_time.total_seconds()),
            'prediction': classes[int(np.argmax(pred_onnx))],
            'scores': predictions,
            'error': { }
        }
    except Exception as error:
        logging.exception('Python Error')
        response['error'] = { 
            'code': '500',
            'message': f'{type(error).__name__}: {str(error)}'
        }

    return func.HttpResponse(
        json.dumps(response),
        status_code=200,
        mimetype='text/json'
    )
    
