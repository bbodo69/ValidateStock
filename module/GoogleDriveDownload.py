import gdown


class GoogleDriveDownload:
    def __init__(self, file_id, output_name):
        google_path = 'https://drive.google.com/uc?id='
        self.file_id = file_id
        self.output_name = output_name
        gdown.download(google_path + self.file_id, self.output_name, quiet=False)