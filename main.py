"""
IDEATEC TECNOLOGIA - MOTTU VISION SYSTEM
Sistema de Mapeamento Inteligente do Pátio e Gestão das Motos

Desenvolvido por: IdeaTec Tecnologia
Cliente: Mottu - Soluções de Mobilidade
"""

import argparse
import sys
import os
from pathlib import Path

# Adicionar src ao path
sys.path.append(str(Path(__file__).parent / "src"))

def main():
    parser = argparse.ArgumentParser(
        description='🏍️ IdeaTec Tecnologia - Mottu Vision System',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
IDEATEC TECNOLOGIA - EXEMPLOS DE USO:
  python main.py --dashboard                    # Sistema completo (RECOMENDADO)
  python main.py --dashboard-integrated         # Dashboard integrado com API .NET
  python main.py --demo-image patio.jpg         # Testar detecção em imagem
  python main.py --demo-video patio.mp4         # Processar vídeo do pátio
  python main.py --demo-iot                     # Simular sensores IoT Mottu
  python main.py --sistema-report               # Gerar relatório do sistema

EMPRESA: IdeaTec Tecnologia - Especialistas em Visão Computacional
CLIENTE: Mottu - Sistema de Mapeamento Inteligente do Pátio
INTEGRAÇÃO: API .NET Sprint para persistência robusta
        """
    )
    
    parser.add_argument('--dashboard', action='store_true',
                       help='Iniciar dashboard completo do sistema')
    parser.add_argument('--dashboard-integrated', action='store_true',
                       help='Iniciar dashboard integrado com API .NET')
    parser.add_argument('--demo-image', type=str,
                       help='Testar detecção em imagem específica')
    parser.add_argument('--demo-video', type=str,
                       help='Processar vídeo do pátio')
    parser.add_argument('--demo-iot', action='store_true',
                       help='Executar simulação IoT das motos Mottu')
    parser.add_argument('--sistema-report', action='store_true',
                       help='Gerar relatório específico do sistema')
    parser.add_argument('--confidence', type=float, default=0.4,
                       help='Threshold de confiança para detecção (0.1-1.0)')
    
    args = parser.parse_args()
    
    print("🏍️ IDEATEC TECNOLOGIA - MOTTU VISION SYSTEM")
    print("=" * 60)
    print("🏢 Empresa: IdeaTec Tecnologia")
    print("🤝 Cliente: Mottu - Soluções de Mobilidade")
    print("🎯 Sistema: Mapeamento Inteligente do Pátio")
    print("=" * 60)
    
    if args.dashboard:
        print("🚀 Iniciando sistema completo IdeaTec...")
        print("📍 Acesse: http://localhost:8501")
        print("💡 Sistema pronto para demonstração operacional!")
        os.system("streamlit run src/dashboard/mottu_app.py")
        
    elif args.dashboard_integrated:
        print("🚀 Iniciando dashboard integrado IdeaTec + API .NET...")
        print("📍 Acesse: http://localhost:8501")
        print("🔗 Integração com API .NET Sprint ativa!")
        print("💡 Sistema completo pronto para produção!")
        os.system("streamlit run src/dashboard/integrated_dashboard.py")
        
    elif args.demo_image:
        print(f"🖼️ DEMO IdeaTec: Detecção de motos - {args.demo_image}")
        from src.detection.moto_detector import MottuMotorcycleDetector
        import cv2
        
        detector = MottuMotorcycleDetector()
        detector.confidence_threshold = args.confidence
        
        image = cv2.imread(args.demo_image)
        if image is None:
            print(f"❌ ERRO: Imagem não encontrada - {args.demo_image}")
            print("💡 Use imagens de pátios de motos para melhores resultados")
            return
        
        print("🔍 IdeaTec processando detecção e classificação...")
        frame_info = detector.detect_and_classify_motorcycles(image)
        annotated_image = detector.draw_detections_professional_style(image, frame_info)
        
        print(f"✅ RESULTADOS IDEATEC:")
        print(f"   🏍️ Motos detectadas: {frame_info['motorcycles_count']}")
        print(f"   🚗 Total de veículos: {frame_info['total_detections']}")
        print(f"   ⚡ FPS: {frame_info['fps']}")
        print(f"   🎯 Modelos identificados: {frame_info['sistema_metrics']['models_variety']}")
        
        cv2.imshow('IdeaTec Tecnologia - Mottu Vision', annotated_image)
        print("⌨️ Pressione qualquer tecla para continuar...")
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        
    elif args.demo_video:
        print(f"🎥 DEMO IdeaTec: Processamento de vídeo - {args.demo_video}")
        from src.detection.moto_detector import MottuMotorcycleDetector
        from src.detection.video_processor import MottuVideoProcessor
        
        detector = MottuMotorcycleDetector()
        detector.confidence_threshold = args.confidence
        processor = MottuVideoProcessor(detector)
        
        print("🎬 IdeaTec processando vídeo para demonstração...")
        report = processor.process_patio_video(args.demo_video, max_frames=200)
        
        print(f"✅ PROCESSAMENTO IDEATEC CONCLUÍDO!")
        print(f"📊 Métricas do sistema:")
        print(f"   🏍️ Total de motos: {report['summary']['total_motorcycles_detected']}")
        print(f"   📹 Frames processados: {report['summary']['total_frames_processed']}")
        print(f"   ⚡ FPS médio: {report['summary']['average_fps']}")
        
    elif args.demo_iot:
        print("📡 DEMO IdeaTec: Simulação IoT das motos Mottu")
        from src.simulation.iot_simulator import MottuIoTSimulator
        
        print("🔄 IdeaTec iniciando simulação da frota Mottu...")
        simulator = MottuIoTSimulator()
        
        print("📊 Status inicial da frota:")
        initial_status = simulator.get_current_fleet_status()
        print(f"   🏍️ Total de motos: {initial_status['total_motos']}")
        print(f"   📊 Distribuição: {initial_status['fleet_summary']}")
        
        print("⏱️ Executando simulação por 30 segundos...")
        simulator.simulate_real_time_data(30)
        
        final_status = simulator.get_current_fleet_status()
        print(f"✅ SIMULAÇÃO IDEATEC CONCLUÍDA!")
        print(f"📊 Status final: {final_status['fleet_summary']}")
        
    elif args.sistema_report:
        print("📋 IdeaTec gerando relatório do sistema...")
        from src.detection.moto_detector import MottuMotorcycleDetector
        
        # Exemplo com dados de teste
        detector = MottuMotorcycleDetector()
        
        # Simular algumas detecções para o relatório
        print("🔄 Simulando detecções para demonstração...")
        import numpy as np
        
        # Dados simulados para o relatório
        for i in range(5):
            mock_detection = {
                'total_detections': np.random.randint(3, 8),
                'motorcycles_count': np.random.randint(2, 6),
                'detections': [
                    {
                        'class': 'motorcycle',
                        'confidence': np.random.uniform(0.6, 0.95),
                        'modelo_mottu': np.random.choice(detector.mottu_models),
                        'zona_patio': f"ZONA_{np.random.choice(['A', 'B', 'C'])}_{'NORTE' if np.random.random() > 0.5 else 'SUL'}"
                    } for _ in range(np.random.randint(2, 5))
                ],
                'fps': np.random.uniform(15, 25),
                'sistema_metrics': {
                    'models_variety': np.random.randint(2, 4),
                    'zones_coverage': np.random.randint(3, 6),
                    'highest_confidence': np.random.uniform(0.8, 0.95)
                }
            }
            detector.detection_history.append(mock_detection)
        
        report = detector.generate_sistema_report()
        
        print("📄 RELATÓRIO IDEATEC GERADO:")
        print("=" * 50)
        print(f"🎯 Projeto: {report['sistema_summary']['projeto']}")
        print(f"🏢 Empresa: {report['sistema_summary']['empresa']}")
        print(f"🤝 Cliente: {report['sistema_summary']['cliente']}")
        print(f"🏍️ Motos detectadas: {report['sistema_summary']['total_motorcycles_detected']}")
        print(f"🎨 Modelos identificados: {report['sistema_summary']['unique_models_identified']}")
        print(f"🗺️ Zonas cobertas: {report['sistema_summary']['patio_zones_coverage']}")
        print(f"🎯 Precisão estimada: {report['sistema_summary']['detection_accuracy_estimate']}")
        print(f"⭐ Performance: {report['mottu_insights']['performance_rating']}")
        
        # Salvar relatório
        import json
        # Converter numpy int64 para int padrão
        def convert_numpy_types(obj):
            if hasattr(obj, 'item'):
                return obj.item()
            return obj
        
        # Serializar com conversão de tipos numpy
        report_json = json.loads(json.dumps(report, default=convert_numpy_types))
        
        with open('ideatec_sistema_report.json', 'w', encoding='utf-8') as f:
            json.dump(report_json, f, indent=2, ensure_ascii=False)
        print(f"💾 Relatório IdeaTec salvo em: ideatec_sistema_report.json")
        
    else:
        print("ℹ️ Use --help para ver todas as opções disponíveis")
        print("🚀 RECOMENDADO PARA DEMONSTRAÇÃO: python main.py --dashboard")
        print("")
        print("🎥 Para demonstração do sistema, execute:")
        print("   1. Dashboard completo com detecção em tempo real")
        print("   2. Simulação IoT da frota Mottu")
        print("   3. Métricas e relatórios de performance")
        print("   4. Mapeamento digital do pátio com zonas")
        print("")
        print("🏢 Desenvolvido por IdeaTec Tecnologia")
        print("🤝 Especialistas em Visão Computacional e IoT")

if __name__ == "__main__":
    main()
