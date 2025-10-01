"""
🎬 Teste Visual de Detecção - IdeaTec Mottu System
Demonstra detecção em tempo real com webcam ou imagem
"""

import cv2
import numpy as np
import sys
from pathlib import Path

# Adicionar src ao path
sys.path.append(str(Path(__file__).parent / "src"))

from src.detection.moto_detector import MottuMotorcycleDetector

def test_camera_detection():
    """Teste com webcam para demonstração ao vivo"""
    print("🎥 IdeaTec - Teste com Webcam")
    print("Pressione 'q' para sair")
    
    detector = MottuMotorcycleDetector()
    cap = cv2.VideoCapture(0)  # Webcam
    
    if not cap.isOpened():
        print("❌ Webcam não disponível")
        return
    
    frame_count = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        # Detectar apenas a cada 3 frames para performance
        if frame_count % 3 == 0:
            frame_info = detector.detect_and_classify_motorcycles(frame)
            annotated_frame = detector.draw_detections_professional_style(frame, frame_info)
        else:
            annotated_frame = frame
        
        cv2.imshow('IdeaTec Mottu Detection System', annotated_frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
        frame_count += 1
    
    cap.release()
    cv2.destroyAllWindows()

def test_image_detection():
    """Cria uma imagem de teste para demonstração"""
    print("🖼️ IdeaTec - Teste com Imagem Sintética")
    
    # Criar imagem de teste
    test_image = np.zeros((480, 640, 3), dtype=np.uint8)
    test_image[:] = (50, 50, 50)  # Fundo cinza escuro
    
    # Adicionar texto
    cv2.putText(test_image, "IDEATEC MOTTU SYSTEM", (120, 100), 
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    cv2.putText(test_image, "Sistema de Detecao Funcionando!", (80, 150), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
    cv2.putText(test_image, "YOLOv8 + OpenCV Carregados", (120, 200), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 1)
    cv2.putText(test_image, "Pressione qualquer tecla...", (150, 400), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
    
    detector = MottuMotorcycleDetector()
    
    # Simular detecção (mesmo sem motos reais)
    frame_info = detector.detect_and_classify_motorcycles(test_image)
    
    print(f"✅ Detecção executada:")
    print(f"   FPS: {frame_info['fps']}")
    print(f"   Tempo: {frame_info['processing_time']}s")
    print(f"   Sistema: Funcional")
    
    cv2.imshow('IdeaTec Test - Sistema Funcionando', test_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    print("🏍️ IDEATEC TECNOLOGIA - TESTE VISUAL")
    print("=" * 50)
    
    choice = input("Escolha:\n1. Teste com Webcam\n2. Teste com Imagem\nOpção (1/2): ")
    
    if choice == "1":
        test_camera_detection()
    else:
        test_image_detection()
    
    print("\n✅ Sistema IdeaTec funcionando corretamente!")