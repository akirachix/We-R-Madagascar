from registry.utils.sheet_parse import parse_sheet


class Preprocessor:
    def __init__(self, file_path, user_id, content):
        self.file_path = file_path
        self.content = content
        self.user_id = user_id

    def parse(self):
        status, error = parse_sheet(self.file_path, self.user_id, self.content)
        return status, error
