import os
from datetime import datetime
from pathlib import Path

from mkdocs.plugins import event_priority


class StateHandler:
    has_exporter = False
    debug = False


def on_config(config):

    StateHandler.has_exporter = "exporter-pdf" in config.plugins
    StateHandler.debug = os.getenv("DEBUG_PDF", "False").lower().strip() in ["true", "1"]

    if not StateHandler.has_exporter:
        return

    # Create file:// protocol root for PDF templates
    # Using base "/assets" path resolves it based on the opened file
    # This leads to net::ERR_FILE_NOT_FOUND so we have to define the root manually
    # TODO For the plugin make a macros filter `file_url`
    root = Path(config.site_dir).as_posix().rstrip("/")
    config.extra["site_file_proto_root"] = f"file://{root}"

    # PDF creation date
    config.extra["pdf_date"] = datetime.now().strftime("%Y-%m-%d")

    # Add extra PDF css that needs to be part of the whole pdf context
    pdf_css = []

    if StateHandler.debug:
        pdf_css.append("assets/stylesheets/debug_pdf.css")

    for css in pdf_css:
        if (Path(config.docs_dir) / css).exists():
            config.extra_css.append(css)


@event_priority(100)
def on_page_markdown(markdown, page, config, files):

    if not StateHandler.has_exporter:
        return

    prefixes = (
        "features",
    )

    src_uri: str = page.file.src_uri

    if src_uri.startswith(prefixes):
        page.meta["pdf"] = True