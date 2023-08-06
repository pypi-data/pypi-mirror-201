import time

import boto3
import os
import requests
import hashlib
import json
import concurrent.futures
import multiprocessing
from tqdm import tqdm
from nvos import login
import logging

# 导入全局日志记录器
logger = logging.getLogger(__name__)
daemon_network = "https://nvos-toolchain-dev.nioint.com"
global_var = 0


def upload_file(file_path_list, project_space_list):
    s3_secret = get_s3_secret()
    bucket_name = s3_secret["bucket"]
    aws_ak = s3_secret["ak"]
    aws_sk = s3_secret["sk"]
    aws_region = s3_secret["regionId"]
    logger.info(f"upload_file execute bucket {bucket_name} {aws_region} {aws_ak} {aws_sk}")
    s3 = boto3.resource('s3', region_name=aws_region, aws_access_key_id=aws_ak,
                        aws_secret_access_key=aws_sk)
    bucket = s3.Bucket(bucket_name)
    upload_list = []
    for project_space in project_space_list:
        flag = False
        for temp in filter_upload_dir():
            if temp in project_space["project_space"]:
                flag = True
                break
        if not flag:
            continue
        for file_path in file_path_list:
            if project_space["project_space"] in file_path["file_path"]:
                file_name = "%s/%s/%s" % (login.get_user_id(), md5(project_space["git_branch"], project_space["project_space"]),
                                            file_path["file_path"][file_path["file_path"]
                                          .find(os.path.basename(project_space["project_space"])):])
                file_name = file_name.replace("\\", "/")
                local_file_path = file_path["file_path"]
                temp_file = {"local_file_path": local_file_path, "file_name": file_name}
                upload_list.append(temp_file)
    upload_process(upload_list, bucket)


def upload_process(upload_list, bucket):
    global global_var
    cores = multiprocessing.cpu_count()
    with concurrent.futures.ThreadPoolExecutor(max_workers=cores) as executor, tqdm(desc="uploading", total=len(upload_list)) as progress:
        for index, file in enumerate(upload_list):
            executor.submit(uploading_file, file, bucket)
        time_count = 0
        addition = 0
        while True:
            time.sleep(1)
            time_count += 1
            progress.update(global_var - addition)
            addition = global_var
            if (global_var == len(upload_list) or global_var >= len(upload_list) - 20):
                break
            if time_count == 60:
                break

def uploading_file(file, bucket):
    global global_var
    local_file_path = file["local_file_path"]
    file_name = file["file_name"]
    logger.info(f"upload file ossUrl:{file_name} file local full path:{local_file_path}")
    bucket.upload_file(local_file_path, file_name)
    global_var += 1



def download_file(project_space):
    s3_secret = get_s3_secret()
    bucket_name = s3_secret["bucket"]
    aws_ak = s3_secret["ak"]
    aws_sk = s3_secret["sk"]
    aws_region = s3_secret["regionId"]
    s3 = boto3.resource('s3', region_name=aws_region, aws_access_key_id=aws_ak,
                        aws_secret_access_key=aws_sk)
    bucket = s3.Bucket(bucket_name)
    for file in project_space["changedFileList"]:
        ossURL = file["ossURL"]
        fileFullPath = file["fileFullPath"]
        try:
            bucket.download_file(ossURL, fileFullPath)
        except Exception:
            logger.info(f"this file sync fail  ossURL:{ossURL} fileFullPath:{fileFullPath}" )
        else:
            logger.info(f"this file sync success  ossURL:{ossURL} fileFullPath:{fileFullPath}")

def save_workspace(workspace_path, project_list):
    url = "%s%s" % (daemon_network, "/workspace/add")
    post_param = {"userId": login.get_user_id(), "fileDirectory": workspace_path, "projectSpaceList": project_list}
    return post_data(url, post_param)


def pull_workspace(workspace, project_list):
    url = "%s%s" % (daemon_network, "/workspace/getChangedFiles")
    post_param = {"userId": login.get_user_id(), "fileDirectory": workspace,"projectSpaceList": project_list}
    return post_data(url, post_param)


def post_data(url, params):
    headers = {"content-type": "application/json"}
    logger.info(f'request url:{url} params:{params}')
    response = requests.post(url, headers=headers, data=json.dumps(params))
    logger.info(f"response status_code: {response.status_code} text: {response.text} \n content:{response.content}")
    if response.status_code == 200:
        response_data = json.loads(response.text)["data"]
        return response_data
    return {}


def md5(git_branch, project_space):
    string = "%s%s" % (git_branch, project_space)
    hash_object = hashlib.md5(string.encode())
    md5_hash = hash_object.hexdigest()
    return md5_hash


def filter_upload_dir():
    return ["ecus", "platform"]

def get_s3_secret():
    url = "%s%s" % (daemon_network, "/file/config")
    headers = {"content-type": "application/json"}
    logger.info(f'request url:{url}')
    response = requests.post(url, headers=headers, data=json.dumps({}))
    if response.status_code == 200:
        response_data = json.loads(response.text)["data"]
        return response_data
    return {}
