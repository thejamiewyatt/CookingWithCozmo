'''
This file contains code that runs tensorflow. Most of it should only be changed if the model type is switched,
or you know what you are doing.
'''


import os
import time
import numpy as np
import tensorflow as tf
from globals import resource_dir

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'



def load_graph(model_file):
    global graph
    graph = tf.Graph()
    graph_def = tf.GraphDef()

    with open(model_file, "rb") as f:
        graph_def.ParseFromString(f.read())
    with graph.as_default():
        tf.import_graph_def(graph_def)

    return graph


def read_tensor_from_image_file(file_name, input_height=299, input_width=299,
                                input_mean=0, input_std=255):
    input_name = "file_reader"
    output_name = "normalized"
    file_reader = tf.read_file(file_name, input_name)
    # only supporting .jpeg right now
    image_reader = tf.image.decode_jpeg(file_reader, channels=3, name='jpeg_reader')
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

    """
    Analyzes a photo, and returns a dict containing predictions and confidence

    :param filename: the file name of the photo to be analyzed
    :return: a dictionary with the form {'name_of_food_1' : confidence, ..., 'name_of_food_5 : confidence}

    """

    global graph, model_file, label_file
    print("Looking good so far")
    print(filename)

    input_filepath = os.path.abspath(filename)

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

    seconds = round(end - start, 3)
    print('\nEvaluation time (1-image): {:.3f}s\n'.format(end - start))

    resp = {}
    resp["seconds"] = seconds
    answer = {}
    for i in top_k:
        # print(labels[i], results[i])
        answer[labels[i]] = float(results[i])

    resp["answer"] = answer

    # os.remove(input_filepath)

    return answer


def allowed_file(filename):
    '''
    Checks to see if the filename supplied is in ALLOWED_EXTENTIONS

    :param filename: a file name to be checked
    :return: True if the filename is valid, False otherwise
    '''

    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# Load the model and graph
print(resource_dir)
model_file = f"{resource_dir}/output_graph.pb"
label_file = f"{resource_dir}/output_labels.txt"
graph = load_graph(model_file)

