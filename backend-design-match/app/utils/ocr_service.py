# app/utils/ocr_service.py
import boto3
from google.cloud import vision


def google_ocr(image_bytes):
    client = vision.ImageAnnotatorClient()
    image = vision.Image(content=image_bytes)
    response = client.text_detection(image=image)
    return response.text_annotations


def aws_textract(image_bytes):
    textract = boto3.client("textract")
    response = textract.detect_document_text(Document={"Bytes": image_bytes})
    return response["Blocks"]
