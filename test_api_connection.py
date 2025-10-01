"""
🔧 TESTE DE CONEXÃO API .NET
Verifica se sua API está rodando e em que porta
"""

import requests
import json

def test_api_connection():
    """Testa diferentes portas comuns da API .NET"""
    
    common_urls = [
        "http://localhost:5000",
        "http://localhost:5001", 
        "http://localhost:7000",
        "http://localhost:7001",
        "http://localhost:8080",
        "https://localhost:5001",
        "https://localhost:7001"
    ]
    
    print("🔍 Testando conexões com API .NET...")
    print("=" * 50)
    
    for url in common_urls:
        try:
            # Testar endpoint básico
            response = requests.get(f"{url}/api/health", timeout=3)
            if response.status_code == 200:
                print(f"✅ API encontrada em: {url}")
                return url
        except:
            pass
        
        try:
            # Testar endpoint alternativo
            response = requests.get(f"{url}/api/moto", timeout=3)
            if response.status_code in [200, 401, 403]:  # API rodando, mesmo que protegida
                print(f"✅ API encontrada em: {url}")
                return url
        except:
            pass
            
        print(f"❌ Não conectou: {url}")
    
    print("\n🚨 API .NET não encontrada!")
    print("💡 Certifique-se que sua API está rodando")
    return None

def get_api_info(base_url):
    """Obtém informações da API"""
    try:
        endpoints_to_test = [
            "/api/moto",
            "/api/patio", 
            "/api/modelo",
            "/swagger"
        ]
        
        print(f"\n📋 Testando endpoints em: {base_url}")
        for endpoint in endpoints_to_test:
            try:
                response = requests.get(f"{base_url}{endpoint}", timeout=3)
                print(f"  {endpoint}: {response.status_code}")
            except Exception as e:
                print(f"  {endpoint}: Erro - {str(e)[:50]}")
                
    except Exception as e:
        print(f"❌ Erro ao testar endpoints: {e}")

if __name__ == "__main__":
    print("🏍️ IDEATEC - TESTE CONEXÃO API .NET")
    print("=" * 50)
    
    api_url = test_api_connection()
    
    if api_url:
        get_api_info(api_url)
        print(f"\n✅ Configure o sistema para usar: {api_url}")
        print(f"💻 Comando: export API_URL={api_url}")
    else:
        print("\n📋 PASSOS PARA CONECTAR:")
        print("1. Vá para o diretório da sua API .NET")
        print("2. Execute: dotnet run")
        print("3. Anote a URL que aparecer (ex: http://localhost:5000)")
        print("4. Execute este script novamente")
        
    print("\n" + "=" * 50)