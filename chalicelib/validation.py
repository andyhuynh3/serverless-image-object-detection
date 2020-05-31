SUPPORTED_IMAGE_EXTENSIONS = (".jpg", ".png", ".jpeg")


def is_image(file_name: str) -> bool:
    return file_name.endswith(SUPPORTED_IMAGE_EXTENSIONS)
