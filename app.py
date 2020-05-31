import base64
import io
import json
import logging
import os
import os.path
from datetime import datetime

from chalice import Chalice, Response
from chalicelib.dynamodb import get_item, put_item
from chalicelib.hash import md5_checksum
from chalicelib.rekognition import detect_labels
from chalicelib.s3 import get_object, key_exists, upload_file_bytes
from chalicelib.validation import is_image
from chalicelib.config import INPUT_BUCKET, OUTPUT_BUCKET, DYNAMO_DB_TABLE
from PIL import Image, ImageDraw

logger = logging.getLogger()
logger.setLevel(logging.INFO)

app = Chalice(app_name="serverless-object-detection")


def _handle_existing_key(key: str) -> Response:
    item = get_item(DYNAMO_DB_TABLE, {"input_md5_checksum": {"S": key.split(".")[0]}})
    file_bytes = get_object(OUTPUT_BUCKET, key)["Body"].read()
    output_file_bytes = base64.b64encode(file_bytes).decode("utf-8")
    response = json.loads(item["Item"]["response"]["S"])
    prediction = {
        i["Name"]: {
            "confidence": f"{i['Confidence']:.3g}",
            "color": "#00d400" if i["Instances"] else "#000000",
        }
        for i in response["Labels"]
    }
    return Response(
        body={"prediction": prediction, "output_file_bytes": output_file_bytes},
        status_code=200,
        headers={"Context-Type": "text/plain"},
    )


def _get_output_file_bytes(file_bytes: bytes, rekognition_response: dict) -> bytes:
    stream = io.BytesIO(file_bytes)
    image = Image.open(stream)
    img_width, img_height = image.size
    draw = ImageDraw.Draw(image)

    for label in rekognition_response["Labels"]:
        if label["Instances"]:
            for instance in label["Instances"]:
                box = instance["BoundingBox"]
                left = img_width * box["Left"]
                top = img_height * box["Top"]
                width = img_width * box["Width"]
                height = img_height * box["Height"]
                draw.text(
                    (left, top), label["Name"], fill="#000000",
                )
                points = (
                    (left, top),
                    (left + width, top),
                    (left + width, top + height),
                    (left, top + height),
                    (left, top),
                )
                draw.line(points, fill="#00d400", width=1)
    with io.BytesIO() as output:
        image.save(output, format="png")
        output_file_bytes = output.getvalue()
    return output_file_bytes


@app.route("/upload", methods=["POST"], cors=True)
def handler():
    body = json.loads(app.current_request.raw_body)
    filename = body["filename"]
    if not is_image(filename):
        return Response(
            body=None,
            status_code=415,  # Unsuppoted Media Type
            headers={"Context-Type": "text/plain"},
        )
    file_bytes = base64.b64decode(body["filebytes"])
    file_hash = md5_checksum(file_bytes)
    file_ext = os.path.splitext(filename)[-1]
    key = file_hash + file_ext
    if key_exists(INPUT_BUCKET, key):
        _handle_existing_key(key)

    upload_file_bytes(file_bytes, INPUT_BUCKET, key)
    rekognition_response = detect_labels(INPUT_BUCKET, key)

    output_file_bytes = _get_output_file_bytes(file_bytes, rekognition_response)
    upload_file_bytes(output_file_bytes, OUTPUT_BUCKET, key)
    item = {
        "input_md5_checksum": {"S": file_hash},
        "response": {"S": json.dumps(rekognition_response)},
        "created_at": {"S": datetime.now().isoformat()},
    }
    put_item(DYNAMO_DB_TABLE, item)
    prediction = {
        i["Name"]: {
            "confidence": f"{i['Confidence']:.3g}",
            "color": "#00d400" if i["Instances"] else "#000000",
        }
        for i in rekognition_response["Labels"]
    }
    encoded_output_file_bytes = base64.b64encode(output_file_bytes).decode("utf-8")
    return Response(
        body=json.dumps(
            {"prediction": prediction, "output_file_bytes": encoded_output_file_bytes}
        ),
        status_code=rekognition_response["ResponseMetadata"]["HTTPStatusCode"],
        headers={"Content-Type": "text/plain"},
    )
