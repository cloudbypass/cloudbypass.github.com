"""Check the shared documentation before either repository uploads its Pages site.

The mirror uses the source repository's checker. Only the packaged CNAME differs;
API and console domains remain specific to the language of each guide.
"""

import argparse
import ast
from collections import Counter
import json
from pathlib import Path
import re
from urllib.parse import parse_qs, unquote, urlsplit


def require(condition, message):
    if not condition:
        raise ValueError(message)


def error_codes(text):
    return re.findall(r"^\|\s*([A-Z][A-Z_]+)\s*\|", text, re.M)


def validate(site, domain):
    for relative in [
        "index.html", "CNAME", "static/docs-layout.js", "static/docs-layout.css",
        "zh-cn/vibe_coding.md", "us-en/vibe_coding.md",
        "zh-cn/response_data.md", "us-en/response_data.md",
    ]:
        path = site / relative
        require(path.is_file() and path.stat().st_size > 0, "Missing or empty file: " + relative)

    require((site / "CNAME").read_text(encoding="utf-8").strip() == domain,
            "Packaged CNAME must belong to this deployment: " + domain)

    summaries = []
    for language, api_host, docs_host, console_host in [
        ("zh-cn", "api.cloudbypass.com", "docs.cloudbypass.com", "console.cloudbypass.com"),
        ("us-en", "api.scrapingbypass.com", "docs.scrapingbypass.com", "console.scrapingbypass.com"),
    ]:
        guide = (site / language / "vibe_coding.md").read_text(encoding="utf-8")
        reference = (site / language / "response_data.md").read_text(encoding="utf-8")
        require("\ufffd" not in guide + reference, "Invalid text encoding: " + language)
        blocks = re.findall(r"^```([^\n]*)\n(.*?)^```\s*$", guide, re.M | re.S)
        require(len(blocks) * 2 == guide.count("```"), "Unclosed code fence: " + language)
        require(sum(kind == "python" for kind, _ in blocks) == 3,
                "Keep the request, Turnstile, and download examples: " + language)
        for kind, body in blocks:
            if kind == "python":
                ast.parse(body)
            elif kind == "json":
                json.loads(body)

        examples = "\n".join(body for kind, body in blocks if kind in {"python", "json"})
        hosts = set(re.findall(r"\bapi\.(?:cloudbypass|scrapingbypass)\.com\b", examples))
        require(hosts == {api_host}, "Unexpected API hostname in " + language + ": " + repr(hosts))
        require("https://" + docs_host + "/" + language + "/vibe_coding.md" in guide,
                "Missing localized guide URL: " + language)
        require("https://" + console_host in guide, "Missing localized console URL: " + language)

        codes = error_codes(reference)
        require(len(codes) == len(set(codes)), "Duplicate error-code rows: " + language)
        codes = set(codes) - {"CODE", "PARAMETER"}
        mentioned = set(re.findall(r"`([A-Z][A-Z_]+)`", guide))
        variables = set(re.findall(r"\bCLOUDBYPASS_[A-Z]+\b", guide))
        variables.update({"TARGET_URL", "CB_VERSION", "HTTP_PROXY", "HTTPS_PROXY", "YOUR_API_KEY"})
        require(not (mentioned - codes - variables),
                "Error codes missing from the reference in " + language + ": "
                + repr(sorted(mentioned - codes - variables)))
        require("`SSL_CONNECT_ERROR`" in guide and "`SSL_ERROR`" not in guide,
                "Use the documented SSL error code: " + language)

        for text in [guide, reference]:
            for link in re.findall(r"\]\((/[^)]+)\)", text):
                url = urlsplit(link)
                target = site / unquote(url.path).lstrip("/")
                if not target.is_file():
                    target = target.with_suffix(".md")
                require(target.is_file(), "Missing document linked from " + language + ": " + link)
                if target.name == "vibe_coding.md" and url.query:
                    anchor = parse_qs(url.query).get("id", [""])[0]
                    headings = re.findall(r"^#{1,6} (.+)", guide, re.M)
                    require(anchor in [heading.lower().replace(" ", "-") for heading in headings],
                            "Missing navigation anchor: " + link)

        summaries.append({
            "sections": len(re.findall(r"^## ", guide, re.M)),
            "blocks": Counter(kind for kind, _ in blocks),
            "headers": set(re.findall(r"\bx-cb-[a-z-]+\b", guide)),
            "variables": variables,
            "mentioned_codes": mentioned - variables,
            "reference_codes": codes,
        })
    require(summaries[0] == summaries[1], "Chinese and English guide coverage differs")
    print("Validated " + domain + ": package, localized domains, links, examples, and bilingual coverage")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("site", type=Path, help="Root of the packaged Pages artifact")
    parser.add_argument("--domain", required=True,
                        choices=["docs.cloudbypass.com", "docs.scrapingbypass.com"])
    args = parser.parse_args()
    try:
        validate(args.site, args.domain)
    except (ValueError, SyntaxError, OSError) as error:
        parser.exit(1, "Documentation validation failed: " + str(error) + "\n")
