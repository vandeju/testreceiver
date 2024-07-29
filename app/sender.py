"""Script to preprocess pdfs using OCR only, this is a backup script in case the main script fails to preprocess the pdf correctly"""
import fitz
import pandas as pd
import numpy as np
from typing import Dict
import os
import ssl
import requests
from time import time
import io
import json
from httpx import ReadTimeout
import argparse
from pathlib import Path



def call_ocr(files, url, **kwargs):
    """Calls the server that has the tokenizer, kwargs are the arguments to be passed to the tokenizer

    Args:
        mode (str): whether to tokenize or decode
    """

    # print(f"Using kwargs: {kwargs}")
    def allowSelfSignedHttps(allowed):
        """
        bypass the server certificate verification on client side
        Args:
            allowed (bool): Is it allowed to use self-signed certificate
        """
        if allowed and not os.environ.get('PYTHONHTTPSVERIFY', '') and getattr(ssl, '_create_unverified_context', None):
            ssl._create_default_https_context = ssl._create_unverified_context

    allowSelfSignedHttps(True)  # this line is needed if you use self-signed certificate in your scoring service.

    # headers = {
    #     'Content-Type': 'application/json',
    # }
    body = {'data': json.dumps(kwargs)}

    try:
        response = requests.post(url=url, data=body, files=files)
        result = response.content
        result = json.loads(result)
        # print(result)
        return result

    except ReadTimeout as e:
        print("{error} : Could not reach the server.")
        return None

def call_ocr_simple(url, **kwargs):
    """Calls the server that has the tokenizer, kwargs are the arguments to be passed to the tokenizer

    Args:
        mode (str): whether to tokenize or decode
    """

    # print(f"Using kwargs: {kwargs}")
    def allowSelfSignedHttps(allowed):
        """
        bypass the server certificate verification on client side
        Args:
            allowed (bool): Is it allowed to use self-signed certificate
        """
        if allowed and not os.environ.get('PYTHONHTTPSVERIFY', '') and getattr(ssl, '_create_unverified_context', None):
            ssl._create_default_https_context = ssl._create_unverified_context

    allowSelfSignedHttps(True)  # this line is needed if you use self-signed certificate in your scoring service.

    # headers = {
    #     'Content-Type': 'application/json',
    # }
    body = {'data': json.dumps(kwargs)}

    try:
        response = requests.post(url=url, data=body)
        result = response.content
        result = json.loads(result)
        # print(result)
        return result

    except ReadTimeout as e:
        print("{error} : Could not reach the server.")
        return None
    
def test_sender(page_count=1, simple = False):
    
    filename = "testf"
    if simple:
        OCR_URL = "Http://host.docker.internal:8000/ocr_doc/"
        time1 = time()
        json_dict = call_ocr_simple(url=OCR_URL, filename=filename)
        time2 = time()
        print(f"Time taken for request: {time2-time1} for simple request")
        
        return 
    doc = fitz.open("data/test.pdf")
    title = "test"
    page_ims = []
    pix_widths = []
    pix_heights = []
    page_metadata = []
    for page_id, page in enumerate(doc):
        """Process pages """
        pix = page.get_pixmap(dpi=200)

        # original_text = page.get_text("text", flags=fitz.TEXTFLAGS_TEXT, sort=True)

        br = io.BufferedReader(io.BytesIO(pix.samples))
        page_ims.append(("files", br))
        pix_widths.append(pix.width)
        pix_heights.append(pix.height)
        page_metadata.append(
            {
                "page_id": page_id,
                "title": title,
                "filename": filename,
                "filename_with_relative_dirs": ""
            }
        )
        if page_id == page_count:
            break
    OCR_URL = "Http://host.docker.internal:8000/ocr/" #"Http://0.0.0.0:8000/ocr/"
    time1 = time()
    json_dict = call_ocr(files=page_ims, url=OCR_URL, pix_widths=pix_widths, pix_heights=pix_heights, batch=True)
    time2 = time()
    print(f"Time taken for request: {time2-time1} for {page_count} pages")
    
    

    


if __name__ == "__main__":
    test_sender(1, simple=True)
    test_sender(1)
    test_sender(10)
    test_sender(30)
