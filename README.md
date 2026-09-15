# 🐾 Aniimo Wiki — Cópia Completa Offline & Base de Dados

Cópia idêntica, completa e 100% funcional do site oficial [https://wiki.aniimo.com/](https://wiki.aniimo.com/).

---

## 📊 Resumo da Análise Técnica do Site Original

- **Stack Tecnológico:** Nuxt 3 (Vue 3 SSR / Prerendered) + Tailwind CSS.
- **Distribuição e CDN:** Akamai Edge Network (`kg-web-cdn.akamaized.net`) e WorldX Media CDN (`worldx-website-cdn.aniimo.com`).
- **Idiomas Nativos:** Inglês (`en-US`), Japonês (`ja-JP`), Coreano (`ko-KR`) e Chinês Tradicional (`zh-TW`).
- **Catálogo:** 94 espécies únicas de Aniimos registradas, com estágios evolutivos (*Lumin*, *Gamma*, *Nova*), elementos (*Fire, Water, Grass, Electric, Ice, Wind, Dark, Holy, Rock*), funções de combate (*DPS, Heal, Support, Break, Regen*), habilidades passivas, ativas e árvores de evolução completas.

---

## 📦 Conteúdo Clonado

Total de arquivos no clone: **2.096 arquivos**

1. **Páginas HTML & Payloads:**
   - **380 páginas completas** (Homepage + 94 itens detalhados em todos os idiomas: EN, JA, KO, TW).
   - Todos os arquivos `_payload.json` pré-renderizados do Nuxt 3 para transições SPA ultrarrápidas.

2. **Mídias e Recursos Baixados Localmente (935 arquivos de mídia):**
   - **95 artes oficiais em alta resolução** de corpo inteiro com fundo transparente (`.png`).
   - **92 avatares de cabeça (Pet Heads)** para interfaces e ícones (`.png`).
   - **600 ícones de habilidades e características** (`.png`).
   - **94 vídeos demonstrativos de efeitos visuais (VFX)** de combate em formato `.mp4`.
   - **Fontes originais** (ex: `BILLGATES-2.TTF`) e folhas de sprites (`attributes.png`, `positions.png`, `stages.png`).
   - **Todos os bundles JS e folhas de estilo CSS** do Nuxt 3.

3. **Reescrita e Adaptação 100% Offline:**
   - Todas as URLs absolutas que apontavam para servidores externos foram reescritas para caminhos relativos locais (`/_nuxt/`, `/cdn/`, `/images/`, `/fonts/`).
   - Removido o banner do Cookiebot que causava bloqueio ou atraso sem internet.
   - Suporte completo a streaming de vídeo com cabeçalhos HTTP `Range` (206 Partial Content).

4. **Base de Dados Estruturada:**
   - Arquivo `data/all_aniimos.json` contendo todos os 376 registros com IDs, números da pokédex/índice, nomes, descrições, estágios, links das imagens locais e vídeos de VFX.

---

## 🚀 Como Executar o Clone

### Opção 1: Pelo arquivo executável (.bat)
Basta dar **duplo clique** no arquivo:
```
iniciar_wiki.bat
```
Ele abrirá automaticamente o navegador padrão no endereço: `http://localhost:8080/`

### Opção 2: Pelo Terminal / Prompt de Comando
Abra o terminal na pasta do projeto e execute:
```bash
python serve.py
```
Acesse: [http://localhost:8080/](http://localhost:8080/)

---

## 📂 Estrutura de Diretórios

```
aniimo-wiki/
├── site/                     # Raiz do site estático
│   ├── index.html            # Página inicial do catálogo
│   ├── _payload.json         # Dados da home
│   ├── _nuxt/                # Scripts JS compilados e CSS
│   ├── fonts/                # Fontes tipográficas originais
│   ├── images/               # Sprites, logos, UI e cabeçalho
│   ├── cdn/                  # 935 artes em alta resolução e vídeos VFX
│   │   ├── init/             # Imagens dos Aniimos e ícones de skills
│   │   └── Vfx/              # Vídeos MP4 das habilidades
│   ├── item/                 # Páginas individuais dos 94 Aniimos
│   ├── ja/                   # Versão japonesa
│   ├── ko/                   # Versão coreana
│   └── tw/                   # Versão chinesa tradicional
├── data/
│   └── all_aniimos.json      # Banco de dados estruturado em JSON
├── clone_aniimo_wiki.py      # Script automatizado de download assíncrono
├── serve.py                  # Servidor HTTP local com suporte a Range requests
└── iniciar_wiki.bat          # Inicializador com 1 clique para Windows
```
