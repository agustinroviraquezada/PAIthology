import xml.etree.ElementTree as ET

def create_base_xml(frame,image):
  tree = ET.ElementTree()
  root = ET.Element("annotation")
  folder = ET.SubElement(root, "folder")
  folder.text = str(frame.path)
  filename = ET.SubElement(root, "filename")
  filename.text = str(frame.filename)
  path = ET.SubElement(root, "path")
  path.text =str(frame.path)
  source = ET.SubElement(root, "source")
  ET.SubElement(source, "database").text = "Unknown"
  size = ET.SubElement(root, "size")
  width = ET.SubElement(size, "width")
  width.text = str(int(image.shape[0]))
  height = ET.SubElement(size, "height")
  height.text = str(int(image.shape[1]))
  depth = ET.SubElement(size, "depth")
  depth.text = str(int(3))
  segmented = ET.SubElement(root, "segmented") 
  segmented.text = '0'
  tree._setroot(root)
  return tree

def create_object_xml(tree,coordinates):
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