class SafeTensorError(RuntimeError):
    pass


class SafeTensorHeaderError(SafeTensorError):
    pass


class SafeTensorEmptyFileError(SafeTensorError):
    pass
