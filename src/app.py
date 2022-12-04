'''FastAPI app'''
import os
import logging
import json

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

from .predictor import Predictor
from .input import BaseInput
from .output import BaseOutput

app = FastAPI()
uvicorn_logger = logging.getLogger('uvicorn.error')
uvicorn_logger.setLevel(os.getenv('LOG_LEVEL', default='INFO'))
uvicorn_logger.debug('Started the FastAPI app')
predictor = Predictor()


@app.exception_handler(RequestValidationError)
def handle_client_error(_, exc):
    uvicorn_logger.debug('Exception in client application\n%s', exc)
    json_exc = json.loads(exc.json())
    error_type = json_exc[0]['type']
    error_body = f'{json_exc[0]["loc"][-1]} {json_exc[0]["msg"]}'
    return JSONResponse({error_type: error_body}, 400)


async def set_body(request, body):
    '''Set the body of the request'''
    async def receive():
        return {'type': 'http.request', 'body': body}
    request._receive = receive  # pylint: disable=protected-access


@app.middleware('http')
async def handle_request(request, call_next):
    body = await request.body()
    try:
        await set_body(request, body)
        response = await call_next(request)
        if response.status_code == 400:
            uvicorn_logger.debug(body)
        return response
    except Exception as exc:  # pylint: disable=broad-except
        uvicorn_logger.debug('Exception in server application',
                             exc_info=exc.__traceback__)
        uvicorn_logger.debug(body)
        error_type = type(exc).__name__
        return JSONResponse({error_type: str(exc)}, 500)


@app.get('/healthz')
def check_health():
    return {
        'status': 'I am healthy, thanks for asking!'
    }


@app.post('/predict', response_model=BaseOutput)
def predict_model(body: BaseInput):
    generated_texts = predictor.predict(body.text, body.top_k, body.top_p, body.n_samples)

    return {
        'generated_texts': generated_texts,
    }
