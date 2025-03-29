import os
import re
from datetime import datetime
from pathlib import Path
from urllib.parse import urljoin, urlparse

from mkdocs.config.defaults import MkDocsConfig
from mkdocs.plugins import event_priority
from mkdocs_exporter.formats.pdf.aggregator import Aggregator
from mkdocs_exporter.formats.pdf.plugin import Plugin as ExporterPlugin
from mkdocs_exporter.formats.pdf.preprocessor import Preprocessor
from mkdocs_exporter.formats.pdf.renderer import Renderer
from mkdocs_exporter.page import Page as ExporterPage


class StateHandler:
    exporter_plugin: ExporterPlugin = None
    debug = False
    rewrite_png_to_webp = True
    replace_placeholder = True
    fix_pages_indexes = True
    process_metadata = True


class PassAlong:
    pdf_date = datetime.now().strftime("%Y-%m-%d")
    pdf_date_meta = datetime.now().strftime("D\072%Y%m%d%H%M%S")
    pdf_title_meta = None
    pdf_author_meta = None
    replace_map: dict = {}
    first_page_title = None

@event_priority(100)
def on_config(config: MkDocsConfig):

    StateHandler.exporter_plugin = config.plugins.get("exporter-pdf")
    StateHandler.debug = os.getenv("DEBUG_PDF", "False").lower().strip() in [
        "true",
        "1",
    ]
    PassAlong.replace_map.clear()
    PassAlong.first_page_title = None

    PassAlong.pdf_title_meta = config.site_name
    PassAlong.pdf_author_meta = config.site_author

    if not StateHandler.exporter_plugin:
        return

    if StateHandler.rewrite_png_to_webp:
        Preprocessor.rewrite_links = rewrite_links

    if StateHandler.replace_placeholder:
        PassAlong.replace_map = {
            "pdf_date": PassAlong.pdf_date,
        }
        Renderer.preprocess = wrap_renderer_preprocess(Renderer.preprocess)

    if StateHandler.fix_pages_indexes:
        Aggregator.preprocess = wrap_aggregator_preprocess(Aggregator.preprocess)

    if StateHandler.process_metadata:
        Aggregator.save = wrap_aggregator_save(Aggregator.save)

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
def on_page_markdown(markdown, page: ExporterPage, config: MkDocsConfig, files):

    if not StateHandler.exporter_plugin:
        return

    exporter_plugin = StateHandler.exporter_plugin

    prefixes = (
        "features",
    )

    src_uri: str = page.file.src_uri

    if exporter_plugin.config.explicit and not src_uri.startswith(prefixes):
        return

    page.meta["pdf"] = True

    if config.extra.get("first_page_title") is None:
        assert (
            PassAlong.first_page_title is None
        ), "first_page_title should be None here"
        PassAlong.first_page_title = page.title
        config.extra["first_page_title"] = page.title

    replace_map = page.formats["pdf"].get("replace_map") or {**PassAlong.replace_map}
    replace_map["page_title"] = page.title
    page.formats["pdf"]["replace_map"] = replace_map


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


def wrap_renderer_preprocess(func):

    pattern = r'"#\s*(.*?)\s*#"'

    def replacer(replace_map):

        def replace(match):
            placeholder = match.groups()[0]
            replacement = replace_map.get(placeholder)

            if replacement is None:
                raise RuntimeError(f"{placeholder} not in replace_map")

            return f'"{replacement}"'

        return replace

    def wrapper(self: Renderer, page: ExporterPage, disable: list = None) -> str:

        if disable is None:
            disable = []

        result: str = func(self, page, disable)

        sections = result.split("</head>")

        if "@page" in sections[0]:
            replace = replacer(page.formats["pdf"]["replace_map"])
            sections[0] = re.sub(pattern, replace, sections[0], flags=re.I)

        result = "</head>".join(sections)

        return result

    return wrapper


def wrap_aggregator_preprocess(func):

    def wrapper(self: Aggregator, page: ExporterPage) -> str:

        min_index = min(p.index for p in self.pages)

        for p in self.pages:
            p.index = p.index - min_index

        return func(self, page)

    return wrapper


def wrap_aggregator_save(func):
    """https://pypdf.readthedocs.io/en/stable/user/metadata.html#writing-metadata"""

    assert StateHandler.exporter_plugin
    exporter_plugin = StateHandler.exporter_plugin

    def wrapper(self, metadata=None) -> Aggregator:

        if metadata is None:
            metadata = {}

        # BUGFIX, the config meta data isn't properly passed
        metadata.update(exporter_plugin.config.aggregator.metadata)

        creation_date: str = metadata.get("/CreationDate")
        mod_date: str = metadata.get("/ModDate")
        pdf_title: str = metadata.get("/Title")
        pdf_author: str = metadata.get("/Author")
        pdf_creator: str = metadata.get("/Creator")
        pdf_subject: str = metadata.get("/Subject")

        if creation_date:
            metadata["/CreationDate"] = creation_date.format(
                hook=PassAlong.pdf_date_meta
            )

        if mod_date:
            metadata["/ModDate"] = mod_date.format(hook=PassAlong.pdf_date_meta)

        if pdf_title is None:
            metadata["/Title"] = PassAlong.pdf_title_meta

        if pdf_subject is None:
            if metadata["/Title"] != PassAlong.first_page_title:
                metadata["/Subject"] = PassAlong.first_page_title

        if pdf_author is None:
            metadata["/Author"] = PassAlong.pdf_author_meta

        if pdf_creator is None:
            metadata["/Creator"] = PassAlong.pdf_author_meta

        return func(self, metadata)

    return wrapper
