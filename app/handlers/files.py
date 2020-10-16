import os

from werkzeug.utils import secure_filename

from flask import send_from_directory, send_file
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

    def show(self, file):
        return send_from_directory(self.folder, file.path)

    def download(self, file):
        return send_file(file.path, attachment_filename=file.name,)


class AWSFileHandler(FileHandler):
    def __init__(self):
        self.s3 = boto3.client(
            "s3",
            aws_access_key_id=app.config["AWS_ACCESS_KEY_ID"],
            aws_secret_access_key=app.config["AWS_SECRET_ACCESS_KEY"],
        )
        self.BUCKET = "ketocalc"
        self.folder = os.path.join(app.root_path, "files/")

    def save(self, file):
        FileHandler().save(file)
        self.upload_file(os.path.join(self.folder, file.path), file.name)

    def show(self, file):
        pass

    def download(self, file):
        pass

    def upload_file(self, file_path, file_name):
        """
        Function to upload a file to an S3 bucket
        """
        s3_client = boto3.client("s3")
        response = s3_client.upload_file(file_path, self.BUCKET, file_name)

        print(response)

        return response

    def download_file(self, file_name):
        """
        Function to download a given file from an S3 bucket
        """
        s3 = boto3.resource("s3")
        output = f"downloads/{file_name}"
        s3.Bucket(self.BUCKET).download_file(file_name, output)

        return output

    def list_files(self):
        """
        Function to list files in a given S3 bucket
        """
        s3 = boto3.client("s3")
        contents = []
        try:
            for item in s3.list_objects(Bucket=self.BUCKET)["Contents"]:
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
        s3_client = boto3.client("s3", region_name="eu-west-3")
        object_name = file.path
        try:
            response = s3_client.generate_presigned_url(
                "get_object",
                Params={"Bucket": self.BUCKET, "Key": object_name},
                ExpiresIn=expiration,
            )
        except ClientError:
            return None

        # The response contains the presigned URL
        return response
