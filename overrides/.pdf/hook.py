import os
from datetime import datetime
from pathlib import Path
from urllib.parse import urljoin, urlparse

from mkdocs.config.defaults import MkDocsConfig
from mkdocs.plugins import event_priority
from mkdocs_exporter.formats.pdf.preprocessor import Preprocessor


class StateHandler:
    has_exporter = False
    debug = False
    rewrite_png_to_webp = True


class PassAlong:
    pdf_date = datetime.now().strftime("%Y-%m-%d")


@event_priority(100)
def on_config(config: MkDocsConfig):

    StateHandler.has_exporter = "exporter-pdf" in config.plugins
    StateHandler.debug = os.getenv("DEBUG_PDF", "False").lower().strip() in [
        "true",
        "1",
    ]

    if not StateHandler.has_exporter:
        return

    if StateHandler.rewrite_png_to_webp:
        Preprocessor.rewrite_links = rewrite_links

    # Create file:// protocol root for PDF templates
    # Using base "/assets" path resolves it based on the opened file
    # This leads to net::ERR_FILE_NOT_FOUND so we have to define the root manually
    # TODO For the plugin make a macros filter `file_url`
    root = Path(config.site_dir).as_posix().rstrip("/")
    config.extra["site_file_proto_root"] = f"file://{root}"

    # PDF creation date
    config.extra["pdf_date"] = PassAlong.pdf_date

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


@event_priority(-105)
def on_post_build(config: MkDocsConfig):
    if StateHandler.rewrite_png_to_webp:
        print(".png images got rewritten to .webp")


# Overrides


def rewrite_links(self, base: str, root: str) -> None:
    """Rewrite links based on the documentation's URL."""

    for element in self.html.find_all("a", href=True):
        url = urlparse(element["href"])

        if bool(url.netloc) or not url.path:
            continue

        final = urlparse(root)
        path = urljoin(base, url.path)

        new_url: str = url._replace(
            netloc=final.netloc, scheme=final.scheme, path=path
        ).geturl()

        if new_url.lower().endswith(".png"):
            new_url = new_url.rsplit(".", maxsplit=1)[0] + ".webp"

        element["href"] = new_url
