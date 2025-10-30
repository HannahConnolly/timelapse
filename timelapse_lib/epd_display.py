"""Safe Waveshare e-Paper display helper.

This module tries to use a Waveshare e-paper driver if available and exposes
simple functions to show a short message or an error on the display. If no
driver or PIL is installed, the functions silently no-op (so the rest of the
program keeps working on headless/dev machines).

The implementation attempts to import common Waveshare driver modules. It
creates a black/white PIL image sized to the display and draws the provided
text, truncating to fit.
"""
from typing import Optional
import textwrap
import traceback
import os
import time

try:
    from PIL import Image, ImageDraw, ImageFont
    _has_pil = True
except Exception:
    Image = ImageDraw = ImageFont = None
    _has_pil = False

# Try importing common Waveshare driver module names.
_epd = None
_epd_name = None
_MODULE_CANDIDATES = (
    # common names used by Waveshare and forks; include both plain and
    # package-prefixed names to match different installation layouts.
    "waveshare_epd.epd2in13_V2",
    "waveshare_epd.epd2in13",
    "waveshare_epd.epd2in7",
    "waveshare_epd.epd2in7b",
    "waveshare_epd.epd2in7_V2",
    # some installs expose module directly as epd2in7_V2 / epd2in7
    "epd2in7_V2",
    "epd2in7",
    "epd2in7b",
    "waveshare_epd",
)

# simple opt-in debug logging (set TIMELAPSE_EPD_DEBUG=1 in the environment)
_DEBUG = os.getenv("TIMELAPSE_EPD_DEBUG", "0") in ("1", "true", "True")
_DEBUG_LOG = "/tmp/epd_debug.log"


def _log_debug(msg: str):
    if not _DEBUG:
        return
    try:
        with open(_DEBUG_LOG, "a") as f:
            f.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} {msg}\n")
    except Exception:
        # never raise from logging
        pass

for mod in _MODULE_CANDIDATES:
    try:
        m = __import__(mod, fromlist=["EPD"])
        _epd = m
        _epd_name = mod
        break
    except Exception:
        _epd = None

_log_debug(f"PIL available: {_has_pil}; selected epd module: {_epd_name}")


def _create_image(width: int, height: int):
    if not _has_pil:
        return None
    # 1-bit image (mode '1') for black/white e-paper
    return Image.new('1', (width, height), 255)


def _draw_text_on_image(img, lines, font=None, margin=4):
    if img is None or not _has_pil:
        return None
    draw = ImageDraw.Draw(img)
    w, h = img.size
    y = margin
    for line in lines:
        draw.text((margin, y), line, font=font, fill=0)
        # advance by line height (approx)
        if font:
            y += font.getsize(line)[1] + 2
        else:
            y += 12
        if y > h - margin:
            break
    return img


def _get_font(size=14):
    if not _has_pil:
        return None
    try:
        return ImageFont.load_default()
    except Exception:
        return None


def show_message(title: str, body: Optional[str] = None, timeout_s: int = 5):
    """Display a short message (title + optional body) on the e-paper display.

    This function is safe to call even when the driver or PIL isn't installed.
    It will silently do nothing in that case.
    """
    lines = []
    if title:
        lines.append(title)
    if body:
        # wrap body to reasonable width
        wrapped = textwrap.wrap(body, width=30)
        lines.extend(wrapped[:10])

    # If we have an actual waveshare driver module, attempt to use it.
    try:
        if _epd is not None:
            # many drivers expose a class like epd2in13_V2.EPD with init/clear/display
            # fall back to module-level functions if necessary.
            epd = None
            if hasattr(_epd, 'EPD'):
                try:
                    epd = _epd.EPD()
                except Exception:
                    # some driver packages define helper functions at module level
                    epd = _epd
            else:
                # some packages expose init functions at module level
                epd = _epd

            _log_debug(f"Using epd module: {_epd_name}, epd object: {type(epd)}")

            # try to establish width/height. prefer lowercase attributes, then
            # uppercase constants used by some drivers. fall back to sensible
            # defaults for small e-paper displays.
            width = (
                getattr(epd, 'width', None)
                or getattr(epd, 'WIDTH', None)
                or getattr(epd, 'EPD_WIDTH', None)
                or 250
            )
            height = (
                getattr(epd, 'height', None)
                or getattr(epd, 'HEIGHT', None)
                or getattr(epd, 'EPD_HEIGHT', None)
                or 122
            )

            # initialize the display if possible
            if hasattr(epd, 'init'):
                try:
                    epd.init()
                except Exception:
                    pass

            # create image and draw text
            img = _create_image(width, height)
            font = _get_font()
            _draw_text_on_image(img, lines, font=font)

            # many drivers require passing a framebuffer produced by
            # epd.getbuffer(image). Try that first if available.
            tried = False
            if hasattr(epd, 'getbuffer') and hasattr(epd, 'display'):
                try:
                    buf = epd.getbuffer(img)
                    epd.display(buf)
                    tried = True
                    _log_debug("Used epd.getbuffer() + epd.display()")
                except Exception:
                    tried = False

            # fallback: try passing the PIL image directly (some wrappers accept it)
            if not tried and hasattr(epd, 'display'):
                try:
                    epd.display(img)
                    tried = True
                    _log_debug("Used epd.display(img)")
                except Exception:
                    # try alternate API used in some drivers: display(image1, image2)
                    try:
                        epd.display(img, img)
                        tried = True
                        _log_debug("Used epd.display(img, img)")
                    except Exception:
                        tried = False

            # older drivers sometimes expose a display_frame API
            if not tried and hasattr(epd, 'display_frame'):
                try:
                    epd.display_frame(img)
                    tried = True
                    _log_debug("Used epd.display_frame(img)")
                except Exception:
                    tried = False

            # optional clear or sleep for a clean update
            if hasattr(epd, 'Clear'):
                try:
                    # some drivers expect a numeric argument for color
                    epd.Clear(0xFF)
                except Exception:
                    try:
                        epd.Clear()
                    except Exception:
                        pass
            elif hasattr(epd, 'clear'):
                try:
                    epd.clear()
                except Exception:
                    pass

            if hasattr(epd, 'sleep'):
                try:
                    epd.sleep()
                except Exception:
                    pass

            return
    except Exception:
        # never raise from display helper
        return

    # If no hardware driver available but we have PIL, save a file for debugging
    if _has_pil:
        try:
            img = _create_image(400, 300)
            font = _get_font()
            _draw_text_on_image(img, lines, font=font)
            preview = '/tmp/timelapse_epd_preview.png'
            img.save(preview)
            _log_debug(f"Wrote preview image: {preview}")
        except Exception:
            pass


def show_error(exc: Exception):
    """Format an exception and show the first lines on the display.

    The full traceback will still be available in logs/stdout, but e-paper will
    show a short, readable message.
    """
    tb = traceback.format_exception_only(type(exc), exc)
    msg = ''.join(tb)
    # keep it short
    lines = textwrap.wrap(msg, width=30)
    show_message("Capture error:", '\n'.join(lines[:6]))
