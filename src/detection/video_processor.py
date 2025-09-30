import cv2
import numpy as np
from typing import Optional, Dict
import time
import os
from .moto_detector import MottuMotorcycleDetector

class MottuVideoProcessor:
    def __init__(self, detector: MottuMotorcycleDetector):
        self.detector = detector
        
    def process_patio_video(self, video_path: str, output_path: Optional[str] = None, 
                          max_frames: int = 300) -> Dict:
        """Processa vídeo do pátio com limite de frames para demonstração"""
        if not os.path.exists(video_path):
            raise FileNotFoundError(f"Vídeo não encontrado: {video_path}")
        
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            raise ValueError(f"Erro ao abrir vídeo: {video_path}")
        
        # Propriedades do vídeo
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        total_frames = min(int(cap.get(cv2.CAP_PROP_FRAME_COUNT)), max_frames)
        
        print(f"📹 IdeaTec processando: {total_frames} frames @ {fps} FPS")
        
        # Configurar gravação
        writer = None
        if output_path:
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            writer = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
        
        processing_stats = []
        frame_count = 0
        
        try:
            while frame_count < max_frames:
                ret, frame = cap.read()
                if not ret:
                    break
                
                # CORREÇÃO: Usar o método correto do detector
                frame_info = self.detector.detect_and_classify_motorcycles(frame)
                
                # Anotar frame
                annotated_frame = self.detector.draw_detections_professional_style(frame, frame_info)
                
                # Adicionar informações do progresso
                progress_text = f"IdeaTec Frame: {frame_count+1}/{total_frames} ({(frame_count/total_frames)*100:.1f}%)"
                cv2.putText(annotated_frame, progress_text, (width-400, height-20), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
                
                # Salvar frame anotado
                if writer:
                    writer.write(annotated_frame)
                
                processing_stats.append(frame_info)
                frame_count += 1
                
                # Log de progresso
                if frame_count % 30 == 0:
                    print(f"✅ IdeaTec processado: {frame_count}/{total_frames} frames")
        
        finally:
            cap.release()
            if writer:
                writer.release()
            cv2.destroyAllWindows()
        
        # Gerar relatório final
        report = self._generate_processing_report(processing_stats, frame_count)
        print(f"🎯 IdeaTec processamento concluído: {report['summary']['total_motorcycles_detected']} motos detectadas")
        
        return report
    
    def process_realtime_demo(self, camera_index: int = 0, demo_duration: int = 60):
        """Demonstração em tempo real com webcam"""
        cap = cv2.VideoCapture(camera_index)
        if not cap.isOpened():
            print("❌ Erro: Não foi possível acessar a webcam")
            return
        
        print(f"📷 IdeaTec iniciando demo em tempo real por {demo_duration} segundos...")
        print("Pressione 'q' para sair antecipadamente")
        
        start_time = time.time()
        frame_count = 0
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            # CORREÇÃO: Usar o método correto do detector
            frame_info = self.detector.detect_and_classify_motorcycles(frame)
            annotated_frame = self.detector.draw_detections_professional_style(frame, frame_info)
            
            # Timer da demo
            elapsed_time = time.time() - start_time
            remaining_time = max(0, demo_duration - elapsed_time)
            
            timer_text = f"IdeaTec Demo Time: {remaining_time:.1f}s"
            cv2.putText(annotated_frame, timer_text, (10, frame.shape[0] - 20), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
            
            cv2.imshow('IdeaTec Tecnologia - Mottu Vision Demo', annotated_frame)
            
            # Verificar saída
            if cv2.waitKey(1) & 0xFF == ord('q') or elapsed_time >= demo_duration:
                break
            
            frame_count += 1
        
        cap.release()
        cv2.destroyAllWindows()
        print(f"✅ IdeaTec demo finalizada: {frame_count} frames processados")
    
    def _generate_processing_report(self, stats: list, total_frames: int) -> Dict:
        """Gera relatório detalhado do processamento"""
        if not stats:
            return {"error": "Nenhum frame processado"}
        
        total_motorcycles = sum(frame['motorcycles_count'] for frame in stats)
        avg_fps = np.mean([frame['fps'] for frame in stats])
        avg_processing_time = np.mean([frame['processing_time'] for frame in stats])
        
        # Análise temporal
        motorcycle_timeline = [frame['motorcycles_count'] for frame in stats]
        max_motorcycles = max(motorcycle_timeline)
        min_motorcycles = min(motorcycle_timeline)
        
        return {
            'summary': {
                'projeto': 'IdeaTec Tecnologia - Processamento de Vídeo',
                'total_frames_processed': total_frames,
                'total_motorcycles_detected': total_motorcycles,
                'max_motorcycles_in_frame': max_motorcycles,
                'min_motorcycles_in_frame': min_motorcycles,
                'average_motorcycles_per_frame': round(total_motorcycles / total_frames, 2),
                'average_fps': round(avg_fps, 1),
                'average_processing_time': round(avg_processing_time, 3),
                'total_processing_time': round(sum(frame['processing_time'] for frame in stats), 2)
            },
            'timeline': motorcycle_timeline,
            'detailed_stats': stats[-5:],  # Últimos 5 frames
            'generated_at': time.strftime('%Y-%m-%d %H:%M:%S')
        }
