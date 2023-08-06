class FileConfig:
    def __init__(self, uri, file_format, timestamp_field):
        self.uri = uri
        self.file_format = file_format
        self.timestamp_field = timestamp_field


class BatchSource:
    def __init__(self, name, batch_config):
        self.name = name
        self.batch_config = batch_config


def create_batch_source(name, uri, file_format, timestamp_field):
    file_config = FileConfig(uri=uri, file_format=file_format, timestamp_field=timestamp_field)
    batch_source = BatchSource(name=name, batch_config=file_config)
    return batch_source
