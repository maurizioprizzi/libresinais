"""
ver_landmarks.py - Visualiza as coordenadas dos landmarks das mãos

Este script mostra os NÚMEROS que o MediaPipe extrai de cada mão.
São esses números que vamos usar para treinar o classificador de Libras.

Cada mão tem 21 pontos (landmarks), e cada ponto tem 3 coordenadas:
    - x: posição horizontal (0.0 = esquerda, 1.0 = direita)
    - y: posição vertical (0.0 = topo, 1.0 = base)
    - z: profundidade (quanto menor, mais perto da câmera)

Os 21 pontos são:
    0  = Pulso (WRIST)
    1  = Base do polegar (THUMB_CMC)
    2  = Meio do polegar (THUMB_MCP)
    3  = Falange do polegar (THUMB_IP)
    4  = Ponta do polegar (THUMB_TIP)
    5  = Base do indicador (INDEX_FINGER_MCP)
    6  = Meio do indicador (INDEX_FINGER_PIP)
    7  = Falange do indicador (INDEX_FINGER_DIP)
    8  = Ponta do indicador (INDEX_FINGER_TIP)
    9  = Base do médio (MIDDLE_FINGER_MCP)
    10 = Meio do médio (MIDDLE_FINGER_PIP)
    11 = Falange do médio (MIDDLE_FINGER_DIP)
    12 = Ponta do médio (MIDDLE_FINGER_TIP)
    13 = Base do anelar (RING_FINGER_MCP)
    14 = Meio do anelar (RING_FINGER_PIP)
    15 = Falange do anelar (RING_FINGER_DIP)
    16 = Ponta do anelar (RING_FINGER_TIP)
    17 = Base do mínimo (PINKY_MCP)
    18 = Meio do mínimo (PINKY_PIP)
    19 = Falange do mínimo (PINKY_DIP)
    20 = Ponta do mínimo (PINKY_TIP)

Como usar:
    1. Ative o ambiente virtual: source venv/bin/activate
    2. Rode: python scripts/ver_landmarks.py
    3. Mostre UMA mão para a câmera
    4. Observe os números mudando conforme você mexe os dedos
    5. Aperte 'q' para sair

Experimente:
    - Faça a letra A de Libras (punho fechado, polegar ao lado)
    - Faça a letra B (mão aberta, dedos juntos)
    - Veja como os números mudam!
    Esses números diferentes são o que permite ao ML distinguir as letras.
"""

import cv2
import mediapipe as mp
import numpy as np

# --- Configuração ---
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

# Nomes resumidos dos 21 landmarks
NOMES = [
    "Pulso",
    "Polegar1", "Polegar2", "Polegar3", "Polegar4",
    "Indicad1", "Indicad2", "Indicad3", "Indicad4",
    "Medio1",   "Medio2",   "Medio3",   "Medio4",
    "Anelar1",  "Anelar2",  "Anelar3",  "Anelar4",
    "Minimo1",  "Minimo2",  "Minimo3",  "Minimo4",
]

# --- Abrir câmera ---
camera = cv2.VideoCapture(0)
if not camera.isOpened():
    print("ERRO: Não foi possível abrir a câmera!")
    exit(1)

print("=" * 55)
print("  LibreSinais - Dia 3: Visualizador de Landmarks")
print("=" * 55)
print()
print("  Mostre UMA mão para a câmera.")
print("  Observe os números mudando conforme mexe os dedos.")
print()
print("  Experimente fazer letras de Libras e veja")
print("  como os números mudam para cada letra!")
print()
print("  Aperte 'q' para sair.")
print()

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
        h_frame, w_frame, _ = frame.shape

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        resultado = hands.process(frame_rgb)

        # --- Painel lateral para os números ---
        # Cria uma área preta à direita do frame para mostrar os dados
        painel_largura = 320
        painel = np.zeros((h_frame, painel_largura, 3), dtype=np.uint8)

        # Título do painel
        cv2.putText(painel, "LANDMARKS DA MAO",
                    (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 128), 2)
        cv2.putText(painel, "Ponto        X      Y      Z",
                    (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (200, 200, 200), 1)
        cv2.line(painel, (10, 68), (painel_largura - 10, 68), (100, 100, 100), 1)

        if resultado.multi_hand_landmarks:
            mao = resultado.multi_hand_landmarks[0]

            # Desenhar landmarks no frame
            mp_drawing.draw_landmarks(
                frame, mao, mp_hands.HAND_CONNECTIONS,
                mp_drawing_styles.get_default_hand_landmarks_style(),
                mp_drawing_styles.get_default_hand_connections_style()
            )

            # Mostrar coordenadas no painel
            for i, landmark in enumerate(mao.landmark):
                x = landmark.x
                y = landmark.y
                z = landmark.z

                # Cor: pontas dos dedos em verde, resto em branco
                eh_ponta = i in [4, 8, 12, 16, 20]
                cor = (0, 255, 0) if eh_ponta else (220, 220, 220)

                texto = f"{NOMES[i]:10s} {x:.3f}  {y:.3f}  {z:.4f}"
                pos_y = 85 + i * 22
                cv2.putText(painel, texto,
                            (10, pos_y), cv2.FONT_HERSHEY_SIMPLEX,
                            0.38, cor, 1)

                # Desenhar o número do landmark no frame (sobre a mão)
                px = int(landmark.x * w_frame)
                py = int(landmark.y * h_frame)
                cv2.putText(frame, str(i),
                            (px + 5, py - 5), cv2.FONT_HERSHEY_SIMPLEX,
                            0.3, (255, 255, 0), 1)

            # Mostrar vetor resumido (o que o classificador vai receber)
            cv2.putText(painel, "VETOR DO CLASSIFICADOR:",
                        (10, 560), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 200, 255), 1)
            cv2.putText(painel, f"42 numeros (21 pontos x 2 coords)",
                        (10, 582), cv2.FONT_HERSHEY_SIMPLEX, 0.38, (180, 180, 180), 1)
            cv2.putText(painel, f"[{mao.landmark[0].x:.2f}, {mao.landmark[0].y:.2f}, "
                        f"{mao.landmark[1].x:.2f}, {mao.landmark[1].y:.2f}, ...]",
                        (10, 602), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (180, 180, 180), 1)

        else:
            cv2.putText(painel, "Nenhuma mao detectada",
                        (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
            cv2.putText(painel, "Mostre sua mao para a camera!",
                        (10, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (150, 150, 150), 1)

        # Info no frame
        cv2.rectangle(frame, (0, 0), (300, 35), (0, 0, 0), -1)
        cv2.putText(frame, "LibreSinais - Landmarks",
                    (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 128), 2)

        cv2.putText(frame, "'q' = sair",
                    (10, h_frame - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (180, 180, 180), 1)

        # Juntar frame e painel lado a lado
        tela = np.hstack([frame, painel])

        cv2.imshow("LibreSinais - Dia 3: Landmarks", tela)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

camera.release()
cv2.destroyAllWindows()
print()
print("Pronto! Agora você sabe o que o classificador vai 'ver'.")
print("Cada letra de Libras gera um padrão diferente de números.")
print("No próximo passo, vamos ensinar o ML a reconhecer esses padrões!")