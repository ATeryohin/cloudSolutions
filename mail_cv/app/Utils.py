import json
import os
import shutil

import cv2
import requests

__all__ = ["request_to_cv"]

def request_to_cv(image_path, n):
    url = "https://smarty.mail.ru/api/v1/objects/detect?oauth_provider=mcs&oauth_token=XXX"
    meta_data = json.dumps({"mode":["object", "scene"], "images":[{"name":"file_0"}]})
    files = {}
    files["file_0"] = open(image_path, "rb")
    res = requests.post(url, data={"meta": meta_data}, files=files, headers={})

    data = res.json()["body"]

    objects = [(i["eng"], i["coord"], i["prob"]) for i in data["object_labels"][0]["labels"]]

    print(data)

    image = cv2.imread(image_path)

    for k, i in enumerate(objects):
        name, coord, prob = i
        x1, y1, x2, y2 = coord
        cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 4, 1)

        cv2.putText(image, f"{name} - {prob}", (x1 + 10, y1 + (k + 1) * 30), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 3, cv2.LINE_AA)

    try:
        if data["scene_labels"][0] is not None:
            scene = (data["scene_labels"][0]["labels"][0]["eng"],
                     data["scene_labels"][0]["labels"][0]["prob"])

            cv2.putText(image, scene[0], (30,30), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 3, cv2.LINE_AA)
            cv2.putText(image, str(scene[1]), (60, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 3, cv2.LINE_AA)
    except Exception:
        print("No scene data")

    if os.path.exists("/home/ateryohin/workspace/python/mail_cv/app/static/upload/render_image.jpg"):
        # shutil.rm("/home/ateryohin/workspace/python/mail_cv/app/static/upload/render_image.jpg")
        os.remove("/home/ateryohin/workspace/python/mail_cv/app/static/upload/render_image.jpg")

    cv2.imwrite(f"/home/ateryohin/workspace/python/mail_cv/app/static/upload/render_image_{n}.jpg", image)


# def request_to_cv(image_path):
#     url = "https://smarty.mail.ru/api/v1/persons/recognize?oauth_provider=mcs&oauth_token=XXX"
#     meta_data = json.dumps({"images": [{"name": "file_0"}], "space": "1"})
#     files = {}
#     files["file_0"] = open(image_path, "rb")
#     res = requests.post(url, data={"meta": meta_data}, files=files, headers={})
#
#     objects = res.json()["body"]
#
#     print(objects)
#
#     persons = [i for i in objects["objects"][0]["persons"]]
#
#     image = cv2.imread(image_path)
#     for i in persons:
#         x1, y1, x2, y2 = i['coord']
#         cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 4, 1)
#         print(i)
#
#     cv2.imwrite("/home/ateryohin/workspace/python/mail_cv/app/static/upload/render_image.jpg", image)
