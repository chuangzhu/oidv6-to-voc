'''Python Code to Convert OpenImage Dataset (v6) into VOC XML format. '''

from xml.etree.ElementTree import Element, SubElement, Comment
import xml.etree.cElementTree as ET
from typing import NamedTuple, Iterable, List, Dict
from functools import partial
from pathlib import Path
import csv
import os

from PIL import Image


def parse_csv(csvfile):
    with open(csvfile) as f:
        csvr = csv.reader(f)
        return list(csvr)


class AnnotationRow(NamedTuple):
    imageid: str
    source: str
    labelname: str
    confidence: str
    xmin: str
    xmax: str
    ymin: str
    ymax: str
    isoccluded: str
    istruncated: str
    isgroupof: str
    isdepiction: str
    isinside: str


def convert_annfile(annfile: str, desc: str, imgd: str, outd: str):
    annl = parse_csv(annfile)[1:]
    imageids = [ann[0] for ann in annl]
    imageids = list(set(imageids))

    mapper = partial(map_anns_of_image, ann_list=annl)
    grouped_anns = map(mapper, imageids)

    desc_dict = dict(parse_csv(desc))
    xml_mapper = partial(get_xml,
                         desc_dict=desc_dict,
                         imgp=Path(imgd),
                         outp=Path(outd))
    m = map(xml_mapper, grouped_anns)
    list(m)  # run get_xml


def map_anns_of_image(imageid: str, ann_list: List[AnnotationRow]):
    filt = lambda row: filter_ann_row(row, imageid)
    filted = filter(filt, ann_list)
    return list(filted)


def filter_ann_row(ann_row, imageid):
    return ann_row[0] == imageid


def get_xml(anns_of_image: List[AnnotationRow], desc_dict: Dict[str, str],
            imgp: Path, outp: Path):
    imageid = anns_of_image[0][0]
    filename = imgp / (imageid + '.jpg')
    if not filename.exists():
        return
    im = Image.open(filename)
    width, height = im.size

    top = Element('annotation')
    child = SubElement(top, 'folder')
    child.text = 'open_images_volume'

    child_filename = SubElement(top, 'filename')
    child_filename.text = str(filename)

    child_source = SubElement(top, 'source')
    child_database = SubElement(child_source, 'database')
    child_database.text = 'Open Image Dataset v6'
    child_image = SubElement(child_source, 'image')
    child_image.text = anns_of_image[0][1]  # source

    child_size = SubElement(top, 'size')
    child_width = SubElement(child_size, 'width')
    child_width.text = str(width)
    child_height = SubElement(child_size, 'height')
    child_height.text = str(height)
    child_depth = SubElement(child_size, 'depth')
    child_depth.text = '3'

    child_seg = SubElement(top, 'segmented')
    child_seg.text = '0'

    def get_xml_object(ann_row: AnnotationRow):
        child_obj = SubElement(top, 'object')

        child_name = SubElement(child_obj, 'name')
        child_name.text = desc_dict[ann_row[2]]  # labelname
        child_pose = SubElement(child_obj, 'pose')
        child_pose.text = 'Unspecified'
        child_trun = SubElement(child_obj, 'truncated')
        child_trun.text = ann_row[9]  # istruncated
        child_diff = SubElement(child_obj, 'difficult')
        child_diff.text = '0'

        child_bndbox = SubElement(child_obj, 'bndbox')

        child_xmin = SubElement(child_bndbox, 'xmin')
        child_xmin.text = str(int(float(ann_row[4]) * width))  # xmin
        child_ymin = SubElement(child_bndbox, 'ymin')
        child_ymin.text = str(int(float(ann_row[6]) * height))  # ymin
        child_xmax = SubElement(child_bndbox, 'xmax')
        child_xmax.text = str(int(float(ann_row[5]) * width))  # xmax
        child_ymax = SubElement(child_bndbox, 'ymax')
        child_ymax.text = str(int(float(ann_row[7]) * height))  # ymax

    # Iterate for each object in a image.
    m = map(get_xml_object, anns_of_image)
    list(m)

    tree = ET.ElementTree(top)
    save = outp / (imageid + '.xml')
    tree.write(save)


def convert(annotation_files: Iterable[str],
            desc: str,
            imgd: str,
            outd: str = 'converted.d'):
    for f in annotation_files:
        convert_annfile(f, desc, imgd, outd)
