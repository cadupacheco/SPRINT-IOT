"""
🔧 CONFIGURADOR DE API - IDEATEC MOTTU SYSTEM
Permite configurar a URL da sua API .NET
"""

import os
import json

def configure_api_url():
    """Configura URL da API .NET"""
    print("🔧 CONFIGURAÇÃO DA API .NET")
    print("=" * 40)
    
    print("💡 Sua API .NET deve estar rodando primeiro!")
    print("📋 Exemplos de URLs comuns:")
    print("   http://localhost:5000")
    print("   http://localhost:5001") 
    print("   https://localhost:7001")
    print("   http://localhost:8080")
    
    api_url = input("\n🌐 Digite a URL da sua API .NET: ").strip()
    
    if not api_url:
        print("❌ URL não pode estar vazia")
        return
    
    # Salvar configuração
    config = {
        "api_url": api_url,
        "configured_at": "2025-10-01",
        "mode": "production"
    }
    
    with open("api_config.json", "w") as f:
        json.dump(config, f, indent=2)
    
    print(f"\n✅ Configuração salva!")
    print(f"🌐 API URL: {api_url}")
    print(f"💾 Salvo em: api_config.json")
    
    # Testar conexão
    print(f"\n🔍 Testando conexão...")
    import requests
    try:
        response = requests.get(f"{api_url}/api/health", timeout=5)
        if response.status_code == 200:
            print("✅ Conexão bem-sucedida!")
        else:
            print(f"⚠️ API respondeu com status: {response.status_code}")
    except Exception as e:
        print(f"❌ Erro na conexão: {e}")
        print("💡 Verifique se a API está rodando")

if __name__ == "__main__":
    configure_api_url()