import os
import re
from datetime import datetime
from pathlib import Path
from urllib.parse import urljoin, urlparse

from mkdocs.config.defaults import MkDocsConfig
from mkdocs.plugins import event_priority
from mkdocs_exporter.formats.pdf.aggregator import Aggregator
from mkdocs_exporter.formats.pdf.preprocessor import Preprocessor
from mkdocs_exporter.formats.pdf.renderer import Renderer
from mkdocs_exporter.page import Page as ExporterPage


class StateHandler:
    has_exporter = False
    debug = False
    rewrite_png_to_webp = True
    replace_placeholder = True
    fix_pages_indexes = True


class PassAlong:
    pdf_date = datetime.now().strftime("%Y-%m-%d")
    replace_map: dict = {}


@event_priority(100)
def on_config(config: MkDocsConfig):

    StateHandler.has_exporter = "exporter-pdf" in config.plugins
    StateHandler.debug = os.getenv("DEBUG_PDF", "False").lower().strip() in [
        "true",
        "1",
    ]
    PassAlong.replace_map.clear()

    if not StateHandler.has_exporter:
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
def on_page_markdown(markdown, page: ExporterPage, config, files):

    if not StateHandler.has_exporter:
        return

    prefixes = (
        "features",
    )

    src_uri: str = page.file.src_uri

    if not src_uri.startswith(prefixes):
        return

    page.meta["pdf"] = True

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

    def wrapper(self: Renderer, page: ExporterPage, disable: list = []) -> str:

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
