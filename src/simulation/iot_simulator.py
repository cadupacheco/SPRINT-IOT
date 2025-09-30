import random
import time
import json
import threading
from datetime import datetime, timedelta
from typing import Dict, List
import paho.mqtt.client as mqtt

class MottuIoTSimulator:
    def __init__(self):
        """Simulador de sensores IoT das motos Mottu"""
        self.motos_fleet = self._generate_fleet_data()
        self.simulation_active = False
        self.mqtt_client = None
        self.simulation_data = []
        
    def _generate_fleet_data(self) -> List[Dict]:
        """Gera dados simulados da frota de motos"""
        fleet = []
        statuses = ['disponivel', 'em_uso', 'manutencao', 'carregando']
        models = ['Mottu Sport 110i', 'Mottu Urban', 'Mottu Delivery']
        
        for i in range(1, 16):  # 15 motos simuladas
            moto = {
                'id': f'MOTTU_{i:03d}',
                'model': random.choice(models),
                'status': random.choice(statuses),
                'battery_level': random.randint(20, 100),
                'position': {
                    'x': random.randint(50, 750),  # Coordenadas do pátio
                    'y': random.randint(100, 500),
                    'zone': f'ZONA_{random.choice(["A", "B", "C"])}'
                },
                'last_maintenance': (datetime.now() - timedelta(days=random.randint(1, 30))).isoformat(),
                'odometer': random.randint(1000, 15000),
                'fuel_level': random.randint(30, 100)
            }
            fleet.append(moto)
        
        return fleet
    
    def simulate_real_time_data(self, duration_seconds: int = 300):
        """Simula dados IoT em tempo real"""
        self.simulation_active = True
        start_time = time.time()
        
        print(f"🚀 Iniciando simulação IoT por {duration_seconds} segundos...")
        
        while self.simulation_active and (time.time() - start_time) < duration_seconds:
            for moto in self.motos_fleet:
                # Simular mudanças nos dados
                self._update_moto_data(moto)
                
                # Criar mensagem IoT
                iot_message = {
                    'moto_id': moto['id'],
                    'timestamp': datetime.now().isoformat(),
                    'sensor_data': {
                        'gps': moto['position'],
                        'battery': moto['battery_level'],
                        'status': moto['status'],
                        'fuel': moto['fuel_level'],
                        'engine_temp': random.randint(80, 120),
                        'speed': random.randint(0, 60) if moto['status'] == 'em_uso' else 0
                    }
                }
                
                self.simulation_data.append(iot_message)
                
                # Simular envio MQTT (local)
                self._publish_mqtt_message(iot_message)
            
            time.sleep(2)  # Atualizar a cada 2 segundos
        
        print("✅ Simulação IoT finalizada")
    
    def _update_moto_data(self, moto: Dict):
        """Atualiza dados simulados da moto"""
        # Pequenas variações realistas
        if moto['status'] == 'em_uso':
            moto['battery_level'] = max(10, moto['battery_level'] - random.randint(0, 2))
            moto['fuel_level'] = max(5, moto['fuel_level'] - random.randint(0, 1))
            # Simular movimento
            moto['position']['x'] += random.randint(-10, 10)
            moto['position']['y'] += random.randint(-10, 10)
        elif moto['status'] == 'carregando':
            moto['battery_level'] = min(100, moto['battery_level'] + random.randint(1, 3))
        
        # Mudança aleatória de status (5% chance)
        if random.random() < 0.05:
            statuses = ['disponivel', 'em_uso', 'manutencao', 'carregando']
            moto['status'] = random.choice(statuses)
    
    def _publish_mqtt_message(self, message: Dict):
        """Simula publicação MQTT (apenas local para demonstração)"""
        # Para demonstração, apenas armazena localmente
        # Em produção, publicaria via MQTT real
        pass
    
    def get_current_fleet_status(self) -> Dict:
        """Retorna status atual da frota"""
        status_summary = {}
        for moto in self.motos_fleet:
            status = moto['status']
            status_summary[status] = status_summary.get(status, 0) + 1
        
        return {
            'fleet_summary': status_summary,
            'total_motos': len(self.motos_fleet),
            'motos_data': self.motos_fleet,
            'last_update': datetime.now().isoformat()
        }
    
    def stop_simulation(self):
        """Para a simulação"""
        self.simulation_active = False
