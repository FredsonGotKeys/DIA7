#!/usr/bin/env python3
"""CLI para actualizar contactos, redes sociais e links de projectos no index.html.

Uso:
    python update_links.py --whatsapp "258846283051"
    python update_links.py --email "novo@email.com"
    python update_links.py --instagram "https://instagram.com/novo_user"
    python update_links.py --facebook "https://facebook.com/novo"
    python update_links.py --linkedin "https://linkedin.com/in/novo"
    python update_links.py --threads "https://threads.com/@novo"
    python update_links.py --project "SonhoEuropa" --url "https://sonhoeuropa.co.mz"
    python update_links.py --listar
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
    from rich.table import Table
except ImportError:  # pragma: no cover
    print("Erro: a biblioteca 'rich' não está instalada. Execute: pip install -r requirements.txt")
    sys.exit(1)

console = Console()

INDEX_FILE = Path(__file__).parent / "index.html"
BACKUP_FILE = Path(__file__).parent / "index.html.bak"

PHONE_PATTERN = re.compile(r"^\+?258[0-9]{9}$")

PROJECT_NAMES = [
    "SonhoEuropa",
    "Muianga Consultores",
    "ADIEP",
    "Mentoria Elite",
    "Michele e Banda",
    "Fundação Muianga",
    "Escola Seiva da Nação",
    "Muianga Carreiras",
]


def ler_html() -> str:
    """Lê o conteúdo de index.html em UTF-8.

    Returns:
        Conteúdo completo do ficheiro como string.

    Raises:
        SystemExit: se o ficheiro não existir.
    """
    if not INDEX_FILE.exists():
        console.print(Panel(f"[red]Ficheiro não encontrado: {INDEX_FILE}[/red]"))
        sys.exit(1)
    with open(INDEX_FILE, encoding="utf-8") as fh:
        return fh.read()


def criar_backup() -> None:
    """Cria uma cópia de segurança index.html.bak antes de qualquer escrita."""
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
    """Valida se uma string é um URL bem formado (http/https).

    Args:
        url: URL a validar.

    Returns:
        True se válido, False caso contrário.
    """
    try:
        resultado = urlparse(url)
        return bool(resultado.scheme in ("http", "https") and resultado.netloc)
    except ValueError:
        return False


def validar_telefone(numero: str) -> bool:
    """Valida um número de telefone moçambicano no formato +258XXXXXXXXX.

    Args:
        numero: Número de telefone a validar (com ou sem '+').

    Returns:
        True se corresponder ao padrão esperado.
    """
    return bool(PHONE_PATTERN.match(numero))


def actualizar_whatsapp(html: str, numero: str) -> str:
    """Substitui todas as ocorrências do número/link de WhatsApp.

    Args:
        html: Conteúdo actual do index.html.
        numero: Novo número no formato 258XXXXXXXXX (sem '+').

    Returns:
        HTML actualizado.
    """
    numero_limpo = numero.lstrip("+")
    if not validar_telefone(numero_limpo):
        console.print(Panel(f"[red]Número inválido: {numero}. Esperado formato +258XXXXXXXXX[/red]"))
        sys.exit(1)

    html = re.sub(
        r"https://wa\.me/258\d{9}(\?text=[^\"']*)?",
        lambda m: f"https://wa.me/{numero_limpo}{m.group(1) or ''}",
        html,
    )
    html = re.sub(r"tel:\+258\d{9}", f"tel:+{numero_limpo}", html)
    numero_formatado = f"+{numero_limpo[:3]} {numero_limpo[3:5]} {numero_limpo[5:8]} {numero_limpo[8:]}"
    html = re.sub(r"\+258\s?\d{2}\s?\d{3}\s?\d{4}(?=</span>\s*</a>)", numero_formatado, html, count=1)
    return html


def actualizar_email(html: str, email: str) -> str:
    """Substitui o endereço de email (mailto e texto visível).

    Args:
        html: Conteúdo actual do index.html.
        email: Novo endereço de email.

    Returns:
        HTML actualizado.
    """
    html = re.sub(r"mailto:[^\"']+", f"mailto:{email}", html)
    html = re.sub(r"<span>[\w.+-]+@[\w.-]+\.\w+</span>\s*</a>\s*<a class=\"pill\" href=\"https://wa\.me",
                  f"<span>{email}</span></a><a class=\"pill\" href=\"https://wa.me", html)
    return html


def actualizar_rede_social(html: str, rede: str, url: str) -> str:
    """Substitui o href de um botão de rede social específico.

    Args:
        html: Conteúdo actual do index.html.
        rede: Nome da rede (instagram, facebook, linkedin, threads).
        url: Novo URL do perfil.

    Returns:
        HTML actualizado.

    Raises:
        SystemExit: se o URL for inválido.
    """
    if not validar_url(url):
        console.print(Panel(f"[red]URL inválido para {rede}: {url}[/red]"))
        sys.exit(1)

    dominios = {
        "instagram": r"https://www\.instagram\.com/[^\"']+",
        "facebook": r"https://www\.facebook\.com/[^\"']+",
        "linkedin": r"https://www\.linkedin\.com/[^\"']+",
        "threads": r"https://www\.threads\.com/[^\"']+",
    }
    pattern = dominios[rede]
    novo_html, n = re.subn(pattern, url, html, count=1)
    if n == 0:
        console.print(Panel(f"[yellow]Aviso: nenhum link de {rede} foi encontrado para substituir.[/yellow]"))
    return novo_html


def actualizar_projecto(html: str, nome: str, url: str) -> str:
    """Actualiza o link de um card de projecto pelo nome visível.

    Args:
        html: Conteúdo actual do index.html.
        nome: Nome do projecto (deve corresponder ao <h3> no card).
        url: Novo URL de destino.

    Returns:
        HTML actualizado.

    Raises:
        SystemExit: se o URL for inválido ou o projecto não existir.
    """
    if not validar_url(url) and url != "#":
        console.print(Panel(f"[red]URL inválido: {url}[/red]"))
        sys.exit(1)

    if nome not in PROJECT_NAMES:
        console.print(Panel(f"[red]Projecto desconhecido: {nome}\nDisponíveis: {', '.join(PROJECT_NAMES)}[/red]"))
        sys.exit(1)

    # Cada card fecha no primeiro "</a>" que encontra, por isso o .*? não-guloso
    # nunca ultrapassa os limites do próprio card (evita cruzar para o card seguinte).
    card_pattern = re.compile(r'<a class="project-card".*?</a>', re.DOTALL)
    h3_pattern = re.compile(r"<h3>" + re.escape(nome) + r"</h3>")
    href_pattern = re.compile(r'(href=")([^"]*)(")')

    encontrado = False

    def substituir_card(match: re.Match) -> str:
        nonlocal encontrado
        card = match.group(0)
        if h3_pattern.search(card):
            encontrado = True
            return href_pattern.sub(lambda m: f"{m.group(1)}{url}{m.group(3)}", card, count=1)
        return card

    novo_html = card_pattern.sub(substituir_card, html)
    if not encontrado:
        console.print(Panel(f"[yellow]Aviso: não foi possível localizar o card do projecto '{nome}'.[/yellow]"))
    return novo_html


def listar_contactos(html: str) -> None:
    """Mostra uma tabela com os contactos e links actualmente presentes no HTML.

    Args:
        html: Conteúdo actual do index.html.
    """
    tabela = Table(title="Contactos e Links Actuais")
    tabela.add_column("Tipo", style="bold")
    tabela.add_column("Valor")

    whatsapp = re.search(r"https://wa\.me/[^\"']+", html)
    email = re.search(r"mailto:[^\"']+", html)
    telefone = re.search(r"tel:[^\"']+", html)
    instagram = re.search(r"https://www\.instagram\.com/[^\"']+", html)
    facebook = re.search(r"https://www\.facebook\.com/[^\"']+", html)
    linkedin = re.search(r"https://www\.linkedin\.com/[^\"']+", html)
    threads = re.search(r"https://www\.threads\.com/[^\"']+", html)

    campos = {
        "WhatsApp": whatsapp,
        "Email": email,
        "Telefone": telefone,
        "Instagram": instagram,
        "Facebook": facebook,
        "LinkedIn": linkedin,
        "Threads": threads,
    }

    for nome_campo, valor in campos.items():
        tabela.add_row(nome_campo, valor.group(0) if valor else "[dim]não encontrado[/dim]")

    console.print(tabela)

    tabela_proj = Table(title="Projectos")
    tabela_proj.add_column("Nome", style="bold")
    for nome in PROJECT_NAMES:
        tabela_proj.add_row(nome)
    console.print(tabela_proj)


def construir_parser() -> argparse.ArgumentParser:
    """Constrói o parser de argumentos da linha de comando.

    Returns:
        Parser configurado com todas as opções suportadas.
    """
    parser = argparse.ArgumentParser(
        description="Actualiza contactos e links no index.html da landing page de Fredson Muianga."
    )
    parser.add_argument("--whatsapp", help="Novo número de WhatsApp, ex: 258846283051")
    parser.add_argument("--email", help="Novo endereço de email")
    parser.add_argument("--instagram", help="Novo URL do Instagram")
    parser.add_argument("--facebook", help="Novo URL do Facebook")
    parser.add_argument("--linkedin", help="Novo URL do LinkedIn")
    parser.add_argument("--threads", help="Novo URL do Threads")
    parser.add_argument("--project", help="Nome do projecto a actualizar (usar com --url)")
    parser.add_argument("--url", help="Novo URL do projecto indicado em --project")
    parser.add_argument("--listar", action="store_true", help="Lista os contactos e projectos actuais")
    return parser


def main() -> None:
    """Ponto de entrada do script."""
    parser = construir_parser()
    args = parser.parse_args()

    if args.listar:
        html = ler_html()
        listar_contactos(html)
        return

    if args.project and not args.url:
        console.print(Panel("[red]--project requer --url[/red]"))
        sys.exit(1)

    houve_alteracao = any([
        args.whatsapp, args.email, args.instagram,
        args.facebook, args.linkedin, args.threads,
        (args.project and args.url),
    ])

    if not houve_alteracao:
        parser.print_help()
        return

    html = ler_html()
    criar_backup()

    if args.whatsapp:
        html = actualizar_whatsapp(html, args.whatsapp)
        console.print("[green]✓[/green] WhatsApp actualizado")

    if args.email:
        html = actualizar_email(html, args.email)
        console.print("[green]✓[/green] Email actualizado")

    if args.instagram:
        html = actualizar_rede_social(html, "instagram", args.instagram)
        console.print("[green]✓[/green] Instagram actualizado")

    if args.facebook:
        html = actualizar_rede_social(html, "facebook", args.facebook)
        console.print("[green]✓[/green] Facebook actualizado")

    if args.linkedin:
        html = actualizar_rede_social(html, "linkedin", args.linkedin)
        console.print("[green]✓[/green] LinkedIn actualizado")

    if args.threads:
        html = actualizar_rede_social(html, "threads", args.threads)
        console.print("[green]✓[/green] Threads actualizado")

    if args.project and args.url:
        html = actualizar_projecto(html, args.project, args.url)
        console.print(f"[green]✓[/green] Projecto '{args.project}' actualizado")

    guardar_html(html)
    console.print(Panel("[bold green]index.html actualizado com sucesso.[/bold green]"))


if __name__ == "__main__":
    main()
