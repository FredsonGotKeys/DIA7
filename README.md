# Fredson Muianga — Link-in-Bio

Landing page pessoal estilo "link-in-bio", estética editorial magazine,
para Fredson Muianga — Conselheiro, Consultor, Empresário e Filantropo moçambicano
baseado em Maputo.

## Estrutura de ficheiros

```
/
├── index.html         # Página principal (HTML + CSS + JS num único ficheiro)
├── foto.jpg            # Placeholder — substituir pela foto real
├── update_links.py     # CLI para actualizar contactos, redes sociais e projectos
├── generate_og.py      # Gera/injecta as meta tags Open Graph após deploy
├── requirements.txt    # Dependências Python
└── README.md
```

## 1. Pré-requisitos

- Python 3.10 ou superior
- Um browser moderno (Chrome, Safari, Firefox, Edge)

Instalar dependências:

```bash
pip install -r requirements.txt
```

## 2. Foto de perfil

O ficheiro `index.html` referencia `foto.jpg` no avatar — já incluído
na raiz do projecto com a foto real de Fredson Muianga (1080x1080px).
Para substituir por outra foto, basta gravar a nova imagem por cima de
`foto.jpg` (formato quadrado, mínimo 200x200px é recomendado). Caso o
ficheiro seja removido ou não carregue, o avatar mostra automaticamente
as iniciais "FM" sobre fundo verde escuro.

## 3. Ver a página localmente

Basta abrir `index.html` directamente no browser, ou servir com um
servidor local simples:

```bash
python -m http.server 8000
```

E aceder a `http://localhost:8000`.

## 4. Actualizar contactos e links (`update_links.py`)

Todos os comandos criam automaticamente um backup `index.html.bak`
antes de gravar qualquer alteração.

```bash
# Actualizar número de WhatsApp (formato 258XXXXXXXXX, sem espaços)
python update_links.py --whatsapp "258846283051"

# Actualizar email
python update_links.py --email "novo@email.com"

# Actualizar redes sociais
python update_links.py --instagram "https://www.instagram.com/novo_user"
python update_links.py --facebook "https://www.facebook.com/novo"
python update_links.py --linkedin "https://www.linkedin.com/in/novo"
python update_links.py --threads "https://www.threads.com/@novo"

# Actualizar o link de um projecto específico
python update_links.py --project "SonhoEuropa" --url "https://sonhoeuropapp.vercel.app/"

# Listar todos os contactos e projectos actualmente configurados
python update_links.py --listar
```

Projectos suportados por `--project`:
`SonhoEuropa`, `Muianga Consultores`, `ADIEP`, `Mentoria Elite`,
`Artes e Cultura`, `Fundação Muianga`, `Escola Seiva da Nação`,
`Muianga Carreiras`.

## 5. Gerar as meta tags Open Graph após o deploy (`generate_og.py`)

Depois de publicar o site (Vercel, Netlify, GitHub Pages, etc.), execute:

```bash
python generate_og.py --url "https://fredsonmuianga.co.mz" --image "https://fredsonmuianga.co.mz/og-image.png"
```

Isto:
1. Remove as meta tags Open Graph/Twitter antigas (com os placeholders).
2. Injecta as novas tags com o URL final do site e da imagem de preview.
3. Gera `og-image.html` — uma página de 1200x630px pronta para ser
   aberta no browser e capturada como screenshot (`og-image.png`), que
   deve depois ser publicada junto do site e apontada em `--image`.

Para ver as meta tags actualmente presentes sem alterar nada:

```bash
python generate_og.py --preview
```

## 6. Publicar o site (deploy)

Qualquer serviço de hosting estático funciona (não há backend nem
build step):

- **Vercel**: `vercel deploy` na pasta do projecto
- **Netlify**: arrastar a pasta para o painel, ou `netlify deploy`
- **GitHub Pages**: activar Pages no repositório apontando para a
  branch/pasta com o `index.html`

Depois do deploy, corra o passo 5 (`generate_og.py`) com o URL final
para que a partilha no WhatsApp, Instagram, Facebook e LinkedIn mostre
uma pré-visualização correcta.

## 7. Projectos e contactos reais já configurados

- **Telefone**: +258 84 628 3051 · +258 87 625 2006
- **Email**: minville@outlook.pt
- **WhatsApp**: https://wa.me/258846283051
- **Instagram**: instagram.com/muianga.oficial
- **Facebook**: facebook.com/share/1B5XpVw2Yw
- **LinkedIn**: linkedin.com/in/fredson-muianga-7495831ba
- **Threads**: threads.com/@muianga.oficial
- **SonhoEuropa**: https://sonhoeuropapp.vercel.app/
- **Muianga Carreiras**: https://muiangacarreiras.vercel.app/ (CVs e vagas de emprego)

Os restantes projectos (Muianga Consultores, ADIEP, Mentoria
Elite, Artes e Cultura, Fundação Muianga, Escola Seiva da Nação) têm
link `#` como placeholder — actualize-os com `update_links.py --project`
assim que os sites/páginas estiverem disponíveis.
