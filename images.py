from clarifai_grpc.channel.clarifai_channel import ClarifaiChannel
from clarifai_grpc.grpc.api import resources_pb2, service_pb2, service_pb2_grpc
from clarifai_grpc.grpc.api.status import status_code_pb2
import base64
import os

# Your PAT (Personal Access Token) can be found in the portal under Authentication
PAT = "adde818caa7d4daf9786dd350ed3faba"
# Specify the correct user_id/app_id pairings
# Since you're making inferences outside your app's scope
USER_ID = "openai"
APP_ID = "dall-e"
# Change these to whatever model and text URL you want to use
MODEL_ID = "DALL-E"
MODEL_VERSION_ID = "f1756115761940bd820e61383de79351"

channel = ClarifaiChannel.get_grpc_channel()
stub = service_pb2_grpc.V2Stub(channel)

metadata = (("authorization", "Key " + PAT),)

userDataObject = resources_pb2.UserAppIDSet(user_id=USER_ID, app_id=APP_ID)


def create_from_data(data, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    image_number = 0
    for element in data:
        if element["type"] != "image":
            continue
        image_number += 1
        image_name = f"image_{image_number}.webp"
        generate(
            element["description"] + ". Vertical image, fully filling the canvas.",
            os.path.join(output_dir, image_name),
        )


import base64
import numpy as np
import cv2


def generate(prompt, output_file, size="1024x1792"):
    post_model_outputs_response = stub.PostModelOutputs(
        service_pb2.PostModelOutputsRequest(
            user_app_id=userDataObject,
            model_id=MODEL_ID,
            version_id=MODEL_VERSION_ID,
            inputs=[
                resources_pb2.Input(
                    data=resources_pb2.Data(text=resources_pb2.Text(raw=prompt))
                )
            ],
        ),
        metadata=metadata,
    )
    if post_model_outputs_response.status.code != status_code_pb2.SUCCESS:
        print(post_model_outputs_response.status)
        raise Exception(
            "Post model outputs failed, status: "
            + post_model_outputs_response.status.description
        )

    output = post_model_outputs_response.outputs[0].data.image.base64

    with open(output_file, "wb") as f:
        f.write(output)

    # Resize the image after decoding
    img = cv2.imread(output_file)
    resized_img = cv2.resize(img, (1920, 1080))
    cv2.imwrite(output_file, resized_img)
