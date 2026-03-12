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

### Diário de desenvolvimento

| Data | Dia | O que foi feito |
|---|---|---|
| 12/03/2026 | Dia 1 | Criação do repositório, estrutura de pastas, módulos Python e documentação |
| 12/03/2026 | Dia 2 | Ambiente virtual configurado, dependências instaladas, primeiro teste com câmera + MediaPipe funcionando ✅ |

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
├── scripts/
│   └── testar_camera.py     # ✅ Teste de câmera com MediaPipe (funcional)
├── data/
│   ├── raw/                 # Dados brutos coletados
│   └── processed/           # Dados processados para treinamento
├── tests/                   # Testes automatizados
├── config/                  # Arquivos de configuração
├── docs/                    # Documentação adicional
└── README.md
```

## Tecnologias

| Componente | Tecnologia | Versão testada | Para que serve |
|---|---|---|---|
| Captura de vídeo | OpenCV | 4.13.0 | Acessar a webcam |
| Detecção de mãos | MediaPipe Hands | 0.10.14 | Encontrar os 21 pontos de cada mão na imagem |
| Classificação | scikit-learn / TensorFlow | 1.8.0 / em breve | Identificar qual sinal está sendo feito |
| Integração | Python-UNO Bridge | — | Inserir texto no LibreOffice Writer |

## Como instalar

### Pré-requisitos

- Python 3.10 ou superior
- LibreOffice 7.0 ou superior (para integração futura)
- Webcam
- Git
- Sistema operacional: Linux, Windows ou macOS

### Instalação

```bash
# 1. Clonar o repositório
git clone https://github.com/maurizioprizzi/libresinais.git
cd libresinais

# 2. Criar ambiente virtual
python3 -m venv venv

# 3. Ativar o ambiente virtual
source venv/bin/activate        # Linux/Mac
# venv\Scripts\activate         # Windows

# 4. Instalar dependências
pip install -r requirements.txt

# 5. Corrigir versão do MediaPipe (necessário até atualização do requirements)
pip install mediapipe==0.10.14
```

### Testar a câmera

```bash
# Com o ambiente virtual ativado:
python scripts/testar_camera.py
```

Ao rodar, uma janela abrirá mostrando a imagem da webcam. Mostre suas mãos para a câmera e você verá os 21 pontos de referência desenhados em cada mão. Aperte **q** para sair.

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