"""
coletar_dados.py - Coleta dados do alfabeto manual de Libras

Este script grava as coordenadas dos landmarks da sua mão
enquanto você faz cada letra do alfabeto de Libras.

Como funciona:
    1. O script mostra qual letra você deve sinalizar
    2. Você faz o sinal na frente da câmera
    3. Aperta ESPAÇO para gravar (ele grava várias amostras rápidas)
    4. Aperta ENTER para ir para a próxima letra
    5. No final, salva tudo em um arquivo .npy

Controles:
    ESPAÇO  = Gravar amostras da letra atual (segure para gravar várias)
    ENTER   = Próxima letra
    BACKSPACE = Letra anterior (caso queira refazer)
    S       = Salvar e sair
    Q       = Sair sem salvar

Dica: Para cada letra, tente gravar pelo menos 30 amostras.
      Varie um pouco a posição da mão (mais perto, mais longe,
      levemente girada) para o modelo aprender melhor.

Como usar:
    source venv/bin/activate
    python scripts/coletar_dados.py
"""

import cv2
import mediapipe as mp
import numpy as np
import os
import json
from datetime import datetime

# --- Configuração ---
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

# Letras do alfabeto manual de Libras + números
# (J e Z envolvem movimento, vamos marcar mas coletar como estáticos por enquanto)
CLASSES = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ") + ["Ç"] + [str(i) for i in range(10)]
# Total: 37 classes

# Pasta para salvar os dados
PASTA_DADOS = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "raw")
os.makedirs(PASTA_DADOS, exist_ok=True)

# --- Abrir câmera ---
camera = cv2.VideoCapture(0)
if not camera.isOpened():
    print("ERRO: Não foi possível abrir a câmera!")
    exit(1)

print("=" * 58)
print("  LibreSinais - Dia 4: Coletor de Dados para Libras")
print("=" * 58)
print()
print("  Controles:")
print("    ESPAÇO    = Gravar amostras (segure para gravar várias)")
print("    ENTER     = Próxima letra")
print("    BACKSPACE = Letra anterior")
print("    S         = Salvar e sair")
print("    Q         = Sair sem salvar")
print()
print(f"  Total de classes: {len(CLASSES)}")
print(f"  Dados serão salvos em: {PASTA_DADOS}")
print()

# --- Variáveis de controle ---
classe_atual = 0          # Índice da classe atual
dados = {}                # Dicionário: classe -> lista de vetores
for c in CLASSES:
    dados[c] = []

gravando = False          # Se está gravando no momento
total_amostras = 0        # Total geral de amostras coletadas


def extrair_vetor(mao_landmarks):
    """
    Extrai um vetor de 42 números (21 landmarks × 2 coordenadas)
    a partir dos landmarks de uma mão.

    Normaliza as coordenadas para que o pulso fique na origem
    e o tamanho da mão fique padronizado.
    """
    # Coletar x, y de cada landmark
    pontos = []
    for lm in mao_landmarks.landmark:
        pontos.append([lm.x, lm.y])

    pontos = np.array(pontos)  # Shape: (21, 2)

    # Normalizar: centralizar no pulso (ponto 0)
    pulso = pontos[0].copy()
    pontos = pontos - pulso  # Pulso vira (0, 0)

    # Normalizar: escalar pelo tamanho da mão
    # (distância do pulso até a base do dedo médio)
    base_medio = pontos[9]
    tamanho = np.linalg.norm(base_medio)
    if tamanho > 0:
        pontos = pontos / tamanho

    # Achatar para um vetor de 42 números
    vetor = pontos.flatten()  # Shape: (42,)

    return vetor


with mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.5
) as hands:

    while True:
        sucesso, frame = camera.read()
        if not sucesso:
            break

        frame = cv2.flip(frame, 1)
        h, w, _ = frame.shape
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        resultado = hands.process(frame_rgb)

        mao_detectada = False

        if resultado.multi_hand_landmarks:
            mao = resultado.multi_hand_landmarks[0]
            mao_detectada = True

            # Desenhar landmarks
            mp_drawing.draw_landmarks(
                frame, mao, mp_hands.HAND_CONNECTIONS,
                mp_drawing_styles.get_default_hand_landmarks_style(),
                mp_drawing_styles.get_default_hand_connections_style()
            )

            # Se estiver gravando, extrair e salvar o vetor
            if gravando:
                vetor = extrair_vetor(mao)
                classe_nome = CLASSES[classe_atual]
                dados[classe_nome].append(vetor)
                total_amostras += 1

        # --- Interface ---
        classe_nome = CLASSES[classe_atual]
        amostras_classe = len(dados[classe_nome])

        # Painel superior
        cv2.rectangle(frame, (0, 0), (w, 120), (0, 0, 0), -1)

        # Letra atual (grande)
        cv2.putText(frame, classe_nome,
                    (20, 90), cv2.FONT_HERSHEY_SIMPLEX,
                    3.0, (0, 255, 128), 4)

        # Info
        cv2.putText(frame, f"Classe {classe_atual + 1}/{len(CLASSES)}",
                    (160, 35), cv2.FONT_HERSHEY_SIMPLEX,
                    0.6, (200, 200, 200), 1)

        cv2.putText(frame, f"Amostras desta letra: {amostras_classe}",
                    (160, 65), cv2.FONT_HERSHEY_SIMPLEX,
                    0.6, (200, 200, 200), 1)

        cv2.putText(frame, f"Total geral: {total_amostras}",
                    (160, 95), cv2.FONT_HERSHEY_SIMPLEX,
                    0.6, (200, 200, 200), 1)

        # Barra de progresso da letra atual
        barra_x = 420
        barra_w = 200
        meta = 30  # meta de amostras por letra
        progresso = min(amostras_classe / meta, 1.0)
        cor_barra = (0, 255, 0) if progresso >= 1.0 else (0, 165, 255)
        cv2.rectangle(frame, (barra_x, 75), (barra_x + barra_w, 95), (50, 50, 50), -1)
        cv2.rectangle(frame, (barra_x, 75), (barra_x + int(barra_w * progresso), 95), cor_barra, -1)
        cv2.putText(frame, f"{amostras_classe}/{meta}",
                    (barra_x + barra_w + 10, 92), cv2.FONT_HERSHEY_SIMPLEX,
                    0.5, (200, 200, 200), 1)

        # Status de gravação
        if gravando and mao_detectada:
            cv2.circle(frame, (w - 30, 30), 12, (0, 0, 255), -1)
            cv2.putText(frame, "GRAVANDO",
                        (w - 130, 37), cv2.FONT_HERSHEY_SIMPLEX,
                        0.6, (0, 0, 255), 2)
        elif gravando and not mao_detectada:
            cv2.putText(frame, "MOSTRE A MAO!",
                        (w - 200, 37), cv2.FONT_HERSHEY_SIMPLEX,
                        0.6, (0, 0, 255), 2)

        # Instruções na parte inferior
        cv2.rectangle(frame, (0, h - 50), (w, h), (0, 0, 0), -1)
        cv2.putText(frame, "ESPACO=gravar  ENTER=proxima  BACKSPACE=anterior  S=salvar  Q=sair",
                    (10, h - 18), cv2.FONT_HERSHEY_SIMPLEX,
                    0.45, (180, 180, 180), 1)

        cv2.imshow("LibreSinais - Coletor de Dados", frame)

        # --- Controles ---
        tecla = cv2.waitKey(1) & 0xFF

        if tecla == ord(' '):  # ESPAÇO = gravar
            gravando = True
        else:
            gravando = False

        if tecla == 13:  # ENTER = próxima letra
            if classe_atual < len(CLASSES) - 1:
                classe_atual += 1
                print(f"  → Próxima letra: {CLASSES[classe_atual]}")

        if tecla == 8:  # BACKSPACE = letra anterior
            if classe_atual > 0:
                classe_atual -= 1
                print(f"  ← Voltando para: {CLASSES[classe_atual]}")

        if tecla == ord('s'):  # S = salvar e sair
            break

        if tecla == ord('q'):  # Q = sair sem salvar
            print("\n  Saindo SEM salvar...")
            camera.release()
            cv2.destroyAllWindows()
            exit(0)

# --- Salvar dados ---
camera.release()
cv2.destroyAllWindows()

# Verificar se tem dados
if total_amostras == 0:
    print("\n  Nenhuma amostra coletada. Nada para salvar.")
    exit(0)

# Gerar nome do arquivo com timestamp
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
arquivo_dados = os.path.join(PASTA_DADOS, f"libras_dados_{timestamp}.npy")
arquivo_info = os.path.join(PASTA_DADOS, f"libras_dados_{timestamp}_info.json")

# Preparar dados para salvar
# Formato: dicionário com arrays numpy
dados_para_salvar = {}
info = {"classes": {}, "total_amostras": total_amostras, "data_coleta": timestamp}

print()
print("=" * 50)
print("  Resumo da coleta:")
print("=" * 50)

for classe in CLASSES:
    n = len(dados[classe])
    if n > 0:
        dados_para_salvar[classe] = np.array(dados[classe])
        info["classes"][classe] = n
        status = "✓" if n >= 30 else "⚠ (poucas)"
        print(f"    {classe}: {n} amostras {status}")

# Salvar
np.save(arquivo_dados, dados_para_salvar, allow_pickle=True)

with open(arquivo_info, 'w') as f:
    json.dump(info, f, indent=2, ensure_ascii=False)

print()
print(f"  Total: {total_amostras} amostras")
print(f"  Dados salvos em: {arquivo_dados}")
print(f"  Info salva em:   {arquivo_info}")
print()
print("  Dica: colete dados de várias sessões para um modelo melhor!")
print("  Os arquivos podem ser combinados depois no treinamento.")