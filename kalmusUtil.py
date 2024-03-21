import base64
import json
import os
import cv2
import numpy as np
import pandas as pd
from kalmus.barcodes.BarcodeGenerator import BarcodeGenerator
from kalmus.tkinter_windows.gui_utils import update_hist
from matplotlib import pyplot as plt
from sklearn.cluster import KMeans
from skimage.color import rgb2hsv
from pyciede2000 import ciede2000

def init_barcode_gn(json_path):
	# Initialize the barcode generator
	barcode_gn = BarcodeGenerator()
	with open(json_path, 'r') as f:
		json_data = json.loads(f.read())
	barcode_gn.generate_barcode_from_json(json_file_path=json_path,
										  barcode_type=json_data['barcode_type'])
	return barcode_gn

def generate_barcode(video_filename, barcode_type, frame_type, color_metric, var_save_json, json_filename, var_multi_thread, multi_thread, var_saved_frame, save_frames_rate, var_rescale_frame, rescale_factor, letterbox_option, high_ver, low_ver, left_hor, right_hor, unit_type, total_frames_str, sampled_frame_rate_str, skip_over_str):

	# Update all the parameters to the barcode generator

	barcode_gn = BarcodeGenerator()

	if unit_type == "Frame":
		if len(skip_over_str) == 0 or skip_over_str.lower() == "start":
			skip_over = 0
		else:
			skip_over = int(skip_over_str)

		if len(total_frames_str) == 0 or total_frames_str.lower() == "end":
			total_frames = int(1e8)
		else:
			total_frames = int(total_frames_str)

		if len(sampled_frame_rate_str) == 0:
			sampled_frame_rate = 1
		else:
			sampled_frame_rate = int(sampled_frame_rate_str)
	elif unit_type == "Time":
		video = cv2.VideoCapture(video_filename)
		fps = video.get(cv2.CAP_PROP_FPS)
		if len(skip_over_str) == 0 or skip_over_str.lower() == "start":
			skip_over = 0
		else:
			split_pos = skip_over_str.find(":")
			skip_over = int((int(skip_over_str[:split_pos]) * 60 + int(skip_over_str[split_pos + 1:])) * fps)

		if len(sampled_frame_rate_str) == 0:
			sampled_frame_rate = 1
		else:
			sampled_frame_rate = int(round(float(sampled_frame_rate_str) * fps))

		if len(total_frames_str) == 0 or total_frames_str.lower() == "end":
			total_frames = int(1e8)
		else:
			split_pos = total_frames_str.find(":")
			total_frames = (int(total_frames_str[:split_pos]) * 60 + int(total_frames_str[split_pos + 1:])) * fps
			total_frames -= skip_over
			total_frames = int(total_frames)
			total_frames //= sampled_frame_rate


	barcode_gn.barcode_type = barcode_type
	barcode_gn.frame_type = frame_type
	barcode_gn.color_metric = color_metric
	barcode_gn.sampled_frame_rate = sampled_frame_rate
	barcode_gn.skip_over = skip_over
	barcode_gn.total_frames = total_frames

	if var_save_json:
		if len(json_filename) == 0:
			json_filename = None
		if json_filename and (not json_filename.endswith(".json")):
			json_filename += ".json"

	# Check if user choose the multi-thread or not
	if not var_multi_thread:
		multi_thread = None
	elif var_multi_thread:
		# If user choose to use the multi-thread, then get the number of threads that will be used
		multi_thread = int(multi_thread)
		if multi_thread < 1:
			multi_thread = 1

	# Check if user choose to save the frames or not
	if var_saved_frame:
		save_frames_rate = int(save_frames_rate)
		save_frames = True
	else:
		save_frames_rate = -1
		save_frames = False

	# Check if user choose to rescale the frames or not
	if var_rescale_frame:
		rescale_factor = float(rescale_factor)
	else:
		rescale_factor = -1

	# Check if user choose to define the letter box region manually
	if letterbox_option == "Manual":
		# Update the letter box parameters, if user choose Manual
		high_ver = int(high_ver)
		low_ver = int(low_ver)
		left_hor = int(left_hor)
		right_hor = int(right_hor)
		# Start the generation
		barcode_gn.generate_barcode(video_filename, user_defined_letterbox=True,
												low_ver=low_ver, high_ver=high_ver,
												left_hor=left_hor, right_hor=right_hor,
												num_thread=multi_thread, save_frames=save_frames,
												rescale_frames_factor=rescale_factor,
												save_frames_rate=save_frames_rate)

	elif letterbox_option == "Auto":
		# try:
		#     If not, start the generation.
		#     The letter box will be automatically found during the generation process
		barcode_gn.generate_barcode(video_filename, num_thread=multi_thread,
												save_frames=save_frames,
												rescale_frames_factor=rescale_factor,
												save_frames_rate=save_frames_rate)

	# Correct the total frames
	total_frames = barcode_gn.get_barcode().total_frames

	# Get the key of the barcode, which will be later stored in the memory stack (dictionary)
	start_pos = video_filename.rfind("/") + 1
	if start_pos < 0:
		start_pos = 0
	end_pos = video_filename.rfind(".")
	videoname = video_filename[start_pos:end_pos] + "_" + barcode_type + "_" + frame_type + "_" + color_metric \
				+ "_" + str(skip_over) + "_" + str(sampled_frame_rate) + "_" + str(total_frames)

	# Get the barcode from the barcode generator
	barcode = barcode_gn.get_barcode()
	if var_save_json:
		try:
			barcode.save_as_json(json_filename)
			if json_filename is None:
				json_filename = "saved_{:s}_barcode_{:s}_{:s}.json" \
					.format(barcode.barcode_type, barcode.frame_type, barcode.color_metric)
				json_filename = os.path.abspath(json_filename)
			json_saved_success_message = "\nand is saved as a JSON object at path: {:20s}" \
				.format(json_filename)
		except Exception as e:
			json_saved_success_message = ""
			print("Error while saving the barcode as a JSON object: ", e)
	else:
		json_saved_success_message = ""

	# Clear the cv2 captured video object
	barcode.video = None

	# Update the user pre-defined meta data to the computed barcode
	# barcode.meta_data = copy.deepcopy(self.meta_data_dict)
	return barcode_gn


