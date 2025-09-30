import streamlit as st
import cv2
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from PIL import Image
import sys
import os
import threading
import time
import json

# Adicionar src ao path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from detection.moto_detector import MottuMotorcycleDetector
from detection.video_processor import MottuVideoProcessor
from simulation.iot_simulator import MottuIoTSimulator

def process_image_for_yolo(image):
    """
    Converte imagem para formato compatível com YOLO (3 canais RGB)
    """
    # Se imagem PIL, converter para numpy
    if hasattr(image, 'mode'):
        # Converter RGBA para RGB se necessário
        if image.mode == 'RGBA':
            # Criar fundo branco
            background = Image.new('RGB', image.size, (255, 255, 255))
            background.paste(image, mask=image.split()[3])  # Usar canal alpha como máscara
            image = background
        elif image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Converter PIL para numpy array
        image_np = np.array(image)
    else:
        # Se já é numpy array
        image_np = image
    
    # Verificar número de canais
    if len(image_np.shape) == 3:
        if image_np.shape[2] == 4:  # RGBA
            # Converter RGBA para RGB removendo canal alpha
            image_np = image_np[:, :, :3]
        elif image_np.shape[2] != 3:
            # Se não é RGB nem RGBA, forçar para 3 canais
            if image_np.shape[2] == 1:  # Grayscale
                image_np = np.repeat(image_np, 3, axis=2)
    
    # Garantir que está no formato correto (height, width, 3)
    if len(image_np.shape) == 2:  # Grayscale sem dimensão de canal
        image_np = np.stack([image_np] * 3, axis=-1)
    
    # Verificação final
    if image_np.shape[2] != 3:
        raise ValueError(f"Erro: Imagem tem {image_np.shape[2]} canais, YOLO precisa de 3 canais RGB")
    
    return image_np

