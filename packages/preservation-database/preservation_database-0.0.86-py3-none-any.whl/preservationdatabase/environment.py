import logging


def setup_environment(
    code_bucket, download_settings=True, verbose=False
) -> None:
    """
    Initialize the Django ORM environment.
    :param code_bucket: the S3 bucket where the code and settings are stored.
    :param download_settings: whether to download the settings file from S3.
    :param verbose: whether to log to the console.
    :return: None
    """
    import os
    import sys
    import inspect
    from pathlib import Path

    from rich.console import Console
    from rich.logging import RichHandler

    logging.basicConfig(
        level=logging.INFO,
        format="%(message)s",
        datefmt="[%X]",
        handlers=[RichHandler(console=Console(stderr=True))],
    )
    log = logging.getLogger("preservation-database")
    log.setLevel(logging.INFO)

    logging.getLogger("boto3").setLevel(logging.WARNING)
    logging.getLogger("botocore").setLevel(logging.WARNING)

    current_directory = os.path.dirname(
        os.path.abspath(inspect.getfile(inspect.currentframe()))
    )

    if download_settings:
        settings_file = Path(current_directory) / "downloaded_settings.py"

        if verbose:
            logging.info(
                "Settings file downloading to: " "{}".format(settings_file)
            )

        import boto3

        s3client = boto3.client("s3")
        s3client.download_file(code_bucket, "settings.py", str(settings_file))

    if code_bucket:
        sys.path.append(current_directory)
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "downloaded_settings")

    import django

    django.setup()
