# Fredson Muianga — Portfolio Pessoal

Website pessoal de nível executivo para Fredson Muianga — empresário,
consultor, escritor e fundador moçambicano baseado em Maputo. Posicionamento
editorial/institucional: preto profundo, branco/off-white, grafite e um
acento dourado metálico discreto, tipografia Playfair Display (serif) + DM
Sans (sans-serif).

## Estrutura de ficheiros

```
/
├── index.html         # Página principal (HTML + CSS + JS num único ficheiro)
├── foto.jpg            # Foto real de Fredson Muianga
├── assets/
│   ├── threads-icon.png
│   └── whatsapp-icon.png
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

## 2. Ver a página localmente

```bash
python -m http.server 8000
```

E aceder a `http://localhost:8000`.

## 3. Estrutura do site

A página está organizada em secções, navegáveis pela barra fixa no topo:

1. **Hero** — nome, posicionamento ("Empresário · Consultor · Escritor ·
   Fundador") e duas chamadas à acção: "Conhecer o meu trabalho" e "Falar
   comigo".
2. **Sobre** — apresentação executiva.
3. **Áreas de Actuação** — seis categorias estratégicas: Business &
   Consulting, Technology & Digital, Education & Career, Culture &
   Entertainment, Social Impact, Entrepreneurship & Projects.
4. **Projectos & Empresas** — portfolio de fundador: nome, categoria,
   descrição, papel de Fredson e link (quando existe).
5. **Impacto** — secção institucional com a frase "Construir oportunidades
   que permanecem para além de um projecto."
6. **Pensamentos / Escritor** — o livro *O Telemóvel na Mesa de Jantar*, com
   links directos de compra.
7. **Presença Digital** — LinkedIn, Instagram, Threads, Facebook, WhatsApp.
8. **O que faço** — serviços detalhados, cada um com contacto directo por
   chamada ou WhatsApp.
9. **Contacto** — telefone, email, WhatsApp, localização (Maputo).

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
`Artes e Cultura`, `Fundação Fredson Muianga`, `Escola Seiva da Nação`,
`Muianga Carreiras`.

## 5. Gerar as meta tags Open Graph após o deploy (`generate_og.py`)

Depois de publicar o site (Vercel, Netlify, GitHub Pages, etc.), execute:

```bash
python generate_og.py --url "https://fredsonmuianga.com" --image "https://fredsonmuianga.com/og-image.png"
```

Isto:
1. Remove as meta tags Open Graph/Twitter antigas (com os placeholders).
2. Injecta as novas tags com o URL final do site e da imagem de preview.
3. Gera `og-image.html` — uma página de 1200x630px (fundo escuro, Playfair
   Display, acento dourado) pronta para ser aberta no browser e capturada
   como screenshot (`og-image.png`), que deve depois ser publicada junto do
   site e apontada em `--image`.

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

## 7. Livro — O Telemóvel na Mesa de Jantar

Links de compra reais, já configurados na secção "Pensamentos":

- **Emola / M-Pesa**: https://checkout.escalepay.com/6347849
- **Visa / Google Pay**: https://checkout.escalepay.com/8395328

## 8. Projectos e contactos reais já configurados

- **Telefone**: +258 84 628 3051 · +258 87 625 2006
- **Email**: fredsonyb@gmail.com
- **WhatsApp**: https://wa.me/258846283051
- **Instagram**: instagram.com/muianga.oficial
- **Facebook**: facebook.com/share/1B5XpVw2Yw
- **LinkedIn**: linkedin.com/in/fredson-muianga-7495831ba
- **Threads**: threads.com/@muianga.oficial
- **SonhoEuropa**: https://sonhoeuropapp.vercel.app/ (Fundador)
- **Muianga Carreiras**: https://muiangacarreiras.vercel.app/ (Fundador —
  CVs e vagas de emprego)
- **Escola Seiva da Nação**: https://escolaseivadanacao.vercel.app/

Os restantes projectos (Muianga Consultores, ADIEP, Mentoria Elite, Artes e
Cultura, Fundação Fredson Muianga) ainda não têm link público —
actualize-os com `update_links.py --project` assim que os sites/páginas
estiverem disponíveis.
