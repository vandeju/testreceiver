"""Scoring script used in the bi and cross sentencetransformer backend for inference"""
import os
import json
from fastapi import FastAPI, File, UploadFile, Depends, Form
from fastapi.responses import RedirectResponse
from pydantic import BaseModel, ConfigDict
from typing import Union, List, TypeAlias
from glob import glob
import numpy as np
from json import JSONDecodeError
import fitz
import io
from time import time
import asyncio
import array
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import HTTPException
from fastapi import status
from pydantic.error_wrappers import ValidationError

os.environ["MASTER_ADDR"] = "localhost"
os.environ["MASTER_PORT"] = "29500"

BATCH_MAX = 64

class TEST_input(BaseModel):
    """Input for the bi encoder
    
        :param query: A sentence or a list of sentences as str, List[str]
        :param batch_size: The batch size for the bi encoder        
        :param normalize_embeddings: Normalize the embeddings before returning them, set to false since GTE-Large is already normalized    
    """

    pix_widths: List
    pix_heights: List
    batch: bool

    model_config = ConfigDict(arbitrary_types_allowed=True,)

class TEST_doc_input(BaseModel):
    """Input for the bi encoder
    
        :param query: A sentence or a list of sentences as str, List[str]
        :param batch_size: The batch size for the bi encoder        
        :param normalize_embeddings: Normalize the embeddings before returning them, set to false since GTE-Large is already normalized    
    """

    filename: str

    model_config = ConfigDict(arbitrary_types_allowed=True,)



def init():
    print("Initializing")

init()

app = FastAPI()


def doc_checker(data: str = Form(...)):
    """Checks the input data for API"""
    try:
        return TEST_doc_input.model_validate_json(data)
    except ValidationError as e:
        print(data)
        raise HTTPException(
            detail=jsonable_encoder(e.errors()),
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        )
def checker(data: str = Form(...)):
    """Checks the input data for API"""
    try:
        return TEST_input.model_validate_json(data)
    except ValidationError as e:
        print(data)
        raise HTTPException(
            detail=jsonable_encoder(e.errors()),
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        )

@app.post("/ocr_doc/")
def TEST_doc(input: TEST_doc_input = Depends(doc_checker)):
    """Runs the TEST model on the input image
    Args:
        input (TEST_input): The input image
    Returns:
        Dict: The OCR output
    """

    print("Receiving request")
    return input.filename

@app.post("/ocr/")
def TEST(input: TEST_input = Depends(checker), files: List[UploadFile] = File(...)):
    """Runs the TEST model on the input image
    Args:
        input (TEST_input): The input image
    Returns:
        Dict: The OCR output
    """
    global counter
    # image = json.loads(input.image)

    print("Receiving request")
    time1 = time()
    im_list = []
    # for image_list in files:
    #     im_list.append(image_list.file.read())


    # input_dict = {
    #     "files": im_list,
    #     "id": 0,
    #     "pix_widths": input.pix_widths,
    #     "pix_heights": input.pix_heights,
    #     "batch": input.batch
    # }
    time2 = time()
    print(f"Time taken for request: {time2-time1}")
    return None


@app.get("/status/ping/")
@app.get("/status/health/")
def status():
    """Health check endpoint"""
    return {"Status": "OK"}


@app.get("/")
async def docs_redirect():
    """Redirect to docs"""
    response = RedirectResponse(url='/docs')
    return response
