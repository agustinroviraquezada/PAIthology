# This is an example of using 
# https://github.com/tensorflow/models/blob/master/research/object_detection/dataset_tools/create_pascal_tf_record.py
# The structure should be like PASCAL VOC format dataset
# +Dataset
#   +Annotations
#   +JPEGImages
# python create_tfrecords_from_xml.py --image_dir=dataset/JPEGImages 
#                                      --annotations_dir=dataset/Annotations 
#                                      --label_map_path=object-detection.pbtxt 
#                                      --output_path=data.record

import hashlib
import io
import logging
import os
from absl import app
from absl import flags
#from absl import logging


from lxml import etree
import PIL.Image
import tensorflow as tf
#import tensorflow.compat.v1 as tf
#tf.disable_v2_behavior()
import sys

from src import tfrecord_util



#from object_detection.utils import dataset_util
#from object_detection.utils import label_map_util



FLAGS = flags.FLAGS

def define_flags():
    flags.DEFINE_string('output_path', 'X:\\projects\\PAIthology\\src\\processed_data\\dataset\\tfrecord', 'Path to output TFRecord')
    flags.DEFINE_string('image_dir', '', 'Path to image directory.')
    flags.DEFINE_string('annotations_dir', '', 'Path to annotations directory.')


label_map_dict = {
    'background': 0,
    'mitosis': 1,
}


def dict_to_tf_example(data, image_dir, label_map_dict):
    """Convert XML derived dict to tf.Example proto.
    Notice that this function normalizes the bounding
    box coordinates provided by the raw data.
    Arguments:
        data: dict holding XML fields for a single image (obtained by
          running dataset_util.recursive_parse_xml_to_dict)
        image_dir: Path to image directory.
        label_map_dict: A map from string label names to integers ids.
    Returns:
        example: The converted tf.Example.
    """
    full_path = os.path.join(image_dir, data['filename'])
    with tf.io.gfile.GFile(full_path, 'rb') as fid:
        encoded_jpg = fid.read()
    encoded_jpg_io = io.BytesIO(encoded_jpg)
    image = PIL.Image.open(encoded_jpg_io)
    #if image.format != 'JPG':
    #    raise ValueError('Image format not JPG')
    key = hashlib.sha256(encoded_jpg).hexdigest()

    width = int(data['size']['width'])
    height = int(data['size']['height'])

    xmin = []
    ymin = []
    xmax = []
    ymax = []
    classes = []
    classes_text = []

    try:
        for obj in data['object']:
            xmin.append(float(obj['bndbox']['xmin']) / width)
            ymin.append(float(obj['bndbox']['ymin']) / height)
            xmax.append(float(obj['bndbox']['xmax']) / width)
            ymax.append(float(obj['bndbox']['ymax']) / height)
            classes_text.append(obj['name'].encode('utf8'))
            classes.append(label_map_dict[obj['name']])
            print(data["filename"] + "SUCESS!")

    except KeyError:
        print(data['filename'] + ' without objects!')

    example = tf.train.Example(features=tf.train.Features(feature={
        'image/height': tfrecord_util.int64_feature(height),
        'image/width': tfrecord_util.int64_feature(width),
        'image/filename': tfrecord_util.bytes_feature(data['filename'].encode('utf8')),
        'image/source_id': tfrecord_util.bytes_feature(data['filename'].encode('utf8')),
        'image/key/sha256': tfrecord_util.bytes_feature(key.encode('utf8')),
        'image/encoded': tfrecord_util.bytes_feature(encoded_jpg),
        'image/format': tfrecord_util.bytes_feature('jpeg'.encode('utf8')),
        'image/object/bbox/xmin': tfrecord_util.float_list_feature(xmin),
        'image/object/bbox/xmax': tfrecord_util.float_list_feature(xmax),
        'image/object/bbox/ymin': tfrecord_util.float_list_feature(ymin),
        'image/object/bbox/ymax': tfrecord_util.float_list_feature(ymax),
        'image/object/class/text': tfrecord_util.bytes_list_feature(classes_text),
        'image/object/class/label': tfrecord_util.int64_list_feature(classes),
    }))
    return example


def main(_):

    writer = tf.io.TFRecordWriter("X:\\projects\\PAIthology\\src\\processed_data\\dataset\\tfrecord\\tfrecord")
    #label_map_dict = label_map_util.get_label_map_dict(FLAGS.label_map_path)

    image_dir = 'X:\\projects\\PAIthology\\src\\/processed_data\\dataset\\images'
    annotations_dir = 'X:\\projects\\PAIthology\\src\\processed_data\\dataset\\annotations'
    logging.info('Reading from dataset: ' + annotations_dir)
    examples_list = os.listdir(annotations_dir)

    for idx, example in enumerate(examples_list):
        if example.endswith('.xml'):
            if idx % 50 == 0:
                print('On image %d of %d' % (idx, len(examples_list)))

            path = os.path.join(annotations_dir, example)
            with tf.io.gfile.GFile(path, 'r') as fid:
                xml_str = fid.read()
            xml = etree.fromstring(xml_str)
            data = tfrecord_util.recursive_parse_xml_to_dict(xml)['annotation']

            tf_example = dict_to_tf_example(data, image_dir, label_map_dict)
            writer.write(tf_example.SerializeToString())

    writer.close()


if __name__ == '__main__':

    app.run(main)

    """raw_dataset = tf.data.TFRecordDataset(
        "X:\\projects\\PAIthology\\src\\processed_data\\dataset\\tfrecord\\tfrecord")

    for raw_record in raw_dataset.take(1):
        example = tf.train.Example()
        example.ParseFromString(raw_record.numpy())
        print(example)"""
    

# Import needed variables from tensorflow
# From tensorflow/models/research/
#protoc object_detection/protos/*.proto --python_out=.
#export PYTHONPATH=$PYTHONPATH:`pwd`:`pwd`/slim
#python object_detection/builders/model_builder_test.py