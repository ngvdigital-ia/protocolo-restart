from __future__ import annotations

from html import unescape
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parent.parent
SOURCE = (ROOT / "_reference" / "source.html").read_text(encoding="utf-8")
CHECKOUT = "https://pay.meurestart.com/pay/protocolo-restart-cademi?utm_content=&amp;utm_source=organic&amp;utm_campaign=&amp;utm_medium=&amp;utm_term=&amp;src=v3_0b4f6398-8dd6-44de-a57c-4ecac48dfe02_69c40e10717734693ca14dad_10_t-12_h-4_s-4"


def element_texts(html: str, tag: str) -> list[str]:
    return [re.sub(r"<[^>]+>", "", item).strip() for item in re.findall(rf"<{tag}[^>]*>([\s\S]*?)</{tag}>", html, re.I) if re.sub(r"<[^>]+>", "", item).strip()]


def localized_body(locale: str) -> str:
    old = subprocess.check_output(["git", "show", f"HEAD^:{locale}/index.html"], cwd=ROOT).decode("utf-8")
    body = re.search(r"<body[^>]*>([\s\S]*?)</body>", SOURCE, re.I).group(1)
    # The captured document is data, not executable code: retain only the rendered Elementor tree.
    body = re.sub(r"<script[\s\S]*?</script>", "", body, flags=re.I)
    body = re.sub(r"<vturb-smartplayer[\s\S]*?</vturb-smartplayer>", '<div class="waiting-video" data-player-status="pending" aria-label="Video presentation pending"><span>◌</span><p>Video presentation coming soon</p></div>', body, flags=re.I)
    def local_image(match):
        tag = match.group(0)
        source = re.search(r'(?:src|srcset)=[\"\']([^\"\']+)', tag, re.I)
        if not source:
            return tag
        filename = source.group(1).split(",")[0].strip().split()[0].rsplit("/", 1)[-1]
        filename = re.sub(r"-\d+x\d+(?=\.webp)", "", filename)
        return f'<img src="../assets/images/{filename}" alt="">'
    body = re.sub(r"<img\b[^>]*>", local_image, body, flags=re.I)
    body = re.sub(r"href=[\"']https://pay\.meurestart\.com/pay/protocolo-restart-cademi[^\"']*[\"']", 'href="' + CHECKOUT + '" data-checkout', body)
    # Preserve the existing localized display copy for every heading/button where hierarchy aligns.
    for tag in ("h2", "h3"):
        values = element_texts(old, tag)
        it = iter(values)
        def replace(match):
            try:
                return match.group(1) + next(it) + match.group(3)
            except StopIteration:
                return match.group(0)
        body = re.sub(rf"(<{tag}[^>]*>)([\s\S]*?)(</{tag}>)", replace, body, flags=re.I)
    ctas = re.findall(r'<a[^>]*data-checkout[^>]*>([\s\S]*?)</a>', old, re.I)
    cta_values = [re.sub(r'<[^>]+>', '', x).strip() for x in ctas]
    it = iter(cta_values)
    def cta(match):
        try:
            return match.group(1) + next(it) + match.group(3)
        except StopIteration:
            return match.group(0)
    body = re.sub(r'(<a[^>]*data-checkout[^>]*>)([\s\S]*?)(</a>)', cta, body, flags=re.I)
    return "\n".join(line.rstrip() for line in body.splitlines())


def build(locale: str, language: str) -> None:
    styles = "\n".join(re.findall(r"<style[^>]*>([\s\S]*?)</style>", SOURCE, re.I))
    body = localized_body(locale)
    page = f'''<!doctype html>
<html lang="{language}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="Protocol Restart"><title>Protocol Restart</title>
<link rel="stylesheet" href="https://protocolorestart.com/wp-content/plugins/elementor/assets/css/frontend.min.css?ver=4.0.3">
<link rel="stylesheet" href="https://protocolorestart.com/wp-content/plugins/elementor/assets/css/widget-heading.min.css?ver=4.0.3">
<link rel="stylesheet" href="https://protocolorestart.com/wp-content/plugins/elementor/assets/css/widget-image.min.css?ver=4.0.3">
<link rel="stylesheet" href="https://protocolorestart.com/wp-content/plugins/elementor/assets/css/widget-icon-list.min.css?ver=4.0.3">
<link rel="stylesheet" href="https://protocolorestart.com/wp-content/plugins/elementor/assets/css/widget-toggle.min.css?ver=4.0.3">
<link rel="stylesheet" href="https://protocolorestart.com/wp-content/uploads/elementor/css/post-213.css?ver=1779816745">
<link rel="stylesheet" href="../assets/site.css"><style>{styles}</style></head><body><main>{body}</main><script src="../assets/site.js" defer></script></body></html>'''
    (ROOT / locale / "index.html").write_text("\n".join(line.rstrip() for line in page.splitlines()) + "\n", encoding="utf-8")


build("EN", "en")
build("FR", "fr")
