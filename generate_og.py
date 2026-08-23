#!/usr/bin/env python3
"""Gera e injecta meta tags Open Graph / Twitter Card no index.html após o deploy.

Uso:
    python generate_og.py --url "https://fredsonmuianga.co.mz" --image "https://fredsonmuianga.co.mz/og-image.png"
    python generate_og.py --preview
"""

from __future__ import annotations

import argparse
import re
import shutil
import sys
from pathlib import Path
from urllib.parse import urlparse

try:
    from rich.console import Console
    from rich.panel import Panel
except ImportError:  # pragma: no cover
    print("Erro: a biblioteca 'rich' não está instalada. Execute: pip install -r requirements.txt")
    sys.exit(1)

console = Console()

BASE_DIR = Path(__file__).parent
INDEX_FILE = BASE_DIR / "index.html"
BACKUP_FILE = BASE_DIR / "index.html.bak"
OG_IMAGE_HTML = BASE_DIR / "og-image.html"

OG_TITLE = "Fredson Muianga — Conselheiro · Consultor · Empresário · Filantropo"
OG_DESCRIPTION = (
    "Fundador da SonhoEuropa, Muianga Carreiras e ADIEP. "
    "Consultoria, Mentoria e Educação Digital em Maputo, Moçambique."
)

OG_TAG_PATTERN = re.compile(
    r'\s*<meta\s+(?:property="og:[^"]*"|name="twitter:[^"]*")[^>]*>\n?',
    re.IGNORECASE,
)


def ler_html() -> str:
    """Lê o conteúdo de index.html em UTF-8.

    Returns:
        Conteúdo completo do ficheiro.

    Raises:
        SystemExit: se o ficheiro não existir.
    """
    if not INDEX_FILE.exists():
        console.print(Panel(f"[red]Ficheiro não encontrado: {INDEX_FILE}[/red]"))
        sys.exit(1)
    with open(INDEX_FILE, encoding="utf-8") as fh:
        return fh.read()


def criar_backup() -> None:
    """Cria uma cópia de segurança index.html.bak antes de escrever."""
    try:
        shutil.copyfile(INDEX_FILE, BACKUP_FILE)
        console.print(f"[dim]Backup criado em {BACKUP_FILE.name}[/dim]")
    except OSError as exc:
        console.print(Panel(f"[red]Falha ao criar backup: {exc}[/red]"))
        sys.exit(1)


def guardar_html(conteudo: str) -> None:
    """Escreve o novo conteúdo em index.html em UTF-8.

    Args:
        conteudo: Novo conteúdo HTML a gravar.
    """
    try:
        with open(INDEX_FILE, "w", encoding="utf-8") as fh:
            fh.write(conteudo)
    except OSError as exc:
        console.print(Panel(f"[red]Falha ao gravar index.html: {exc}[/red]"))
        sys.exit(1)


def validar_url(url: str) -> bool:
    """Valida se uma string é um URL http/https bem formado.

    Args:
        url: URL a validar.

    Returns:
        True se válido.
    """
    try:
        resultado = urlparse(url)
        return bool(resultado.scheme in ("http", "https") and resultado.netloc)
    except ValueError:
        return False


def construir_meta_tags(site_url: str, image_url: str) -> str:
    """Constrói o bloco de meta tags Open Graph e Twitter Card.

    Args:
        site_url: URL público final do site.
        image_url: URL público da imagem de preview (1200x630).

    Returns:
        Bloco de tags HTML pronto para injectar.
    """
    return (
        '<meta property="og:type" content="profile">\n'
        f'<meta property="og:title" content="{OG_TITLE}">\n'
        f'<meta property="og:description" content="{OG_DESCRIPTION}">\n'
        f'<meta property="og:image" content="{image_url}">\n'
        '<meta property="og:image:width" content="1200">\n'
        '<meta property="og:image:height" content="630">\n'
        f'<meta property="og:url" content="{site_url}">\n'
        '<meta property="og:locale" content="pt_MZ">\n'
        '<meta property="og:site_name" content="Fredson Muianga">\n\n'
        '<meta name="twitter:card" content="summary_large_image">\n'
        f'<meta name="twitter:title" content="{OG_TITLE}">\n'
        f'<meta name="twitter:description" content="{OG_DESCRIPTION}">\n'
        f'<meta name="twitter:image" content="{image_url}">\n'
    )


def injectar_meta_tags(html: str, site_url: str, image_url: str) -> str:
    """Remove tags OG/Twitter existentes e injecta as novas após <meta charset>.

    Args:
        html: Conteúdo actual do index.html.
        site_url: URL final do site.
        image_url: URL da imagem OG.

    Returns:
        HTML actualizado com as novas meta tags.
    """
    html_sem_og = OG_TAG_PATTERN.sub("", html)

    novo_bloco = construir_meta_tags(site_url, image_url)

    charset_pattern = re.compile(r'(<meta charset="UTF-8">\n?)')
    if charset_pattern.search(html_sem_og):
        html_final = charset_pattern.sub(
            lambda m: m.group(1) + "\n" + novo_bloco + "\n", html_sem_og, count=1
        )
    else:
        html_final = html_sem_og.replace("<head>", f"<head>\n{novo_bloco}", 1)

    return html_final


