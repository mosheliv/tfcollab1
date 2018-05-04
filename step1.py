import numpy as np
import tensorflow as tf
import cv2 as cv
import sys
import glob
import os

# Read the graph.
with tf.gfile.FastGFile('ssd_mobilenet_v2_coco_2018_03_29/frozen_inference_graph.pb') as f:
#with tf.gfile.FastGFile('ssd_inception_v2_coco_2017_11_17/frozen_inference_graph.pb') as f:
	graph_def = tf.GraphDef()
	graph_def.ParseFromString(f.read())

with tf.Session() as sess:
	# Restore session
	sess.graph.as_default()
	tf.import_graph_def(graph_def, name='')

	low_prob_count = 0
	low_prob_count_1st = 0
	no_bird = 0
	fcount = 0
	csvf = open("detections.csv", "w")
	csvf.write("filename, width, hight, class, xmin, ymin, xmax, ymax\n")

	for fn in glob.glob(sys.argv[1]+"/*.jpg"):
		print("processing %s" % fn)
		fcount += 1
    # Read and preprocess an image.
		img = cv.imread(fn)
		rows = img.shape[0]
		cols = img.shape[1]
		inp = cv.resize(img, (300, 300))
		inp = inp[:, :, [2, 1, 0]]  # BGR2RGB

		# Run the model
		out = sess.run([sess.graph.get_tensor_by_name('num_detections:0'),
				    sess.graph.get_tensor_by_name('detection_scores:0'),
				    sess.graph.get_tensor_by_name('detection_boxes:0'),
				    sess.graph.get_tensor_by_name('detection_classes:0')],
				   feed_dict={'image_tensor:0': inp.reshape(1, inp.shape[0], inp.shape[1], 3)})

		# Visualize detected bounding boxes.
		num_detections = int(out[0][0])
		for i in range(num_detections):
			classId = int(out[3][0][i])
			if classId != 16:
				no_bird += 1
				continue
			score = float(out[1][0][i])
			bbox = [float(v) for v in out[2][0][i]]
			x = bbox[1] * cols
			y = bbox[0] * rows
			right = bbox[3] * cols
			bottom = bbox[2] * rows
			if score > 0.6:
				cv.rectangle(img, (int(x), int(y)), (int(right), int(bottom)), 2, thickness=1)
				csvf.write("{}, {}, {}, {}, {}, {}, {}, {}\n".format(os.path.basename(fn), cols, rows, "Blackbird", bbox[1], bbox[0], bbox[3], bbox[2]))
			else:
				label = "confidence {}, classid {}, detection index {}".format(score, classId, i)
				print(label)
				low_prob_count += 1
				cv.rectangle(img, (int(x), int(y)), (int(right), int(bottom)), 1, thickness=3)
				cv.imshow(label, img)
				while True:
					key = cv.waitKey(0)
					if key not in [ord('y'), ord('n')]:
						print("y or n")
					else:
						break
				if key == 'y':
					csvf.write("{}, {}, {}, {}, {}, {}, {}, {}\n".format(os.path.basename(fn), cols, rows, "Blackbird", bbox[1], bblox[0], bbox[3], bbox[2]))
				cv.destroyAllWindows()
				
print("low prob count %d" % low_prob_count)
print("low prob 1st count %d" % low_prob_count_1st)
print("no bird %d" % no_bird)
print("total file count %d" % fcount)
csvf.close()