def main():
    st.set_page_config(
        page_title="IdeaTec Tecnologia - Mottu Vision",
        page_icon="🏍️",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # CSS personalizado IdeaTec
    st.markdown("""
    <style>
    .main-header {
        background: linear-gradient(90deg, #FF6B6B, #4ECDC4);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    .ideatec-box {
        background: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #FF6B6B;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Header principal IdeaTec
    st.markdown('''
    <div class="main-header">
        <h1>🏍️ IdeaTec Tecnologia - Mottu Vision System</h1>
        <p>Sistema Inteligente de Detecção e Gestão de Motos</p>
        <p><strong>Cliente:</strong> Mottu | <strong>Projeto:</strong> Mapeamento Inteligente do Pátio</p>
    </div>
    ''', unsafe_allow_html=True)
    
    # Sidebar IdeaTec
    st.sidebar.header("⚙️ Configurações IdeaTec")
    st.sidebar.markdown("**Especialistas em Visão Computacional**")
    
    confidence_threshold = st.sidebar.slider("Confiança Mínima", 0.1, 1.0, 0.4, 0.1)
    max_frames = st.sidebar.slider("Máximo de Frames", 50, 500, 200, 50)
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("**🏢 IdeaTec Tecnologia**")
    st.sidebar.markdown("📧 contato@ideatec.tech")
    st.sidebar.markdown("🌐 www.ideatec.tech")
    
    # Inicializar componentes
    @st.cache_resource
    def load_detector():
        return MottuMotorcycleDetector()
    
    @st.cache_resource  
    def load_iot_simulator():
        return MottuIoTSimulator()
    
    detector = load_detector()
    detector.confidence_threshold = confidence_threshold
    iot_simulator = load_iot_simulator()
    
    # Tabs principais
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📷 Detecção de Imagens", 
        "🎥 Processamento de Vídeo", 
        "📡 Simulação IoT", 
        "📊 Analytics & Relatórios",
        "ℹ️ IdeaTec Tecnologia"
    ])
    
    with tab1:
        st.header("🖼️ Detecção Inteligente de Motos - IdeaTec")
        
        uploaded_file = st.file_uploader(
            "📤 Faça upload de uma imagem do pátio Mottu",
            type=['jpg', 'jpeg', 'png'],
            help="Sistema IdeaTec otimizado para pátios de motos"
        )
        
        if uploaded_file is not None:
            try:
                # Carregar imagem
                image = Image.open(uploaded_file)
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.subheader("📷 Imagem Original")
                    # CORREÇÃO: usar use_container_width ao invés de use_column_width
                    st.image(image, use_container_width=True)
                    st.info(f"**Dimensões:** {image.width} x {image.height} pixels")
                    
                    # Mostrar informações de canal
                    if hasattr(image, 'mode'):
                        st.info(f"**Formato:** {image.mode}")
                
                with col2:
                    st.subheader("🎯 Análise IdeaTec")
                    
                    with st.spinner("🔍 IdeaTec analisando imagem..."):
                        # CORREÇÃO: Processar imagem para garantir compatibilidade com YOLO
                        image_processed = process_image_for_yolo(image)
                        
                        # Verificar se processamento foi bem-sucedido
                        st.success(f"✅ Imagem processada: {image_processed.shape[2]} canais")
                        
                        # Detectar motos
                        frame_info = detector.detect_and_classify_motorcycles(image_processed)
                        annotated_image = detector.draw_detections_professional_style(image_processed, frame_info)
                    
                    # CORREÇÃO: usar use_container_width
                    st.image(annotated_image, use_container_width=True)
                    
                    # Métricas IdeaTec
                    col2_1, col2_2, col2_3 = st.columns(3)
                    with col2_1:
                        st.metric("🏍️ Motos Detectadas", frame_info['motorcycles_count'])
                    with col2_2:
                        st.metric("🚗 Total Veículos", frame_info['total_detections'])
                    with col2_3:
                        st.metric("⚡ Tempo Proc.", f"{frame_info['processing_time']}s")
                
                # Detalhes IdeaTec
                if frame_info['detections']:
                    st.subheader("📋 Análise Detalhada IdeaTec")
                    
                    detection_df = pd.DataFrame([
                        {
                            'ID Mottu': det['id'],
                            'Tipo': det['class'],
                            'Modelo': det.get('modelo_mottu', 'N/A'),
                            'Confiança': f"{det['confidence']:.2%}",
                            'Zona Pátio': det.get('zona_patio', 'N/A'),
                            'Posição X': det['center'][0],
                            'Posição Y': det['center'][1]
                        }
                        for det in frame_info['detections']
                    ])
                    
                    st.dataframe(detection_df, use_container_width=True)
                
            except Exception as e:
                st.error(f"❌ Erro ao processar imagem: {str(e)}")
                st.info("💡 Tente usar uma imagem JPG sem transparência ou uma imagem PNG com 3 canais")
    
    with tab2:
        st.header("🎬 Processamento de Vídeo IdeaTec")
        
        video_file = st.file_uploader(
            "📹 Upload vídeo do pátio Mottu",
            type=['mp4', 'avi', 'mov'],
            help="Sistema IdeaTec para análise de vídeos em tempo real"
        )
        
        if video_file is not None:
            st.info(f"📁 **Arquivo:** {video_file.name} ({video_file.size / 1024 / 1024:.1f} MB)")
            
            if st.button("🚀 Processar com IdeaTec", type="primary"):
                temp_video_path = f"temp_{video_file.name}"
                with open(temp_video_path, "wb") as f:
                    f.write(video_file.read())
                
                processor = MottuVideoProcessor(detector)
                
                with st.spinner(f"⚙️ IdeaTec processando {max_frames} frames..."):
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    
                    try:
                        for i in range(max_frames):
                            progress = (i + 1) / max_frames
                            progress_bar.progress(progress)
                            status_text.text(f"IdeaTec processando frame {i+1}/{max_frames}")
                            time.sleep(0.01)
                        
                        output_path = f"output_{video_file.name}"
                        report = processor.process_patio_video(temp_video_path, output_path, max_frames)
                        
                        st.success("✅ Processamento IdeaTec concluído!")
                        
                        summary = report['summary']
                        col3, col4, col5, col6 = st.columns(4)
                        with col3:
                            st.metric("🎞️ Frames", summary['total_frames_processed'])
                        with col4:
                            st.metric("🏍️ Motos", summary['total_motorcycles_detected'])
                        with col5:
                            st.metric("📊 FPS Médio", summary['average_fps'])
                        with col6:
                            st.metric("⏱️ Tempo Total", f"{summary['total_processing_time']}s")
                        
                        if 'timeline' in report:
                            fig = px.line(
                                x=list(range(len(report['timeline']))),
                                y=report['timeline'],
                                title="📈 Análise Temporal IdeaTec - Motos por Frame",
                                labels={'x': 'Frame', 'y': 'Número de Motos'}
                            )
                            st.plotly_chart(fig, use_container_width=True)
                        
                    except Exception as e:
                        st.error(f"❌ Erro no processamento IdeaTec: {str(e)}")
                    finally:
                        if os.path.exists(temp_video_path):
                            os.remove(temp_video_path)
    
    with tab3:
        st.header("📡 Simulação IoT IdeaTec")
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.subheader("🚀 Controle IdeaTec")
            
            if st.button("▶️ Iniciar Simulação IdeaTec", type="primary"):
                with st.spinner("🔄 IdeaTec gerando dados simulados..."):
                    simulation_thread = threading.Thread(
                        target=iot_simulator.simulate_real_time_data,
                        args=(10,)
                    )
                    simulation_thread.start()
                    time.sleep(12)
                
                st.success("✅ Simulação IdeaTec concluída!")
        
        with col2:
            st.subheader("📊 Status Frota Mottu")
            
            fleet_status = iot_simulator.get_current_fleet_status()
            
            col2_1, col2_2 = st.columns(2)
            with col2_1:
                st.metric("🏍️ Total Motos", fleet_status['total_motos'])
            with col2_2:
                available = fleet_status['fleet_summary'].get('disponivel', 0)
                st.metric("✅ Disponíveis", available)
            
            status_data = fleet_status['fleet_summary']
            if status_data:
                fig = px.pie(
                    values=list(status_data.values()),
                    names=list(status_data.keys()),
                    title="📊 IdeaTec - Status da Frota Mottu"
                )
                st.plotly_chart(fig, use_container_width=True)
        
        st.subheader("🗂️ Monitoramento IdeaTec - Frota Detalhada")
        
        fleet_df = pd.DataFrame([
            {
                'ID Mottu': moto['id'],
                'Modelo': moto['model'],
                'Status': moto['status'],
                'Bateria (%)': moto['battery_level'],
                'Combustível (%)': moto['fuel_level'],
                'Zona': moto['position']['zone'],
                'Posição X': moto['position']['x'],
                'Posição Y': moto['position']['y'],
                'Odômetro (km)': moto['odometer']
            }
            for moto in fleet_status['motos_data']
        ])
        
        st.dataframe(fleet_df, use_container_width=True)
    
    with tab4:
        st.header("📈 Analytics IdeaTec")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🎯 Métricas de Detecção")
            
            if detector.detection_history:
                detection_report = detector.generate_sistema_report()
                summary = detection_report['sistema_summary']
                
                st.metric("📊 Frames Processados", summary['total_frames_processed'])
                st.metric("🏍️ Motos Detectadas", summary['total_motorcycles_detected'])
                st.metric("⚡ FPS Médio", summary['average_fps'])
                st.metric("🎯 Precisão", summary['detection_accuracy_estimate'])
                
                with st.expander("📄 Relatório Completo IdeaTec"):
                    st.json(detection_report)
            else:
                st.info("ℹ️ Execute detecções para visualizar métricas IdeaTec")
        
        with col2:
            st.subheader("🏭 Analytics Frota IoT")
            
            fleet_status = iot_simulator.get_current_fleet_status()
            
            battery_data = [moto['battery_level'] for moto in fleet_status['motos_data']]
            fuel_data = [moto['fuel_level'] for moto in fleet_status['motos_data']]
            
            fig_battery = px.histogram(
                x=battery_data,
                nbins=10,
                title="📋 IdeaTec - Níveis de Bateria",
                labels={'x': 'Nível da Bateria (%)', 'y': 'Quantidade'}
            )
            st.plotly_chart(fig_battery, use_container_width=True)
        
        # Mapa digital do pátio
        st.subheader("🗺️ Mapa Digital IdeaTec - Pátio Mottu")
        
        patio_data = []
        for moto in fleet_status['motos_data']:
            patio_data.append({
                'x': moto['position']['x'],
                'y': moto['position']['y'],
                'id': moto['id'],
                'status': moto['status'],
                'battery': moto['battery_level']
            })
        
        if patio_data:
            patio_df = pd.DataFrame(patio_data)
            
            fig_patio = px.scatter(
                patio_df,
                x='x',
                y='y',
                color='status',
                size='battery',
                hover_data=['id', 'battery'],
                title="🏍️ IdeaTec - Posicionamento Inteligente das Motos",
                labels={'x': 'Posição X', 'y': 'Posição Y'}
            )
            
            fig_patio.update_layout(
                xaxis=dict(range=[0, 800]),
                yaxis=dict(range=[0, 600]),
                height=400
            )
            
            st.plotly_chart(fig_patio, use_container_width=True)
    
    with tab5:
        st.header("ℹ️ IdeaTec Tecnologia")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🎯 Sobre a IdeaTec")
            st.write("""
            **IdeaTec Tecnologia** é uma empresa especializada em soluções de **Visão Computacional** 
            e **Internet das Coisas (IoT)**, focada em transformar desafios operacionais em 
            oportunidades tecnológicas.
            
            **Especialidades:**
            - ✅ Visão Computacional com IA
            - ✅ Sistemas IoT integrados
            - ✅ Análise de dados em tempo real
            - ✅ Dashboards operacionais
            - ✅ Soluções escaláveis
            """)
            
            st.subheader("🛠️ Tecnologias IdeaTec")
            st.write("""
            **Stack Tecnológico:**
            - 🤖 YOLOv8 para detecção avançada
            - 👁️ OpenCV para processamento de imagem
            - 🐍 Python para desenvolvimento
            - 📡 MQTT para comunicação IoT
            - 🌐 Streamlit para interfaces web
            - 📊 Plotly para visualizações
            """)
        
        with col2:
            st.subheader("🤝 Projeto Mottu")
            st.write("""
            **Cliente:** Mottu - Líder em Mobilidade Urbana
            
            **Desafio:** Gestão manual de frotas em +100 filiais 
            gerando imprecisões operacionais críticas.
            
            **Solução IdeaTec:**
            - 🏍️ Detecção inteligente de motos
            - 🗺️ Mapeamento digital de pátios
            - 📱 Interface web responsiva
            - 📡 Simulação IoT realística
            - 📊 Analytics operacionais
            """)
            
            st.subheader("📈 Resultados Esperados")
            st.write("""
            **Benefícios para Mottu:**
            - 📊 60% redução tempo de localização
            - 🎯 95%+ precisão no inventário
            - 🚀 Escalabilidade para 100+ filiais
            - 💰 ROI estimado em 18 meses
            - ⚡ Operação em tempo real
            """)
        
        st.success("""
        💡 **IdeaTec Tecnologia** - Transformando o futuro da gestão de frotas através de 
        tecnologias disruptivas de Visão Computacional e IoT.
        """)

if __name__ == "__main__":
    main()
