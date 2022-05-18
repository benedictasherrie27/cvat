### Custom Export Format for WSP Ecology Team

from asyncore import write
from tempfile import TemporaryDirectory, TemporaryFile

import os
import os.path as osp

from datumaro.components.dataset import Dataset

from cvat.apps.dataset_manager.bindings import (TaskData, match_dm_item, ProjectData, get_defaulted_subset, GetCVATDataExtractor,
    import_dm_annotations)
from cvat.apps.dataset_manager.util import make_zip_archive
from cvat.apps.engine.frame_provider import FrameProvider

from .registry import dm_env, exporter, importer

from exif import Image
import datetime
import boto3


def get_img_metadata(img_name):
    s3 = boto3.resource('s3', region_name='ap-southeast-2')
    bucket = s3.Bucket('animal-crossing')
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
    # iterate over all frames
    for frame_annotation in task_data.group_by_frame():
        #get frame info
        image_path = frame_annotation.name
        project = image_path.split('/')[0]
        camera = image_path.split('/')[1]
        image_name = image_path.split('/')[-1]
        capture_date, capture_time = get_img_metadata(image_path)

        f.write(project+','+camera+','+image_name+','+str(capture_date)+','+str(capture_time)+'\n')

    f.close()

# def write_to_csv_project(f, project_data): # need to be changed!!!!! -> might need a project list
#     # iterate over all frames
#     for frame_annotation in project_data.group_by_frame():
#         #get frame info
#         image_path = frame_annotation.name

#         project = image_path.split('/')[0]
#         camera = image_path.split('/')[1]
#         image_name = image_path.split('/')[-1]
#         capture_date, capture_time = get_img_metadata(image_path)

#         f.write(project+','+camera+','+image_name+','+str(capture_date)+','+str(capture_time)+'\n')
#     f.close()


def _export_task(dst_file, task_data, save_images=False):
    with TemporaryDirectory() as temp_dir:
        with open(osp.join(temp_dir, 'annotations.csv'), 'w') as f:
            f.write('Project name,Camera name,Image name,Date,Time,\n')
            write_to_csv_task(f, task_data)

        make_zip_archive(temp_dir, dst_file)


# def _export_project(dst_file: str, project_data: ProjectData, save_images: bool=False):
#      with TemporaryDirectory() as temp_dir:
#          with open(osp.join(temp_dir, 'annotations.xml'), 'wb') as f:
#             f.write('Project name,Camera name,Image name,Date,Time/n,\n')
#             write_to_csv_project(f, project_data)

#          make_zip_archive(temp_dir, dst_file)


@exporter(name='TEST FORMAT', ext='ZIP', version='1.0')
def _export_images(dst_file, instance_data, save_images=False):
    if isinstance(instance_data, TaskData):
        _export_task(dst_file, instance_data,save_images=save_images)

    # else:
    #      _export_project(dst_file, instance_data, save_images=save_images)
