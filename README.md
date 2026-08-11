# Tecnodemocracia Biocêntrica — Explorador Interativo

Dashboard interativo em HTML/CSS/JS que apresenta, para um público leigo, os conceitos centrais do **Método Brasiliano** e da **Tecnodemocracia Biocêntrica**: a "Armadilha Brasiliana" institucional, a dinâmica do vetor de estado Φ, o Funcional de Brasilde e o Sistema VERDE de tokenização de capital natural.

## O que tem aqui

| Seção | Conteúdo |
|---|---|
| **Diagnóstico** | Gráfico de rosca mostrando a mudança de paradigma na matriz de valor |
| **Método Brasiliano** | Gráfico radar comparando o estado institucional atual ("Atrito") com o potencial ("Fluidez") nas três dimensões Φᴿ, Φˢ, Φᴾ |
| **Matemática do Desenvolvimento** | Quatro cartões traduzindo, em linguagem acessível, a SDE institucional, o Funcional de Brasilde, a Elasticidade-Sombra εⁱ e o "Veredito da Unificação" |
| **Sistema VERDE** | Fluxo interativo (Usufruto → Validação IoT/satélite → Liquidez via blockchain → Renda Básica) com painéis clicáveis |
| **Laboratório de Simulação IA** | Analista de cenários institucionais (texto) e gerador de imagens "Visão 2050", via API Gemini |
| **Planejador de Projetos VERDE** | Gerador de planos de ação estruturados em JSON via IA |
| **Consultor Brasiliano IA** | Chatbot flutuante treinado para responder sobre o framework |

## Stack

- HTML puro + [Tailwind CSS](https://tailwindcss.com) via CDN
- [Chart.js](https://www.chartjs.org) via CDN (gráfico de rosca e radar)
- Fontes Inter (texto) e JetBrains Mono (equações), via Google Fonts
- Sem build step, sem backend — um único arquivo HTML

## ⚠️ Antes de publicar: as funções de IA não funcionam sozinhas

O arquivo foi gerado num ambiente ("Canvas") que injeta automaticamente uma chave de API do Gemini em tempo de execução:

```js
const apiKey = ""; // Canvas provides this automatically
```

Fora desse ambiente — inclusive no GitHub Pages ou Netlify — essa chave chega vazia, e as quatro funções que dependem dela vão falhar silenciosamente ou mostrar "Erro na conexão com o modelo":

- Analista de Vetor Φ (`gemini-3-flash-preview`)
- Visualizador Biocêntrico / geração de imagem (`imagen-4.0-generate-001`)
- Planejador de Projetos VERDE (`gemini-3-flash-preview`)
- Consultor Brasiliano IA, o chatbot flutuante (`gemini-3-flash-preview`)

O restante do dashboard — gráficos, seções, fluxo interativo do Sistema VERDE — funciona normalmente sem nenhuma chave.

**Opções para as funções de IA funcionarem em produção:**

1. **Deixar desativado.** Mais simples e mais seguro para um site público; nenhum dado sai do navegador do visitante.
2. **Colar uma chave própria** direto em `apiKey`. Funciona, mas fica visível a qualquer pessoa que veja o código-fonte da página (é tudo client-side) — só recomendável com uma chave restrita por domínio e com cota baixa, nunca uma chave de produção.
3. **Rotear as chamadas por um backend simples** (uma function serverless, por exemplo) que guarda a chave no servidor e nunca a expõe ao navegador. É o padrão correto para produção, mas exige mais do que um único arquivo estático.

## Problema conhecido

O menu de navegação tem um link **"Pilares"** apontando para `#pilares`, mas não existe nenhuma seção com esse `id` no HTML — o link não leva a lugar nenhum. Provavelmente a seção "Pilares Acadêmicos", citada no comentário de estrutura no topo do arquivo, ficou de fora da versão final.

## Como rodar localmente

Não precisa de servidor — é um arquivo só:

```bash
open index.html   # macOS — ou apenas arraste o arquivo para o navegador
```

## Como publicar

Mesmo processo já usado para o dashboard Gaia: renomear este arquivo para `index.html`, subir num repositório novo no GitHub e ativar em *Settings → Pages*.
