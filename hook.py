import os
from pathlib import Path

from mkdocs.plugins import event_priority


def on_config(config):

    # Create file:// protocol root for PDF templates
    # Using base "/assets" path resolves it based on the opened file
    # This leads to net::ERR_FILE_NOT_FOUND so we have to define the root manually
    # TODO For the plugin make a macros filter `file_url`
    root = Path(config.site_dir).as_posix().rstrip("/")
    config.extra["site_file_proto_root"] = f"file://{root}"


@event_priority(100)
def on_page_markdown(markdown, page, config, files):

    prefixes = (
        "features",
    )

    src_uri: str = page.file.src_uri

    if src_uri.startswith(prefixes):
        page.meta["pdf"] = True