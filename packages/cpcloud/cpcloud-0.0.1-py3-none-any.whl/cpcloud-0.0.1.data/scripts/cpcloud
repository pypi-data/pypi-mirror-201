import os

import argparse
from tqdm import tqdm
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload
from googleapiclient.http import MediaIoBaseDownload

from mimetypes import guess_type

# If modifying these scopes, delete the file token.json.
SCOPES = [
    "https://www.googleapis.com/auth/drive",
    "https://www.googleapis.com/auth/drive.appdata",
    "https://www.googleapis.com/auth/drive.file",
]

credentials = {
    "installed": {
        "client_id": "800441787528-it01hk3lbo75isf8r5nuoj15c1aa2kro.apps.googleusercontent.com",
        "project_id": "cpcloud",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_secret": "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",
        "redirect_uris": ["http://localhost"],
    }
}


def get_credentials():
    creds = None

    TOKEN_FILE = os.path.join(os.path.expanduser("~"), ".cpcloud", "token.json")

    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_config(credentials, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        os.makedirs(os.path.dirname(TOKEN_FILE))
        with open(TOKEN_FILE, "w") as token:
            token.write(creds.to_json())
    return creds


def upload_file(source_path, directory_id, service):
    try:
        mimetype = guess_type(source_path, strict=False)[0]

        file_metadata = {
            "name": source_path,
            "mimeType": mimetype,
            "parents": [directory_id],
        }

        media = MediaFileUpload(
            source_path, chunksize=262144 * 20, mimetype=mimetype, resumable=True
        )

        request = service.files().create(
            body=file_metadata, media_body=media, fields="id"
        )

        response = None
        size = media.size()
        previous = 0
        with tqdm(
            total=size,
            unit="B",
            unit_scale=True,
            desc=f"Sending file {os.path.basename(source_path)}",
        ) as pbar:
            while response is None:
                status, response = request.next_chunk()
                if status:
                    current = status.progress() * size
                    pbar.update(current - previous)
                    previous = current

            pbar.update(size - previous)

    except Exception as e:
        print(e)


def download_file(file_id, file_name, service):
    try:
        size = int(service.files().get(fileId=file_id, fields="size").execute()["size"])

        request = service.files().get_media(fileId=file_id)

        previous = 0
        with tqdm(
            total=size,
            unit="B",
            unit_scale=True,
            desc=f"Downloading file {file_name}",
        ) as pbar:
            with open(file_name, "wb") as file:
                downloader = MediaIoBaseDownload(file, request, chunksize=262144 * 30)
                done = False
                while done is False:
                    status, done = downloader.next_chunk()
                    current = status.progress() * size
                    pbar.update(current - previous)
                    previous = current

        service.files().delete(fileId=file_id).execute()

    except HttpError as error:
        print(f"An error occurred: {error}")
        file = None


def directory_exists(directory_name, service):
    try:
        files = []
        found = False
        page_token = None
        directory_id = None

        while True:
            response = (
                service.files()
                .list(
                    q=f"name='{directory_name}'",
                    spaces="drive",
                    fields="nextPageToken, " "files(id, name)",
                    pageToken=page_token,
                )
                .execute()
            )

            for file in response.get("files", []):
                if file.get("name") == directory_name:
                    found = True
                    directory_id = file.get("id")

            files.extend(response.get("files", []))
            page_token = response.get("nextPageToken", None)
            if page_token is None:
                break

    except HttpError as error:
        print(f"An error ocurred: {error}")

    return found, directory_id


def get_files(directory_id, service):
    try:
        files = []
        page_token = None

        while True:
            response = (
                service.files()
                .list(
                    q=f"'{directory_id}' in parents",
                    spaces="drive",
                    fields="nextPageToken, " "files(id, name)",
                    pageToken=page_token,
                )
                .execute()
            )

            files.extend(response.get("files", []))
            page_token = response.get("nextPageToken", None)
            if page_token is None:
                break

    except HttpError as error:
        print(f"An error ocurred: {error}")

    return files


def create_directory(directory_name, service):
    try:
        file_metadata = {
            "name": directory_name,
            "mimeType": "application/vnd.google-apps.folder",
        }

        # pylint: disable=maybe-no-member
        file = service.files().create(body=file_metadata, fields="id").execute()
        return file.get("id")

    except HttpError as error:
        print(f"An error occurred: {error}")
        return None


def invalid_command():
    raise Exception("Invalid action")


def send_files(**args):
    creds = get_credentials()
    service = build("drive", "v3", credentials=creds)

    exists, directory_id = directory_exists("cpcloud", service)
    if not exists:
        directory_id = create_directory("cpcloud", service)

    for file in args["files"]:
        upload_file(file, directory_id, service)


def receive_files():
    creds = get_credentials()
    service = build("drive", "v3", credentials=creds)

    exists, directory_id = directory_exists("cpcloud", service)
    if exists:
        files = get_files(directory_id, service)

        for file in files:
            download_file(file.get("id"), file.get("name"), service)


def get_version():
    return "0.0.1"


def command_selector(command, **args):
    commands = {"send": send_files, "receive": receive_files, "version": get_version}

    command_fnc = commands.get(command, invalid_command)

    return command_fnc(**args)


def main():
    parser = argparse.ArgumentParser(
        description="Simple tool to copy files using Google Drive.",
        epilog="Enjoy it!",
    )

    subparsers = parser.add_subparsers(title="actions to perform", dest="command")

    send_parser = subparsers.add_parser("send", help="send files")
    send_parser.add_argument(nargs="+", dest="files")

    receive_parser = subparsers.add_parser("receive", help="receive files")

    parser.add_argument(
        "--version", action="version", version=f"cpcloud {get_version()}"
    )

    args = parser.parse_args()

    if args.command == None:
        parser.print_help()

    else:
        command_selector(**vars(args))


if __name__ == "__main__":
    main()
