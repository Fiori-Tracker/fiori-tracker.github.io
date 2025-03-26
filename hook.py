from mkdocs.plugins import event_priority

@event_priority(100)
def on_page_markdown(markdown, page, config, files):

    prefixes = (
        "features",
    )

    src_uri: str = page.file.src_uri

    if src_uri.startswith(prefixes):
        page.meta["pdf"] = True