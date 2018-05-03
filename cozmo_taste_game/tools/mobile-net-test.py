import argparse
import os
import time
import numpy as np
import tensorflow as tf
from sys import argv

'''
A standalone program which analyzes a picture. 
Note: the model and labels that are being tested should be in ./output

'''


def load_graph(model_file):
    global graph
    graph = tf.Graph()
    graph_def = tf.GraphDef()

    with open(model_file, "rb") as f:
        graph_def.ParseFromString(f.read())
    with graph.as_default():
        tf.import_graph_def(graph_def)
    
    return graph

def read_tensor_from_image_file(file_name, input_height=224, input_width=224,
    input_mean=0, input_std=255):
    input_name = "file_reader"
    output_name = "normalized"
    file_reader = tf.read_file(file_name, input_name)
    # only supporting .jpeg right now
    image_reader = tf.image.decode_jpeg(file_reader, channels = 3, name='jpeg_reader')
    float_caster = tf.cast(image_reader, tf.float32)
    dims_expander = tf.expand_dims(float_caster, 0)
    resized = tf.image.resize_bilinear(dims_expander, [input_height, input_width])
    normalized = tf.divide(tf.subtract(resized, [input_mean]), [input_std])
    sess = tf.Session()
    result = sess.run(normalized)
    return result

def load_labels(label_file):
    label = []
    proto_as_ascii_lines = tf.gfile.GFile(label_file).readlines()
    for l in proto_as_ascii_lines:
        label.append(l.rstrip())
    return label


def analyze_photo(filename):
    global graph

    print("Looking good so far")
    print(filename)
    
    input_filepath = os.path.abspath(filename)
        
    model_file="./output/output_graph.pb"
    label_file="./output/output_labels.txt"
    input_height = 224
    input_width = 224
    input_mean = 128
    input_std = 128
   
    
    t = read_tensor_from_image_file(input_filepath,
                                        input_height=input_height,
                                        input_width=input_width,
                                        input_mean=input_mean,
                                        input_std=input_std)

    input_layer = "input"
    output_layer = "final_result"
    input_name = "import/" + input_layer
    output_name = "import/" + output_layer
    input_operation = graph.get_operation_by_name(input_name)
    output_operation = graph.get_operation_by_name(output_name)

    with tf.Session(graph=graph) as sess:
        start = time.time()
        results = sess.run(output_operation.outputs[0],
                          {input_operation.outputs[0]: t})
        end = time.time()

    results = np.squeeze(results)
    top_k = results.argsort()[-5:][::-1]
    labels = load_labels(label_file)

    seconds = round(end-start, 3)
    print('\nEvaluation time (1-image): {:.3f}s\n'.format(end-start))

    resp = {}
    resp["seconds"] = seconds
    answer = {}
    for i in top_k:
        # print(labels[i], results[i])
        answer[labels[i]] = float(results[i])

    resp["answer"] = answer

    #os.remove(input_filepath)

    
    return answer

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



photo_location = "./test.jpg"

if len(argv) > 1:
	photo_location = f'./{argv[1]}.jpg'

model_file="./output/output_graph.pb"
label_file="./output/output_labels.txt"

graph = load_graph(model_file)

    
r = analyze_photo(photo_location)
print(r) 

