"""
File Handlers

This classes are used to manage files.

Currently two types of storage are supported:
    - Local (via LocalFileHandler)
    - AWS (via AWSFileStorage)

    All (both) types should support following public methods:
    - save (expecting either apps File or werkzeug FileStorage)
    - delete (expecting File)
    - show (expecting File)
    - @property all_files
    - url


expects:
   - Files model for type checking (probably will find a way to change this)
   - Files controller (for generating url. don't know how to do this other way yet.)
"""

import os

from werkzeug.utils import secure_filename

from flask import send_from_directory
from flask import current_app as application

import boto3


class FileHandler(object):
    def __new__(self, **kwargs):
        if application.config["STORAGE_SYSTEM"] == "LOCAL":
            return LocalFileHandler(**kwargs)
        elif application.config["STORAGE_SYSTEM"] == "AWS":
            return AWSFileHandler(**kwargs)
        else:
            return LocalFileHandler(**kwargs)


class LocalFileHandler(object):
    def __init__(self, subfolder=None):
        self.folder = os.path.join(application.root_path, "files/")
        # create folder `files/` if doesn't exist
        if not os.path.exists(self.folder):
            os.makedirs(self.folder)
        if subfolder is not None:
            self.folder = os.path.join(self.folder, subfolder)
            # create folder `files/subfolder/` if doesn't exist
            if not os.path.exists(self.folder):
                os.makedirs(self.folder)

        # self.allowed_extension = {"txt", "pdf", "png", "jpg", "jpeg", "gif"}

    def save(self, file):
        """
        Arguments:
            file {[werkzeug.datastructures.FileStorage]}
        """
        file.full_name = secure_filename(file.name)

        file.save(self._get_full_path(file))

    def delete(self, file):
        """
        Arguments:
            file {app.models.File}
        """
        if os.path.exists(self._get_full_path(file)):
            os.remove(self._get_full_path(file))

    def show(self, file, thumbnail=False):
        if thumbnail:
            self.folder = os.path.join(self.folder, "thumbnails/")

        return send_from_directory(self.folder, file.path)

    def url(self, file, thumbnail=False):
        from flask import url_for

        return url_for("FilesView:show", hash_value=file.hash, thumbnail=True)

    @property
    def all_files(self):
        # TODO - list all files in folder
        return []

    def _get_full_path(self, file):
        # File.path or FileStorage.name
        name = getattr(file, "path", getattr(file, "name", None))
        return os.path.join(self.folder, name)

    # def download(self, file):
    #     return send_file(file.path, attachment_filename=file.name,)
    #


class AWSFileHandler(object):
    def __init__(self, subfolder=None):
        self.client = boto3.client(
            "s3",
            aws_access_key_id=application.config["AWS_ACCESS_KEY_ID"],
            aws_secret_access_key=application.config["AWS_SECRET_ACCESS_KEY"],
            region_name="eu-west-3",
        )

        self.resource = boto3.resource(
            "s3",
            aws_access_key_id=application.config["AWS_ACCESS_KEY_ID"],
            aws_secret_access_key=application.config["AWS_SECRET_ACCESS_KEY"],
            region_name="eu-west-3",
        )
        self.folder = os.path.join(application.root_path, "files/")

    def save(self, file):
        fh = FileHandler(subfolder="tmp")
        fh.save(file)
        self._upload_file(os.path.join(fh.folder, file.path), file.name)
        fh.delete(file)

    def _upload_file(self, file_path, file_name):
        """
        Function to upload a file to an S3 bucket
        """
        response = self.client.upload_file(
            file_path, application.config["BUCKET"], file_name
        )

        return response

    # def download_file(self, file_name):
    #     """
    #     Function to download a given file from an S3 bucket
    #     """
    #     output = file_name
    #     self.resource.Bucket(application.config["BUCKET"]).download_file(file_name, output)

    #     return output
    @property
    def all_files(self):
        from app.models.files import File

        aws_files = self._list_files()
        # TODO - match all aws_files to all files (probably composed from multiple models)
        files = []
        for file in aws_files:
            file = File().load_first_by_attribute("path", file["Key"])
            if file is not None and file.can_current_user_view:
                files.append(file)

    def _list_files(self):
        """
        Function to list files in a given S3 bucket
        """
        contents = []
        try:
            for item in self.client.list_objects(Bucket=application.config["BUCKET"])[
                "Contents"
            ]:
                contents.append(item)
        except Exception:
            return []

        return contents

    def url(self, file):
        return self._create_presigned_url(file)

    def _create_presigned_url(self, file, expiration=3600):
        from botocore.exceptions import ClientError

        """Generate a presigned URL to share an S3 object

        :param bucket_name: string
        :param object_name: string
        :param expiration: Time in seconds for the presigned URL to remain valid
        :return: Presigned URL as string. If error, returns None.
        """

        # Generate a presigned URL for the S3 object
        object_name = file.path
        try:
            response = self.client.generate_presigned_url(
                "get_object",
                Params={"Bucket": application.config["BUCKET"], "Key": object_name},
                ExpiresIn=expiration,
            )
        except ClientError:
            return None

        # The response contains the presigned URL
        return response


class ImageHandler(object):
    def create_and_save_thumbnail(self, file, size=(128, 128)):
        from PIL import Image

        image = Image.open(FileHandler()._get_full_path(file))
        image.thumbnail(size)
        image.name = file.name
        FileHandler(subfolder="thumbnails").save(image)

    def delete(self, file):
        FileHandler().delete(file)
        FileHandler(subfolder="thumbnails").delete(file)
