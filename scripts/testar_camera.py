"""
testar_camera.py - Testa a webcam com detecção de mãos via MediaPipe

Este é o primeiro script funcional do LibreSinais!
Ele abre a webcam, detecta suas mãos e desenha os 21 pontos
de referência (landmarks) na tela em tempo real.

Como usar:
    1. Ative o ambiente virtual: source venv/bin/activate
    2. Rode: python scripts/testar_camera.py
    3. Mostre suas mãos para a câmera
    4. Aperte 'q' para sair

O que você vai ver:
    - Pontos verdes em cada articulação da mão (21 por mão)
    - Linhas conectando os pontos (esqueleto da mão)
    - No canto da tela: quantas mãos foram detectadas

Isso é a BASE de tudo — o MediaPipe "enxerga" suas mãos
e nos dá as coordenadas de cada dedo. Depois, vamos usar
essas coordenadas para classificar os sinais de Libras.
"""

import cv2
import mediapipe as mp

# --- Configuração do MediaPipe ---
# mp_hands: módulo de detecção de mãos
# mp_drawing: módulo para desenhar os pontos na tela
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

# --- Abrir a webcam ---
# 0 = câmera padrão do computador
# Se você tiver mais de uma câmera, tente 1, 2, etc.
camera = cv2.VideoCapture(0)

if not camera.isOpened():
    print("ERRO: Não foi possível abrir a câmera!")
    print("Verifique se sua webcam está conectada e funcionando.")
    exit(1)

print("=" * 50)
print("  LibreSinais - Teste de Câmera + MediaPipe")
print("=" * 50)
print()
print("  Mostre suas mãos para a câmera!")
print("  Aperte 'q' para sair.")
print()

# --- Iniciar o detector de mãos ---
# max_num_hands=2: detecta até 2 mãos
# min_detection_confidence=0.7: confiança mínima para detectar
# min_tracking_confidence=0.5: confiança mínima para rastrear
with mp_hands.Hands(
    max_num_hands=2,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.5
) as hands:

    while True:
        # Ler um frame da câmera
        sucesso, frame = camera.read()
        if not sucesso:
            print("Erro ao ler frame da câmera.")
            break

        # Espelhar a imagem (como um espelho, mais natural)
        frame = cv2.flip(frame, 1)

        # Converter de BGR (OpenCV) para RGB (MediaPipe)
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Processar o frame com MediaPipe
        resultado = hands.process(frame_rgb)

        # --- Desenhar os landmarks na tela ---
        num_maos = 0

        if resultado.multi_hand_landmarks:
            num_maos = len(resultado.multi_hand_landmarks)

            for mao_landmarks in resultado.multi_hand_landmarks:
                # Desenhar os pontos e conexões
                mp_drawing.draw_landmarks(
                    frame,
                    mao_landmarks,
                    mp_hands.HAND_CONNECTIONS,
                    mp_drawing_styles.get_default_hand_landmarks_style(),
                    mp_drawing_styles.get_default_hand_connections_style()
                )

        # --- Mostrar informações na tela ---
        # Fundo semi-transparente para o texto
        cv2.rectangle(frame, (0, 0), (350, 90), (0, 0, 0), -1)

        # Título
        cv2.putText(
            frame, "LibreSinais - Teste",
            (10, 30), cv2.FONT_HERSHEY_SIMPLEX,
            0.8, (0, 255, 128), 2
        )

        # Quantidade de mãos detectadas
        cor_maos = (0, 255, 0) if num_maos > 0 else (0, 0, 255)
        cv2.putText(
            frame, f"Maos detectadas: {num_maos}",
            (10, 65), cv2.FONT_HERSHEY_SIMPLEX,
            0.7, cor_maos, 2
        )

        # Instrução
        cv2.putText(
            frame, "Aperte 'q' para sair",
            (10, frame.shape[0] - 15), cv2.FONT_HERSHEY_SIMPLEX,
            0.5, (200, 200, 200), 1
        )

        # Mostrar o frame na janela
        cv2.imshow("LibreSinais - Teste de Camera", frame)

        # Verificar se 'q' foi pressionado
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

# --- Limpeza ---
camera.release()
cv2.destroyAllWindows()
print()
print("Câmera fechada. Até a próxima!")