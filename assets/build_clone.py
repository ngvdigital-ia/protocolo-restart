from __future__ import annotations

from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parent.parent
SOURCE = (ROOT / "_reference" / "source.html").read_text(encoding="utf-8")
CHECKOUT = "https://pay.meurestart.com/pay/protocolo-restart-cademi?utm_content=&amp;utm_source=organic&amp;utm_campaign=&amp;utm_medium=&amp;utm_term=&amp;src=v3_0b4f6398-8dd6-44de-a57c-4ecac48dfe02_69c40e10717734693ca14dad_10_t-12_h-4_s-4"
VENDOR_CSS = (
    "elementor-frontend.css", "elementor-kit-9.css", "elementor-animation-grow.css",
    "elementor-heading.css", "elementor-image.css", "elementor-icon-list.css",
    "elementor-toggle.css", "elementor-page-213.css", "eael-general.css",
)


def element_texts(html: str, tag: str) -> list[str]:
    return [re.sub(r"<[^>]+>", "", item).strip() for item in re.findall(rf"<{tag}[^>]*>([\s\S]*?)</{tag}>", html, re.I) if re.sub(r"<[^>]+>", "", item).strip()]


def localized_body(locale: str) -> str:
    old = subprocess.check_output(["git", "show", f"HEAD^:{locale}/index.html"], cwd=ROOT).decode("utf-8")
    body = re.search(r"<body[^>]*>([\s\S]*?)</body>", SOURCE, re.I).group(1)
    # The captured document is data, not executable code: retain only the rendered Elementor tree.
    body = re.sub(r"<script[\s\S]*?</script>", "", body, flags=re.I)
    # The source PixelYourSite fallback is a tracker and would add a non-content image.
    body = re.sub(r"<noscript[\s\S]*?</noscript>", "", body, flags=re.I)
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
    # Required locale/checkout adaptation: retain the source offer geometry, never BRL.
    if locale == "FR":
        prices = {
            "Valor: <del>R$ 267,00</del>": "Valeur : <del>$267.00</del>",
            "Valor: <del>R$ 147,00</del>": "Valeur : <del>$147.00</del>",
            "Valor: R$ 1.970,00": "Valeur : $1,970.00",
            "Valor: R$ 267,00": "Valeur : $267.00",
            "Valor: R$ 147,00": "Valeur : $147.00",
            "De: ": "Avant : ",
            "R$ 2.384,00": "$2,384.00",
            "R$</span>29<span": "$</span>67<span",
            "Ou à vista por R$ 297,00": "Ou en un paiement de $67.00",
        }
    else:
        prices = {
            "Valor: <del>R$ 267,00</del>": "Value: <del>$267.00</del>",
            "Valor: <del>R$ 147,00</del>": "Value: <del>$147.00</del>",
            "Valor: R$ 1.970,00": "Value: $1,970.00",
            "Valor: R$ 267,00": "Value: $267.00",
            "Valor: R$ 147,00": "Value: $147.00",
            "De: ": "Was: ",
            "R$ 2.384,00": "$2,384.00",
            "R$</span>29<span": "$</span>67<span",
            "Ou à vista por R$ 297,00": "Or one payment of $67.00",
        }
    for before, after in prices.items():
        body = body.replace(before, after)
    body = re.sub(
        r"(<h5[^>]*>)[\s\S]*?(</h5>)",
        r'\1<span style="font-size: 50px">$</span>67\2',
        body,
        count=1,
        flags=re.I,
    )
    return "\n".join(line.rstrip() for line in body.splitlines())


def build(locale: str, language: str) -> None:
    styles = "\n".join(re.findall(r"<style[^>]*>([\s\S]*?)</style>", SOURCE, re.I))
    # The captured theme embeds these remote faces; Manrope is provided locally by site.css.
    styles = re.sub(r"@font-face\{[^}]*\}\s*", "", styles)
    body = localized_body(locale)
    body_tag = re.search(r"(<body[^>]*>)", SOURCE, re.I).group(1)
    css_links = "\n".join(f'<link rel="stylesheet" href="../assets/vendor/{name}">' for name in VENDOR_CSS)
    page = f'''<!doctype html>
<html lang="{language}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="Protocol Restart"><title>Protocol Restart</title>
{css_links}
<link rel="stylesheet" href="../assets/site.css"><style>{styles}</style></head>{body_tag}{body}<script src="../assets/site.js" defer></script></body></html>'''
    (ROOT / locale / "index.html").write_text("\n".join(line.rstrip() for line in page.splitlines()) + "\n", encoding="utf-8")


build("EN", "en")
build("FR", "fr")