def gerar_og_image_html(site_url: str) -> None:
    """Gera og-image.html: página 1200x630 para screenshot como imagem OG.

    Args:
        site_url: URL final do site (mostrado no rodapé da imagem).
    """
    conteudo = f"""<!DOCTYPE html>
<html lang="pt">
<head>
<meta charset="UTF-8">
<title>OG Image — Fredson Muianga</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Lora:ital@1&family=DM+Sans:wght@300;400;500&display=swap" rel="stylesheet">
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  html, body {{
    width: 1200px;
    height: 630px;
    background: #E9E2D3;
    font-family: 'DM Sans', sans-serif;
    overflow: hidden;
  }}
  .stage {{
    width: 1200px;
    height: 630px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
    padding: 0 80px;
  }}
  .avatar {{
    width: 140px;
    height: 140px;
    border-radius: 50%;
    background: #16332B;
    color: #E9E2D3;
    display: flex;
    align-items: center;
    justify-content: center;
    font-family: 'Bebas Neue', sans-serif;
    font-size: 3rem;
    margin-bottom: 32px;
  }}
  h1 {{
    font-family: 'Bebas Neue', sans-serif;
    font-size: 5rem;
    letter-spacing: 6px;
    color: #211A13;
    margin-bottom: 14px;
  }}
  p.tagline {{
    font-family: 'Lora', serif;
    font-style: italic;
    font-size: 1.7rem;
    color: #55483A;
    margin-bottom: 24px;
  }}
  p.footer {{
    font-size: 1.1rem;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: #93816D;
  }}
</style>
</head>
<body>
  <div class="stage">
    <div class="avatar">FM</div>
    <h1>FREDSON MUIANGA</h1>
    <p class="tagline">Conselheiro · Consultor · Empresário · Filantropo</p>
    <p class="footer">{site_url}</p>
  </div>
</body>
</html>
"""
    try:
        with open(OG_IMAGE_HTML, "w", encoding="utf-8") as fh:
            fh.write(conteudo)
        console.print(f"[green]✓[/green] {OG_IMAGE_HTML.name} gerado — abra num browser e tire um screenshot 1200x630 para usar como imagem OG.")
    except OSError as exc:
        console.print(Panel(f"[red]Falha ao gerar og-image.html: {exc}[/red]"))
        sys.exit(1)


def mostrar_preview(html: str) -> None:
    """Mostra no terminal as meta tags OG/Twitter actualmente presentes no HTML.

    Args:
        html: Conteúdo actual do index.html.
    """
    tags_encontradas = OG_TAG_PATTERN.findall(html)
    if not tags_encontradas:
        console.print(Panel("[yellow]Nenhuma meta tag Open Graph/Twitter encontrada em index.html.[/yellow]"))
        return

    matches = re.findall(r'<meta\s+(?:property="og:[^"]*"|name="twitter:[^"]*")[^>]*>', html)
    corpo = "\n".join(matches)
    console.print(Panel(corpo, title="Preview das Meta Tags Open Graph / Twitter"))


def construir_parser() -> argparse.ArgumentParser:
    """Constrói o parser de argumentos da linha de comando.

    Returns:
        Parser configurado.
    """
    parser = argparse.ArgumentParser(
        description="Gera e injecta meta tags Open Graph no index.html após o deploy."
    )
    parser.add_argument("--url", help="URL público final do site (ex: https://fredsonmuianga.co.mz)")
    parser.add_argument("--image", help="URL público da imagem OG (1200x630)")
    parser.add_argument("--preview", action="store_true", help="Mostra as meta tags actualmente presentes")
    return parser


def main() -> None:
    """Ponto de entrada do script."""
    parser = construir_parser()
    args = parser.parse_args()

    html = ler_html()

    if args.preview:
        mostrar_preview(html)
        return

    if not args.url or not args.image:
        console.print(Panel("[red]É necessário indicar --url e --image (ou usar --preview).[/red]"))
        parser.print_help()
        sys.exit(1)

    if not validar_url(args.url):
        console.print(Panel(f"[red]URL do site inválido: {args.url}[/red]"))
        sys.exit(1)

    if not validar_url(args.image):
        console.print(Panel(f"[red]URL da imagem inválido: {args.image}[/red]"))
        sys.exit(1)

    criar_backup()

    html_actualizado = injectar_meta_tags(html, args.url, args.image)
    guardar_html(html_actualizado)

    gerar_og_image_html(args.url)

    console.print(Panel(f"[bold green]Meta tags Open Graph actualizadas com site={args.url}[/bold green]"))


if __name__ == "__main__":
    main()
