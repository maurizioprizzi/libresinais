"""
stabilizer.py - Buffer de confiança e estabilização

Responsável por:
- Manter um buffer dos últimos N resultados de classificação
- Só confirmar um sinal quando houver N frames consecutivos iguais
- Evitar flickering (trocar de letra a cada frame)
- Detectar pausas entre letras na datilologia

TODO: Implementar na Fase 1
"""
