# mpunch-catalog

Uma plataforma de visualização de dados desenvolvida para análise de charges do periódico **Melbourne Punch** no período entre 1855 e 1860. Esta iniciativa nasceu como ferramenta metodológica durante a dissertação *"Melbourne Punch: Idealizações de um "mundo britânico" na Austrália colonial (1855-1860)"*.

## Sobre o Projeto
Este repositório contém uma interface web interativa para exploração e análise de dados das charges publicadas no Melbourne Punch durante seus primeiros anos de circulação. A plataforma oferece múltiplas visualizações que permitem investigar padrões temáticos, co-ocorrências de assuntos e distribuições temporais no corpus documental.

### Objetivos
- **Análise Temática**: Identificar e quantificar os principais temas abordados nas charges
- **Co-ocorrência de Temas**: Mapear relações e conexões entre diferentes assuntos
- **Distribuição Temporal**: Examinar a evolução dos temas ao longo do período estudado

## Contexto Acadêmico
**Instituição**: Universidade Estadual de Campinas (UNICAMP)  
**Unidade**: Instituto de Filosofia e Ciências Humanas  
**Financiamento**: Conselho Nacional de Desenvolvimento Científico e Tecnológico (CNPq)

## Funcionalidades
### Visualizações Disponíveis

1. **Co-ocorrência de Temas** - Rede interativa mostrando conexões entre temas
2. **Distribuição por Ano** - Análise temporal com gráficos e estatísticas

## Estrutura dos Dados

O dataset principal (`cartoons.json`) contém registros estruturados com os seguintes campos:


```json
{
  "id": 1789,
  "title": "A MERRY CHRISTMAS AND A HAPPY NEW YEAR!",
  "caption": "",
  "content": "<p>Texto da charge...</p>",
  "category": "Decorativa",
  "publication_date": "1860-12-27T00:00:00.000Z",
  "author_name": "",
  "engraver_name": "",
  "image_url": "./data/imgs/...",
  "themes": ["Festividades"],
  "topic": "Cotidiano",
  "year": 1860,
  "has_author_signature": false,
  "has_engraver_signature": false
}
```

### Construção do Dataset
O corpus documental foi construído através de um processo de:

- Leitura sistemática das edições do Melbourne Punch (1855-1860) via Trove Digital Collections
- Extração automatizada de charges, ilustrações e textos satíricos relevantes
- Catalogação estruturada com metadados descritivos e analíticos
- Validação e revisão dos dados catalogados para consistência

O dataset resultante representa uma amostra significativa da produção imagética e textual do periódico, organizizada para análise quantitativa e qualitativa através de técnicas de humanidades digitais.

## Desenvolvimento e Documentação

**Importante**: Parte do código deste repositório e esta documentação foram desenvolvidos com assistência do **Claude.ai**.

## Contribuições

Este projeto foi desenvolvido especificamente para fins acadêmicos. Sugestões e melhorias são bem-vindas, especialmente relacionadas a:

- Otimização de performance para grandes datasets
- Novas visualizações relevantes para análise histórica
- Melhorias na acessibilidade da interface
- Correções de bugs ou inconsistências