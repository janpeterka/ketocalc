import os

from werkzeug.utils import secure_filename

from flask import send_from_directory
from flask import current_app as app

import boto3


class FileHandler(object):
    """[summary]

    [description]

    requirements:
       - Files model
    """

    def __init__(self, subfolder=None):
        self.folder = os.path.join(app.root_path, "files/")
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
        """Save file to filesystem

        [description]

        Arguments:
            file {[app.models.files.File or werkzeug.datastructures.FileStorage]} --
        """
        from app.models.files import File

        if isinstance(file, File):
            file.data.name = file.name
            file = file.data

        file.name = secure_filename(file.name)

        full_path = os.path.join(self.folder, file.name)
        file.save(full_path)

    def delete(self, file):
        path = os.path.join(self.folder, file.path)
        if os.path.exists(path):
            os.remove(path)

    def show(self, file):
        return send_from_directory(self.folder, file.path)

    # def download(self, file):
    #     return send_file(file.path, attachment_filename=file.name,)


class AWSFileHandler(object):
    def __init__(self):
        self.client = boto3.client(
            "s3",
            aws_access_key_id=app.config["AWS_ACCESS_KEY_ID"],
            aws_secret_access_key=app.config["AWS_SECRET_ACCESS_KEY"],
            region_name="eu-west-3",
        )

        self.resource = boto3.resource(
            "s3",
            aws_access_key_id=app.config["AWS_ACCESS_KEY_ID"],
            aws_secret_access_key=app.config["AWS_SECRET_ACCESS_KEY"],
            region_name="eu-west-3",
        )
        self.folder = os.path.join(app.root_path, "files/")

    def save(self, file):
        fh = FileHandler(subfolder="tmp")
        fh.save(file)
        self.upload_file(os.path.join(fh.folder, file.path), file.name)
        fh.delete(file)

    def upload_file(self, file_path, file_name):
        """
        Function to upload a file to an S3 bucket
        """
        response = self.client.upload_file(file_path, app.config["BUCKET"], file_name)

        return response

    # def download_file(self, file_name):
    #     """
    #     Function to download a given file from an S3 bucket
    #     """
    #     output = file_name
    #     self.resource.Bucket(app.config["BUCKET"]).download_file(file_name, output)

    #     return output

    def list_files(self):
        """
        Function to list files in a given S3 bucket
        """
        contents = []
        try:
            for item in self.client.list_objects(Bucket=app.config["BUCKET"])[
                "Contents"
            ]:
                contents.append(item)
        except Exception:
            return []

        return contents

    def create_presigned_url(self, file, expiration=3600):
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
                Params={"Bucket": app.config["BUCKET"], "Key": object_name},
                ExpiresIn=expiration,
            )
        except ClientError:
            return None

        # The response contains the presigned URL
        return response
