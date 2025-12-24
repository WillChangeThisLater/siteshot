import math
import subprocess
import sys
import tempfile
from pathlib import Path
from urllib.parse import urlparse

from playwright.sync_api import sync_playwright

import llm


@llm.hookimpl
def register_fragment_loaders(register):
    register("siteshot", siteshot)


VIEWPORT = {"width": 1280, "height": 900}


def ensure_chromium() -> None:
    try:
        subprocess.run(
            [sys.executable, "-m", "playwright", "install", "chromium"],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
    except subprocess.CalledProcessError:
        raise RuntimeError(
            "Playwright could not download Chromium. Please run 'playwright install chromium' manually."
        )


def _normalize_argument(argument: str) -> str:
    if argument.startswith("siteshot-frames:"):
        argument = argument.split(":", 1)[1]
    argument = argument.strip()
    if not argument:
        raise ValueError("No URL provided to siteshot")

    parsed = urlparse(argument)
    if not parsed.scheme:
        argument = f"https://{argument}"
    return argument


def capture_screenshots(url: str, out_dir: Path, viewport_height: int = 900) -> list[Path]:
    ensure_chromium()

    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        page = browser.new_page(viewport=VIEWPORT)
        page.goto(url)
        page.wait_for_timeout(2000)

        scroll_height = page.evaluate("() => document.body.scrollHeight")
        if not scroll_height:
            scroll_height = viewport_height

        step = viewport_height
        num_screenshots = math.ceil(scroll_height / step)

        captured = []
        for index in range(num_screenshots):
            scroll_y = index * step
            page.evaluate("(y) => window.scrollTo(0, y)", scroll_y)
            page.wait_for_timeout(1000)
            output_path = out_dir / f"screenshot_{index}.png"
            page.screenshot(path=str(output_path))
            captured.append(output_path)

        browser.close()

    return captured


def siteshot(argument: str):
    """Capture tiled screenshots of the provided URL and return them as attachments."""

    url = _normalize_argument(argument)
    temp_dir = Path(tempfile.mkdtemp(prefix="siteshot_"))
    files = capture_screenshots(url, temp_dir, viewport_height=VIEWPORT["height"])
    attachments = [llm.Attachment(path=str(path)) for path in files]
    return attachments
