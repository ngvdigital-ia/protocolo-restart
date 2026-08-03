# DESIGN — Protocolo Restart (clone fiel)

Registro extraído de `_reference/source.html` e das capturas de referência de 2026-08-03. Este documento é um contrato de reprodução, não uma direção nova: não substituir o player, não reinterpretar a composição e não acrescentar elementos visuais.

## 1. Conceito-âncora

`"Reset metabólico em 9 dias" apresentado por uma VSL vertical isolada; a página funciona como moldura creme mínima, não como landing page editorial.`

## 2. Modo

`conversao` — clone fiel de VSL. Prioridade: player vertical central, leitura imediata em mobile, conteúdo de venda bloqueado até o pitch e rodapé legal persistente.

## 3. Color

```yaml
base-pre-pitch: "#F6F4EE" # fundo dos containers inicial e de rodapé
texto-pre-pitch: ["#000000", "#535353", "#FFFFFF"]
cta-pos-pitch: ["#F24A33", "#FB513B", "#00AC1A"] # cada seletor Elementor preserva sua própria cor
neutros-pos-pitch: ["#0F0F0F", "#131313", "#191717", "#1D1D1D", "#272727", "#2A2A2A", "#666666", "#777777", "#C2C2C2", "#E7E7E7", "#EEEEEB"]
azuis-verdes-pos-pitch: ["#1D3A44", "#333C43", "#4A6169", "#04727A", "#078AA9", "#00909B", "#A4CEC5"]
outros-pos-pitch: ["#B39154"]
```

Paleta extraída do CSS canônico `post-213.css`, válida por seletor e por seção. Não usar a paleta navy/lime da implementação rejeitada **fora dos seletores herdados**; preservar exatamente as cores por seção da origem. As cores do render do player continuam pertencendo ao player, não a uma nova camada global.

## 4. Typography

```yaml
display: "não há H1/H2 fora do player antes do pitch; preservar a tipografia renderizada pelo fornecedor do player sem tentar recriá-la"
body: "Inter 400, Arial, sans-serif"
footer: "Inter 400 / 14px desktop, 12px mobile / line-height 1.5"
cta-pos-pitch: "Montserrat 500, sans-serif / 23px desktop; 18px mobile"
h1: "N/A fora do smartplayer — não inventar clamp, tracking ou headline HTML"
h2-h6: "N/A no estado pré-pitch; títulos do DOM pós-pitch preservam a fonte, pesos e escalas de cada regra Elementor de origem"
```

## 5. Spacing

```yaml
pagina-pre-pitch-desktop: "padding 70px 0 80px"
pagina-pre-pitch-mobile: "padding 40px 8px 50px"
player: "436px max-width, width: 100%, margin-inline: auto"
rodape-desktop: "padding 40px 0"
rodape-mobile: "padding 30px 10px"
rodape-mobile-conteudo: "max-width 449px, centralizado"
pos-pitch: "containers Elementor preservam os paddings originais por bloco (predominantemente 90px vertical; exceções de 60/70, 80/100 e 20/70px)"
```

## 6. Components

```yaml
player-pre-pitch:
  estrutura: "único vturb-smartplayer central; o frame de vídeo contém título, imagem/thumbnail e controles próprios"
  estado: "visível desde o carregamento; nenhuma copy externa ao player"
  layout: "coluna única, sem header, navegação, cards, hero adicional ou CTA visível"
rodape:
  estrutura: "links Política de Privacidade | Termos de Uso; quatro avisos legais; copyright"
  estado: "sempre visível, inclusive antes do pitch"
  alinhamento: "centralizado"
cta-pos-pitch:
  cor: "#F24A33, #FB513B ou #00AC1A sobre #FFFFFF, conforme o seletor Elementor de origem"
  raio: "18px"
  desktop: "23px; padding 23px 50px; max-width 430px"
  mobile: "18px; padding 16px; max-width 327px"
  hover: "somente a classe de origem elementor-animation-grow; não criar estado novo"
```

