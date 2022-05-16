### Custom Export Format for WSP Ecology Team

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

# def dump_task_anno(dst_file, task_data, callback):
#     dumper = create_xml_dumper(dst_file)
#     dumper.open_document()
#     callback(dumper, task_data)
#     dumper.close_document()

# def dump_media_files(task_data: TaskData, img_dir: str, project_data: ProjectData = None):
#     ext = ''
#     if task_data.meta['task']['mode'] == 'interpolation':
#         ext = FrameProvider.VIDEO_FRAME_EXT

#     frame_provider = FrameProvider(task_data.db_task.data)
#     frames = frame_provider.get_frames(
#         frame_provider.Quality.ORIGINAL,
#         frame_provider.Type.BUFFER)
#     for frame_id, (frame_data, _) in enumerate(frames):
#         frame_name = task_data.frame_info[frame_id]['path'] if project_data is None \
#             else project_data.frame_info[(task_data.db_task.id, frame_id)]['path']
#         img_path = osp.join(img_dir, frame_name + ext)
#         os.makedirs(osp.dirname(img_path), exist_ok=True)
#         with open(img_path, 'wb') as f:
#             f.write(frame_data.getvalue())

def get_img_metadata(img_name):
    s3 = boto3.resource('s3', region_name='ap-southeast-2')
    bucket = s3.Bucket('animal-crossing')
    obj = bucket.Object(img_name)
    body = obj.get()['Body']
    img = Image(body)

    if img.has_exif:
        try:
            capture_datetime = datetime.datetime.strptime(img.datetime, "%Y:%m:%d %H:%M:%S")
            capture_date = capture_datetime.date
            capture_time = capture_datetime.time
            return capture_date, capture_time
        except AttributeError:
            capture_datetime = (f"Image EXIF does not contain datetime")
            return None, None

def write_to_csv(f, task_data):
    # iterate over all frames
    for frame_annotation in task_data.group_by_frame():
        #get frame info
        image_name = frame_annotation.name
        capture_date, capture_time = get_img_metadata(image_name)



def _export_task(dst_file, task_data, anno_callback, save_images=False):
    with TemporaryDirectory() as temp_dir:
        with open(osp.join(temp_dir, 'annotations.csv'), 'wb') as f:
            dump_task_anno(f, task_data, anno_callback)

        if save_images:
            dump_media_files(task_data, osp.join(temp_dir, 'images'))

        make_zip_archive(temp_dir, dst_file)

# def _export_project(dst_file: str, project_data: ProjectData, anno_callback: Callable, save_images: bool=False):
#     with TemporaryDirectory() as temp_dir:
#         with open(osp.join(temp_dir, 'annotations.xml'), 'wb') as f:
#             dump_project_anno(f, project_data, anno_callback)

#         if save_images:
#             for task_data in project_data.task_data:
#                 subset = get_defaulted_subset(task_data.db_task.subset, project_data.subsets)
#                 subset_dir = osp.join(temp_dir, 'images', subset)
#                 os.makedirs(subset_dir, exist_ok=True)
#                 dump_media_files(task_data, subset_dir, project_data)

#         make_zip_archive(temp_dir, dst_file)


@exporter(name='CVAT for images', ext='ZIP', version='1.1')
def _export_images(dst_file, instance_data, save_images=False):
    if isinstance(instance_data, TaskData):
        _export_task(dst_file, instance_data,
            anno_callback=dump_as_cvat_annotation, save_images=save_images)
    # else:
    #     _export_project(dst_file, instance_data,
    #         anno_callback=dump_as_cvat_annotation, save_images=save_images)