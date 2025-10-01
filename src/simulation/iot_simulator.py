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
    
    def start_simulation(self):
        """Inicia a simulação IoT"""
        if not self.simulation_active:
            self.simulation_active = True
            # Iniciar em thread separada para não bloquear
            threading.Thread(target=self.simulate_real_time_data, daemon=True).start()
    
    def is_running(self) -> bool:
        """Verifica se a simulação está ativa"""
        return self.simulation_active
    
    def reset_simulation(self):
        """Reseta a simulação"""
        self.simulation_active = False
        self.motos_fleet = self._generate_fleet_data()
        self.simulation_data = []
    
    def get_simulation_status(self) -> Dict:
        """Retorna status detalhado da simulação"""
        if not hasattr(self, '_start_time'):
            self._start_time = time.time()
        
        active_motos = len([m for m in self.motos_fleet if m['status'] != 'manutencao'])
        avg_battery = sum(m['battery_level'] for m in self.motos_fleet) / len(self.motos_fleet)
        
        return {
            'running': self.simulation_active,
            'active_motorcycles': active_motos,
            'total_messages': len(self.simulation_data),
            'avg_battery': avg_battery,
            'uptime_seconds': int(time.time() - self._start_time) if self.simulation_active else 0,
            'delta_motorcycles': 0,  # Para compatibilidade com métricas
            'delta_messages': 0,
            'delta_battery': 0
        }
    
    def get_motorcycles_data(self) -> List[Dict]:
        """Retorna dados atuais das motos"""
        formatted_data = []
        for moto in self.motos_fleet:
            formatted_data.append({
                'moto_id': moto['id'],
                'model': moto['model'],
                'battery_level': moto['battery_level'],
                'fuel_level': moto['fuel_level'],
                'status': moto['status'],
                'zone': moto['position']['zone'],
                'x': moto['position']['x'],
                'y': moto['position']['y']
            })
        return formatted_data
    
    def configure_mqtt(self, broker: str, port: int, topic: str):
        """Configura parâmetros MQTT"""
        self.mqtt_broker = broker
        self.mqtt_port = port
        self.mqtt_topic = topic
    
    def set_fleet_size(self, size: int):
        """Define tamanho da frota"""
        if size != len(self.motos_fleet):
            self.motos_fleet = self._generate_fleet_data()[:size]
    
    def set_update_interval(self, interval: int):
        """Define intervalo de atualização"""
        self.update_interval = interval
    
    def get_recent_logs(self, limit: int = 10) -> List[Dict]:
        """Retorna logs recentes da simulação"""
        if not hasattr(self, '_logs'):
            self._logs = []
        
        # Gerar alguns logs exemplo se não tiver
        if not self._logs:
            for i in range(5):
                self._logs.append({
                    'timestamp': datetime.now().strftime('%H:%M:%S'),
                    'message': f'Moto MOTTU_{i+1:03d} atualizou status'
                })
        
        return self._logs[-limit:]
    
    def clear_logs(self):
        """Limpa logs da simulação"""
        self._logs = []