def get_csv(csv_filename,barcode):
	"""
	Output the per frame level data to a csv file
	"""
	# Get the file name of the output csv file


	# Get the sampled frame rate of the barcode
	sample_rate = barcode.sampled_frame_rate

	# Get the starting/skipped over frame of the barcode
	starting_frame = barcode.skip_over

	# Generate the corresponding csv file for the type of the barcode
	if barcode.barcode_type == 'Color':
		# Data frame of the csv file for the color barcode
		colors = barcode.colors
		hsvs = rgb2hsv(colors.reshape(-1, 1, 3).astype("float64") / 255)
		hsvs[..., 0] = 360 * hsvs[..., 0]
		colors = colors.astype("float64")
		brightness = 0.299 * colors[..., 0] + 0.587 * colors[..., 1] + 0.114 * colors[..., 1]

		colors = colors.astype("uint8")
		hsvs = hsvs.reshape(-1, 3)
		brightness = brightness.astype("int64")

		frame_indexes = np.arange(starting_frame, len(colors) * sample_rate + starting_frame, sample_rate)

		dataframe = pd.DataFrame(data={'Frame index': frame_indexes,
									   'Red (0-255)': colors[..., 0],
									   'Green (0-255)': colors[..., 1],
									   'Blue (0-255)': colors[..., 2],
									   'Hue (0 -360)': (hsvs[..., 0]).astype("int64"),
									   'Saturation (0 - 1)': hsvs[..., 1],
									   'Value (lightness) (0 - 1)': hsvs[..., 2],
									   'Brightness': brightness})

	elif barcode.barcode_type == 'Brightness':
		# Data frame of the csv file for the brightness barcode
		brightness = barcode.brightness

		frame_indexes = np.arange(starting_frame, len(brightness) * sample_rate + starting_frame, sample_rate)
		# Get the per frame level brightness data
		dataframe = pd.DataFrame(data={'Frame index': frame_indexes,
									   'Brightness': brightness.astype("uint8").reshape(-1)})

	dataframe = dataframe.set_index('Frame index')
	dataframe.to_csv(csv_filename)


def rgb2lab(inputColor):
	RGB=[0,0,0]
	for i in range(0,len(inputColor)):
		RGB[i]=inputColor[i]/255.0

	X=RGB[0]*0.4124+RGB[1]*0.3576+RGB[2]*0.1805
	Y=RGB[0]*0.2126+RGB[1]*0.7152+RGB[2]*0.0722
	Z=RGB[0]*0.0193+RGB[1]*0.1192+RGB[2]*0.9505
	XYZ=[X,Y,Z]
	XYZ[0]/=95.045/100
	XYZ[1]/=100.0/100
	XYZ[2]/=108.875/100

	L=0
	for i in range(0,3):
		v=XYZ[i]
		if v>0.008856:
			v=pow(v,1.0/3)
			if i==1:
				L=116.0*v-16.0
		else:
			v*=7.787
			v+=16.0/116
			if i==1:
				L=903.3*XYZ[i]
		XYZ[i]=v

	a=500.0*(XYZ[0]-XYZ[1])
	b=200.0*(XYZ[1]-XYZ[2])
	Lab=[int(L),int(a),int(b)]
	return Lab


