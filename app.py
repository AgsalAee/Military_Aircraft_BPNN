import base64
import calendar
import time

from flask import Flask, request, json, abort, send_file
from flask_expects_json import expects_json
from flask_cors import CORS

from config.utils import checkImageSize, checkImageType, substringCircum
from config.response import response
from pickle import TRUE
import test
import remove

import os
import pandas

app = Flask(__name__)
directory_name = "files/datasets/"
upload_dir = "images/"
CORS(app)


@app.route('/datasets/<id>/', methods=['GET'])
def datasets_table(id):
    # try:
    file_list = os.listdir(directory_name)
    print(file_list)
    location = [substringCircum(fl) for fl in file_list].index(id.strip())
    if(file_list[location]):
        print(file_list[location])
        excel_data_df = pandas.read_excel(
            os.path.join(directory_name, file_list[location])).to_json(orient='records')
        json_datasets = json.loads(excel_data_df)
        return response(200, "", json_datasets), 200
    #     else:
    #         abort(404)
    # except:
    #     abort(400)


@app.route('/img/<path:filename>')
def get_image(filename):
    # return filename
    return send_file(os.path.join(upload_dir, filename))


schema = {
    "type": "object",
    "properties": {
        "id": {"type": "string"},
        "name": {"type": "string"},
        "values": {"type": "string"},
    },
    "required": ["id", "name", "values"],
    "additionalProperties": False
}


@app.route('/analyze', methods=['POST'])
@expects_json(schema)
def submit_model():
    remove.removefile()
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        json = request.get_json()
        image = base64.b64decode(str(json['values']))
        ts = calendar.timegm(time.gmtime())
        file_name = str(ts)+"-"+json['name']
        if(checkImageSize(image)):
            with open(os.path.join(upload_dir, file_name), "wb") as fh:
                fh.write(image)
                fh.close()
                if(checkImageType(upload_dir+file_name, ["jpg", "jpeg"]) == True):
                    print("image validi")
                    data = test.test_main(file_name)
                    result = {
                        "image": "/img/" + file_name,
                        "euclidian": data["euclidian"],
                        "fusi": data["fusi"],
                        "classification": data["classification"],
                    }
                    return response(200, "", result), 200
                else:
                    os.remove(os.path.join(upload_dir, file_name))
                    print("imej tidak valdi")
                    abort(400, description="Tipe imej tidak valdi")
        else:
            abort(400, description="File size too big")
    else:
        abort(400, description="Resource not found")


if __name__ == '__main__':
    app.run(debug=True, threaded=True, port=5000)
