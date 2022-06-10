### Custom Export Format for WSP Ecology Team - allow multiple labels

from asyncore import write
from tempfile import TemporaryDirectory, TemporaryFile
import os
import os.path as osp
from cvat.apps.dataset_manager.bindings import (TaskData, match_dm_item, ProjectData, get_defaulted_subset,import_dm_annotations)
from cvat.apps.dataset_manager.util import make_zip_archive
from .registry import exporter, importer

from exif import Image
import datetime
import boto3
from botocore.handlers import disable_signing

def get_img_metadata(img_name):
    region = 'ap-southeast-2'
    s3 = boto3.resource('s3', region_name=region)
    s3.meta.client.meta.events.register('choose-signer.s3.*', disable_signing)
    client_s3 = s3.meta.client

    bucket_name = 'animal-crossing'
    bucket = s3.Bucket(bucket_name)
    obj = bucket.Object(img_name)
    body = obj.get()['Body']
    img = Image(body)

    if img.has_exif:
        try:
            capture_datetime = datetime.datetime.strptime(img.datetime, "%Y:%m:%d %H:%M:%S")
            capture_date = capture_datetime.date()
            capture_time = capture_datetime.time()
            return capture_date, capture_time
        except AttributeError:
            capture_datetime = (f"Image EXIF does not contain datetime")
            return None, None

def write_to_csv_task(f, task_data):
    # add labels columns
    title = False
    tags_num = []
    for frame_annotation in task_data.group_by_frame():
        tag_num = 0
        for tags in frame_annotation.tags:
            tag_num += 1
        tags_num.append(tag_num)
    max_tag = max(tags_num)
    label_title = ''
    for i in range(max_tag):
        label_title = label_title+',Label'+str(i+1)
    f.write('Project name,Camera name,Image name,Date,Time'+label_title+',\n')

    # add date, time, labels info for each image
    for frame_annotation in task_data.group_by_frame():
        image_path = frame_annotation.name
        project = image_path.split('/')[0]
        camera = image_path.split('/')[1]
        image_name = image_path.split('/')[-1]
        capture_date, capture_time = get_img_metadata(image_path)
        start_str = project+','+camera+','+image_name+','+str(capture_date)+','+str(capture_time)
        label_str = ''
        for tags in frame_annotation.tags:
            label = tags.label
            label_str = label_str +','+ label
        f.write(start_str+ label_str+'\n')
    f.close()

def write_to_csv_project(f, project_data):
    # add labels columns
    title = False
    tags_num = []
    for frame_annotation in project_data.group_by_frame():
        tag_num = 0
        for tags in frame_annotation.tags:
            tag_num += 1
        tags_num.append(tag_num)
    max_tag = max(tags_num)
    label_title = ''
    for i in range(max_tag):
        label_title = label_title+',Label'+str(i+1)
    f.write('Project name,Camera name,Image name,Date,Time'+label_title+',\n')

    # add date, time, labels info for each image
    for frame_annotation in project_data.group_by_frame():
        image_path = frame_annotation.name
        project = image_path.split('/')[0]
        camera = image_path.split('/')[1]
        image_name = image_path.split('/')[-1]
        capture_date, capture_time = get_img_metadata(image_path)
        start_str = project+','+camera+','+image_name+','+str(capture_date)+','+str(capture_time)
        label_str = ''
        for tags in frame_annotation.tags:
            label = tags.label
            label_str = label_str +','+ label
        f.write(start_str+ label_str+'\n')
    f.close()


def _export_task(dst_file, task_data, save_images=False):
    with TemporaryDirectory() as temp_dir:
        with open(osp.join(temp_dir, 'task_annotations_labels.csv'), 'w') as f:
            write_to_csv_task(f, task_data)

        make_zip_archive(temp_dir, dst_file)


def _export_project(dst_file: str, project_data: ProjectData, save_images: bool=False):
     with TemporaryDirectory() as temp_dir:
        with open(osp.join(temp_dir, 'project_annotations_labels.csv'), 'w') as f:
            write_to_csv_task(f, project_data)

        make_zip_archive(temp_dir, dst_file)


@exporter(name='Animal Crossing Column Labels', ext='ZIP', version='1.0')
def _export_images(dst_file, instance_data, save_images=False):
    if isinstance(instance_data, TaskData):
        _export_task(dst_file, instance_data,save_images=save_images)

    else:
         _export_project(dst_file, instance_data, save_images=save_images)
