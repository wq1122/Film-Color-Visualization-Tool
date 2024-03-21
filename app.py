import json
import kalmus
from flask import Flask, request
from flask_cors import CORS
from kalmusUtil import init_barcode_gn,generate_barcode,get_csv,get_color_dominant,get_img_base64,draw_hue_histogram,get_color_highlight

app = Flask(__name__)
CORS(app)

fileName = "mission_impossible_Bright_Whole_frame_Color.json"
barcode_gn = init_barcode_gn(f"static/{fileName.split('.')[0]}.json")

@app.route('/')
def hello_world():  # put application's code here
    print(kalmus.__version__)
    return f'{kalmus.__version__}'

@app.route('/generateBarcode', methods=['POST'])
def generateBarcode():
    global fileName, barcode_gn
    fileName = request.json.get("video_filename")
    video_filename = f"static/{fileName}"
    barcode_type = request.json.get("barcode_type")
    frame_type = request.json.get("frame_type")
    color_metric = request.json.get("color_metric")
    var_save_json = 1
    json_filename = f"static/{fileName.split('.')[0]}.json"
    var_multi_thread = request.json.get("var_multi_thread")
    multi_thread = request.json.get("multi_thread")
    var_saved_frame = request.json.get("var_saved_frame")
    # save_frames_rate = request.json.get("save_frames_rate")
    save_frames_rate = 1
    var_rescale_frame = request.json.get("var_rescale_frame")
    rescale_factor = request.json.get("rescale_factor")
    letterbox_option = request.json.get("letterbox_option")
    high_ver = request.json.get("high_ver")
    low_ver = request.json.get("low_ver")
    left_hor = request.json.get("left_hor")
    right_hor = request.json.get("right_hor")
    unit_type = request.json.get("unit_type")
    total_frames_str = request.json.get("total_frames_str")
    sampled_frame_rate_str = request.json.get("sampled_frame_rate_str")
    skip_over_str = request.json.get("skip_over_str")

    barcode_gn = generate_barcode(video_filename, barcode_type, frame_type, color_metric, var_save_json, json_filename, var_multi_thread, multi_thread, var_saved_frame, save_frames_rate, var_rescale_frame, rescale_factor, letterbox_option, high_ver, low_ver, left_hor, right_hor, unit_type, total_frames_str, sampled_frame_rate_str, skip_over_str)
    with open(json_filename, 'r') as f:
        data = json.load(f)
    return json.dumps(data)

@app.route('/getCSV', methods=['GET'])
def getCSV():
    global barcode_gn,fileName
    csv_filename = f"static/{fileName.split('.')[0]}.csv"
    if barcode_gn is not None:
        get_csv(csv_filename,barcode_gn.get_barcode())
        with open(csv_filename, 'r') as f:
            data = f.read()
        return data
    else:
        return "No barcode generated yet"

@app.route('/getJson', methods=['GET','POST'])
def getJson():
    global fileName, barcode_gn
    if request.method == 'POST':
        fileName = request.json.get("json_filename")
        json_filename = f"static/{fileName.split('.')[0]}.json"
        barcode_gn = init_barcode_gn(json_filename)
        with open(json_filename, 'r') as f:
            data = json.load(f)
        return json.dumps(data)
    elif request.method == 'GET':
        json_filename = f"static/{fileName.split('.')[0]}.json"
        barcode_gn = init_barcode_gn(json_filename)
        with open(json_filename, 'r') as f:
            data = json.load(f)
        return json.dumps(data)



@app.route('/getColorDominant', methods=['POST'])
def getColorDominant():
    global barcode_gn
    which = request.json.get("which")
    res_json = get_color_dominant(which,barcode_gn.get_barcode())
    return json.dumps(res_json)

@app.route('/getImgBase64', methods=['POST'])
def getImgBase64():
    global fileName, barcode_gn
    which = request.json.get("which")
    IMG_filename = f"{fileName.split('.')[0]}"
    res_bs64 = get_img_base64(IMG_filename, which,barcode_gn.get_barcode())
    return res_bs64

@app.route('/getHueHistogram', methods=['GET'])
def getHueHistogram():
    global fileName, barcode_gn
    if barcode_gn is not None:
        barcode = barcode_gn.get_barcode()
    else:
        return "No barcode generated yet"
    IMG_filename = f"{fileName.split('.')[0]}"
    res_bs64 = draw_hue_histogram(barcode, IMG_filename)
    return res_bs64
@app.route('/getColorHighlight', methods=['POST'])
def getColorHighlight():
    global barcode_gn
    which = request.json.get("which")
    res_json = get_color_highlight(which, barcode_gn.get_barcode())
    return json.dumps(res_json)



if __name__ == '__main__':
    app.run()
