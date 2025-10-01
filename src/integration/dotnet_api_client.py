"""
IDEATEC TECNOLOGIA - INTEGRAÇÃO API .NET
Módulo de integração com a API .NET Sprint para dados de motos e pátios

Desenvolvido por: IdeaTec Tecnologia
Integração: API .NET Sprint + Mottu Vision System
"""

import requests
import json
from typing import Dict, List, Optional
from datetime import datetime
import time

class DotNetApiClient:
    """Cliente para integração com API .NET Sprint"""
    
    def __init__(self, base_url: str = "http://localhost:5000/api"):
        """Inicializa cliente da API .NET"""
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'User-Agent': 'IdeaTec-Mottu-Vision/1.0'
        })
    
    # ================================
    # MOTOS - OPERAÇÕES CRUD
    # ================================
    
    def get_motos(self, page: int = 1, page_size: int = 50) -> Dict:
        """Busca motos da API .NET com paginação"""
        try:
            response = self.session.get(
                f"{self.base_url}/moto",
                params={'pageNumber': page, 'pageSize': page_size}
            )
            response.raise_for_status()
            
            motos = response.json()
            total_count = response.headers.get('X-Total-Count', '0')
            
            return {
                'motos': motos,
                'total': int(total_count),
                'page': page,
                'success': True
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def get_moto_by_id(self, moto_id: int) -> Dict:
        """Busca moto específica por ID"""
        try:
            response = self.session.get(f"{self.base_url}/moto/{moto_id}")
            response.raise_for_status()
            return {'moto': response.json(), 'success': True}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def create_moto_from_detection(self, detection_data: Dict, patio_id: int = 1) -> Dict:
        """Cria moto baseada nos dados de detecção do sistema de visão"""
        try:
            moto_data = {
                'placa': f"DETECT-{int(time.time())}",  # Placa temporária
                'cor': 'Detectada',
                'status': 'detected',
                'locationX': detection_data.get('center_x', 0),
                'locationY': detection_data.get('center_y', 0),
                'batteryLevel': 85,  # Simulado
                'fuelLevel': 90,     # Simulado
                'mileage': 1500,     # Simulado
                'assignedBranch': 'Pátio Principal',
                'technicalInfo': f"Detectada por IdeaTec Vision System - Confiança: {detection_data.get('confidence', 0.0):.2f}",
                'modeloId': 1,  # Modelo padrão
                'patioId': patio_id
            }
            
            response = self.session.post(f"{self.base_url}/moto", json=moto_data)
            response.raise_for_status()
            
            return {'moto': response.json(), 'success': True}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def update_moto_location(self, moto_id: int, x: float, y: float) -> Dict:
        """Atualiza localização da moto baseada na detecção visual"""
        try:
            # Primeiro busca a moto atual
            moto_response = self.get_moto_by_id(moto_id)
            if not moto_response['success']:
                return moto_response
            
            moto = moto_response['moto']
            
            # Atualiza dados de localização
            update_data = {
                'placa': moto['placa'],
                'cor': moto['cor'],
                'status': 'tracked',  # Status atualizado para rastreada
                'locationX': x,
                'locationY': y,
                'batteryLevel': moto.get('batteryLevel', 85),
                'fuelLevel': moto.get('fuelLevel', 90),
                'mileage': moto.get('mileage', 1500),
                'assignedBranch': moto.get('assignedBranch', 'Pátio Principal'),
                'technicalInfo': f"{moto.get('technicalInfo', '')} | Atualizado: {datetime.now().isoformat()}",
                'modeloId': moto['modeloId'],
                'patioId': moto['patioId']
            }
            
            response = self.session.put(f"{self.base_url}/moto/{moto_id}", json=update_data)
            response.raise_for_status()
            
            return {'success': True, 'updated': True}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    # ================================
    # PÁTIOS - OPERAÇÕES CRUD
    # ================================
    
    def get_patios(self, page: int = 1, page_size: int = 20) -> Dict:
        """Busca pátios da API .NET"""
        try:
            response = self.session.get(
                f"{self.base_url}/patio",
                params={'pageNumber': page, 'pageSize': page_size}
            )
            response.raise_for_status()
            
            patios = response.json()
            total_count = response.headers.get('X-Total-Count', '0')
            
            return {
                'patios': patios,
                'total': int(total_count),
                'success': True
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def create_patio(self, nome: str, localizacao: str) -> Dict:
        """Cria novo pátio na API .NET"""
        try:
            patio_data = {
                'nome': nome,
                'localizacao': localizacao
            }
            
            response = self.session.post(f"{self.base_url}/patio", json=patio_data)
            response.raise_for_status()
            
            return {'patio': response.json(), 'success': True}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    # ================================
    # MODELOS - OPERAÇÕES
    # ================================
    
    def get_modelos(self) -> Dict:
        """Busca modelos de motos disponíveis"""
        try:
            response = self.session.get(f"{self.base_url}/modelo")
            response.raise_for_status()
            return {'modelos': response.json(), 'success': True}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    # ================================
    # SINCRONIZAÇÃO COM SISTEMA VISÃO
    # ================================
    
    def sync_detections_with_database(self, detections: List[Dict]) -> Dict:
        """Sincroniza detecções do sistema de visão com banco de dados"""
        results = {
            'synced': 0,
            'errors': 0,
            'details': []
        }
        
        for detection in detections:
            # Criar/atualizar moto baseada na detecção
            result = self.create_moto_from_detection(detection)
            
            if result['success']:
                results['synced'] += 1
                results['details'].append({
                    'detection_id': detection.get('id'),
                    'moto_id': result['moto']['id'],
                    'status': 'created'
                })
            else:
                results['errors'] += 1
                results['details'].append({
                    'detection_id': detection.get('id'),
                    'error': result['error'],
                    'status': 'failed'
                })
        
        return results
    
    def get_fleet_analytics(self) -> Dict:
        """Obtém analytics da frota do banco de dados"""
        try:
            motos_response = self.get_motos(page_size=1000)  # Buscar todas
            
            if not motos_response['success']:
                return motos_response
            
            motos = motos_response['motos']
            
            # Calcular métricas
            total_motos = len(motos)
            status_distribution = {}
            battery_levels = []
            locations = []
            
            for moto in motos:
                status = moto.get('status', 'unknown')
                status_distribution[status] = status_distribution.get(status, 0) + 1
                
                if 'batteryLevel' in moto:
                    battery_levels.append(moto['batteryLevel'])
                
                if 'location' in moto:
                    locations.append(moto['location'])
            
            avg_battery = sum(battery_levels) / len(battery_levels) if battery_levels else 0
            
            return {
                'success': True,
                'analytics': {
                    'total_motos': total_motos,
                    'status_distribution': status_distribution,
                    'average_battery': round(avg_battery, 2),
                    'active_locations': len(locations),
                    'last_updated': datetime.now().isoformat()
                }
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def health_check(self) -> Dict:
        """Verifica se a API .NET está funcionando"""
        try:
            response = self.session.get(f"{self.base_url}/health")
            response.raise_for_status()
            return {'success': True, 'api_status': response.json()}
        except Exception as e:
            return {'success': False, 'error': str(e)}

# ================================
# EXEMPLO DE USO
# ================================

if __name__ == "__main__":
    # Teste da integração
    client = DotNetApiClient()
    
    print("🚀 IDEATEC - Testando integração com API .NET...")
    
    # Health check
    health = client.health_check()
    print(f"✅ Health Check: {health}")
    
    # Buscar motos
    motos = client.get_motos()
    print(f"🏍️ Motos encontradas: {motos.get('total', 0)}")
    
    # Analytics da frota
    analytics = client.get_fleet_analytics()
    if analytics['success']:
        print(f"📊 Analytics: {analytics['analytics']}")