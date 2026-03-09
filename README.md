# ✋ LibreSinais

**Plugin open source para LibreOffice Writer que reconhece Libras via webcam e converte em texto.**

Uma doação para a comunidade surda brasileira.

---

## O que é

O LibreSinais é uma extensão para o LibreOffice Writer que usa a câmera do computador para reconhecer sinais da Língua Brasileira de Sinais (Libras) e inseri-los como texto no documento.

O objetivo é permitir que pessoas surdas possam produzir documentos usando sua língua natural.

## Como funciona

```
Câmera → MediaPipe (detecta as mãos) → Modelo de ML (classifica o sinal) → Texto no Writer
```

1. A webcam captura a imagem das mãos
2. O MediaPipe extrai os pontos de referência (landmarks) das mãos
3. Um modelo de Machine Learning classifica o gesto como uma letra ou sinal
4. O texto é inserido no documento do LibreOffice Writer

## Status do projeto

🚧 **Em desenvolvimento — Fase 1 (Protótipo)**

Estamos começando pelo reconhecimento do **alfabeto manual de Libras** (A–Z, Ç) e números (0–9).

## Estrutura do projeto

```
libresinais/
├── python/
│   └── libresinais/        # Código principal do plugin
│       ├── __init__.py
│       ├── camera.py        # Captura de vídeo (OpenCV)
│       ├── detector.py      # Detecção de mãos (MediaPipe)
│       ├── classifier.py    # Classificação dos sinais (ML)
│       ├── stabilizer.py    # Buffer de confiança
│       └── writer_bridge.py # Integração com LibreOffice (UNO)
├── models/
│   └── libras/              # Modelos treinados para Libras
├── data/
│   ├── raw/                 # Dados brutos coletados
│   └── processed/           # Dados processados para treinamento
├── scripts/                 # Scripts auxiliares (coleta de dados, treinamento)
├── tests/                   # Testes automatizados
├── config/                  # Arquivos de configuração
├── docs/                    # Documentação adicional
└── README.md
```

## Tecnologias

| Componente | Tecnologia | Para que serve |
|---|---|---|
| Captura de vídeo | OpenCV | Acessar a webcam |
| Detecção de mãos | MediaPipe Hands | Encontrar os pontos das mãos na imagem |
| Classificação | scikit-learn / TensorFlow | Identificar qual sinal está sendo feito |
| Integração | Python-UNO Bridge | Inserir texto no LibreOffice Writer |

## Requisitos

- Python 3.10 ou superior
- LibreOffice 7.0 ou superior
- Webcam
- Sistema operacional: Linux, Windows ou macOS

## Como instalar (em breve)

> ⚠️ O projeto ainda está em fase inicial de desenvolvimento. As instruções de instalação serão adicionadas conforme o progresso.

## Como contribuir

Este é um projeto de doação — toda ajuda é bem-vinda!

- **Desenvolvedores Python:** ajudem com o pipeline de reconhecimento e integração
- **Comunidade surda:** validem os sinais, gravem dados, deem feedback
- **Pesquisadores de ML:** ajudem a treinar e otimizar os modelos
- **Qualquer pessoa:** testem, reportem bugs, sugiram melhorias

Veja o arquivo [CONTRIBUTING.md](CONTRIBUTING.md) para detalhes.

## Sobre Libras

A Língua Brasileira de Sinais (Libras) é reconhecida como meio legal de comunicação pela [Lei nº 10.436/2002](https://www.planalto.gov.br/ccivil_03/leis/2002/l10436.htm), regulamentada pelo [Decreto nº 5.626/2005](https://www.planalto.gov.br/ccivil_03/_ato2004-2006/2005/decreto/d5626.htm).

Libras **não** é uma versão gestual do português — é uma língua completa, com gramática própria, usada por mais de 10 milhões de brasileiros.

## Licença

Este projeto é distribuído sob a licença [Apache 2.0](LICENSE).

---

*LibreSinais — Porque a comunicação é um direito de todos.* 🤟