def get_color_dominant(which, barcode, base_color_list=None, colors=None):
	try:
		if base_color_list is None:
			base_color_list = [(0, 0, 0), (38.15, 50.39, 31.83), (53.58, 0.0, -0.0), (54.29, 80.81, 69.89),
							   (75.59, 27.52, 79.12), (29.57, 68.3, -112.03), (90.67, -50.66, -14.96),
							   (60.17, 93.55, -60.5), (100.0, 0.0, -0.0), (97.61, -15.75, 93.39), (87.82, -79.28, 80.99)]
		if colors is None:
			colors = ['black', 'brown', 'grey', 'red', 'orange', 'blue', 'cyan', 'magenta', 'white', 'yellow', 'green']

		frame = barcode.saved_frames
		frame = frame[which][:][:][:]
		frame = np.array(frame).reshape(-1, 3)
		frame = frame.tolist()

		dict_color = dict(zip(colors, base_color_list))
		dict_result = {'total': 0}
		for color in colors:
			dict_result[color] = 0

		for f in frame:
			dict_temp = {}
			for color in colors:
				lab1 = rgb2lab(f)
				dict_temp[color] = ciede2000(lab1, dict_color[color])['delta_E_00']
			# 获取字典最小值的键
			min_key = min(dict_temp, key=dict_temp.get)
			dict_result[min_key] += 1
			dict_result['total'] += 1
		# 构造echarts数据
		returnList = []
		for color in colors:
			returnList.append({'name': color, 'value': dict_result[color]})
		print(returnList)
		return returnList
	except Exception as e:
		print(e)
		returnList = []
		for color in colors:
			returnList.append({'name': color, 'value': 0})
		print(returnList)
		return returnList


def get_img_base64(fileName,which,barcode):
	try:
		frame = barcode.saved_frames
		frame = frame[which][:][:][:]
		plt.imshow(frame)
		plt.axis('tight')
		plt.axis("off")
		plt.tight_layout()
		plt.savefig(f"static/{fileName}-{which}.jpeg")
		plt.close()
		# 转换为base64
		with open(f"static/{fileName}-{which}.jpeg", "rb") as f:
			base64_data = base64.b64encode(f.read())
			base64_data = base64_data.decode("ascii")
		return base64_data
	except Exception as e:
		with open(f"static/blank.png", "rb") as f:
			base64_data = base64.b64encode(f.read())
			base64_data = base64_data.decode("ascii")
		return base64_data


def draw_hue_histogram(barcode,fileName):
	# Set up the plotted figure
	fig, ax = plt.subplots(figsize=(9, 5))
	update_hist(barcode, ax=ax, bin_step=5)

	# Plot the histogram based on the barcode's type
	if barcode.barcode_type == "Color":
		ax.set_xticks(np.arange(0, 361, 30))
		ax.set_xlabel("Color Hue (0 - 360)")
		ax.set_ylabel("Number of frames")
	else:
		ax.set_xticks(np.arange(0, 255, 15))
		ax.set_xlabel("Brightness (0 - 255)")
		ax.set_ylabel("Number of frames")

	# 绘图并保存
	plt.savefig(f"static/{fileName}-hue_hist.jpeg")
	plt.close()
	# 转换为base64
	with open(f"static/{fileName}-hue_hist.jpeg", "rb") as f:
		base64_data = base64.b64encode(f.read())
		base64_data = base64_data.decode("ascii")
	return base64_data

def get_color_highlight(which, barcode, base_color_list=None, colors=None,k=5):
	try:
		if base_color_list is None:
			base_color_list = [(53, 80, 67), (68, 38, 75), (80, 12, 82), (89, -6, 88), (97, -21, 94), (94, -33, 91),
							   (92, -48, 89), (90, -65, 86), (87, -86, 83), (88, -75, 42), (89, -65, 18), (90, -56, 0),
							   (91, -48, -14), (82, -34, -27), (71, -15, -44), (56, 13, -67), (32, 79, -107),
							   (41, 83, -91),
							   (49, 88, -79), (55, 93, -69), (60, 98, -60), (58, 94, -46), (56, 89, -27), (55, 85, 0)]
		if colors is None:
			# 从"1"到24
			colors = [str(i) for i in range(1, 25)]

		frame = barcode.saved_frames
		frame = frame[which][:][:][:]
		frame = np.array(frame).reshape(-1, 3)

		estimator = KMeans(n_clusters=k, max_iter=4000, init='k-means++', n_init=50)  # 构造聚类器
		estimator.fit(frame)  # 聚类
		centroids = estimator.cluster_centers_  # 聚类中心

		frame = centroids

		dict_color = dict(zip(colors, base_color_list))
		dict_result = {}
		for color in colors:
			dict_result[color] = 0

		for f in frame:
			dict_temp = {}
			for color in colors:
				lab1 = rgb2lab(f)
				dict_temp[color] = ciede2000(lab1, dict_color[color])['delta_E_00']
			# 获取字典最小值的键
			min_key = min(dict_temp, key=dict_temp.get)
			dict_result[min_key] += 1
		# 构造echarts数据
		returnList = []
		for color in colors:
			returnList.append(5 + dict_result[color])
		print(returnList)
		return returnList
	except Exception:
		returnList = []
		for color in colors:
			returnList.append(0)
		return returnList
