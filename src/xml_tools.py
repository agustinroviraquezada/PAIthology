import xml.etree.ElementTree as ET
import os

def create_base_xml(original_file_path, tile, name):
  tree = ET.ElementTree()
  root = ET.Element("annotation")
  folder = ET.SubElement(root, "folder")
  folder.text = str(original_file_path)
  filename = ET.SubElement(root, "filename")
  filename.text = str(name)
  path = ET.SubElement(root, "path")
  path.text =str(os.path.join(original_file_path, name))
  source = ET.SubElement(root, "source")
  ET.SubElement(source, "database").text = "Unknown"
  size = ET.SubElement(root, "size")
  width = ET.SubElement(size, "width")
  width.text = str(int(tile.image.shape[0]))
  height = ET.SubElement(size, "height")
  height.text = str(int(tile.image.shape[1]))
  depth = ET.SubElement(size, "depth")
  depth.text = str(int(3))
  segmented = ET.SubElement(root, "segmented") 
  segmented.text = '0'
  tree._setroot(root)
  for record in tile.records:
    create_object_xml(tree, record.generate_bndbox())
  return tree

def create_object_xml(tree, coordinates):
  root = tree.getroot()
  obj = ET.SubElement(root, "object") 
  name = ET.SubElement(obj, "name")
  name.text = "mitosis"
  pose = ET.SubElement(obj, "pose")
  pose.text = "Unspecified"
  truncated = ET.SubElement(obj, "truncated")
  truncated.text = '0'
  difficult = ET.SubElement(obj, "difficult")
  difficult.text = '0'
  bndbox = ET.SubElement(obj, "bndbox")
  ymin = ET.SubElement(bndbox, "xmin")
  ymin.text = str(coordinates[0])
  ymax = ET.SubElement(bndbox, "xmax")
  ymax.text = str(coordinates[1])
  xmin = ET.SubElement(bndbox, "ymin")
  xmin.text = str(coordinates[2])
  xmax = ET.SubElement(bndbox, "ymax")
  xmax.text = str(coordinates[3])
  return tree