### Estado pré-pitch e revelação pós-pitch

Antes do pitch, `.esconder { display: none; }`: há somente o player, sobre `#F6F4EE`, e o rodapé legal. Ao evento `player:ready`, as versões de player mapeadas no HTML chamam `displayHiddenElements(1431, ['.esconder'], { persist: true })`; o gatilho é **23:51 (1431 s)**.

O DOM de referência contém 21 nós com `.esconder` (16 containers `e-parent` de conteúdo e 5 CTAs). Para execução e revisão, eles formam as **18 seções pós-pitch** abaixo — CTAs repetidos pertencem aos blocos de oferta/credibilidade/FAQ, sem criar layout independente:

1. CTA inicial “QUERO ACESSO IMEDIATO!”.
2. Dor: ciclo interminável / mensagens de restrição.
3. Comparação visual: salada, pochete e barriga + culpa.
4. Reenquadramento: “você não falhou”.
5. História/antes de Isadora.
6. Explicação da “verdade que ninguém fala”.
7. Apresentação do Protocolo Restart e seus dois elementos.
8. Provas sociais (Kelly, Stefany, Danielle).
9. Diferenciação do Restart em relação a dietas.
10. Lista do que existe dentro do protocolo.
11. Três passos: ajustar, resetar, transformar.
12. Critérios de “o Restart é para você”.
13. Combo Magra Pra Sempre e os três bônus.
14. Empilhamento de oferta, preço e CTA.
15. Bloco posterior de três passos / bio de Isadora e CTA.
16. Garantia e CTA associado.
17. FAQ de 11 perguntas.
18. CTA final associado ao FAQ.

O agrupamento acima não autoriza simplificar, reordenar, excluir ou adicionar copy, imagens, cards, bullets, preço, bônus ou CTAs. No clone, a mesma regra de revelar todos os elementos marcados é a fonte de verdade; a lista é um mapa de QA, não uma nova estrutura.

## 7. Motion

```yaml
dur-micro: "0ms de motion autoral; CTA mantém apenas o comportamento de origem `elementor-animation-grow`"
dur-layout: "0ms; os blocos surgem pelo mecanismo do player, sem transição CSS própria declarada no HTML"
dur-page: "gatilho aos 1431s (23:51), persistido pelo player"
ease-out: "N/A — não declarado pela referência"
ease-in: "N/A — não declarado pela referência"
ease-inout: "N/A — não declarado pela referência"
```

## 8. Voice

```yaml
do:
  - "Manter a VSL como conteúdo dominante e a página como moldura silenciosa."
  - "Preservar o contraste e a cor de cada CTA pós-pitch conforme o seletor de origem (coral, vermelho-coral ou verde)."
  - "Exibir exatamente o rodapé legal centralizado no estado inicial."
dont:
  - "Não criar hero, navbar, selo, logo, ícone, card ou seção paralela."
  - "Não antecipar CTA, preço, prova social, FAQ ou qualquer conteúdo .esconder antes de 23:51."
  - "Não recriar em HTML a copy ou a aparência que pertence ao player/VTurb."
```

## 9. Anti-patterns

```yaml
- "Usar a paleta navy/lime da implementação rejeitada fora dos seletores herdados; preservar exatamente as cores por seção da origem, inclusive fundos escuros, azuis/teais e CTAs coral, vermelho-coral ou verde quando o CSS canônico os definir."
- "Página longa visível desde o início: os 21 nós .esconder só surgem pelo evento do player aos 1431s."
- "Player substituto, thumbnail inventada, VTurb/player ID inventado, tracking inventado ou controles recriados."
- "Tipografia de headline, clamp ou copy adicionados fora do player; no estado inicial não há H1/H2 visível no DOM."
- "Radius, sombras, animações, seção de benefícios ou design system novos que alterem a referência."
```
