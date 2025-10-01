"""
🔧 TESTE DETALHADO DA API .NET
Verifica endpoints e estrutura da sua API
"""

import requests
import json

def test_api_endpoints():
    """Testa diferentes endpoints da API"""
    base_url = "http://localhost:5221"
    
    endpoints_to_test = [
        "/",
        "/api",
        "/api/moto", 
        "/api/Moto",
        "/api/motos",
        "/api/Motos",
        "/api/patio",
        "/api/Patio", 
        "/api/patios",
        "/api/Patios",
        "/api/modelo",
        "/api/Modelo",
        "/swagger"
    ]
    
    print("🔍 TESTANDO ENDPOINTS DA API .NET")
    print("=" * 50)
    
    working_endpoints = []
    
    for endpoint in endpoints_to_test:
        try:
            response = requests.get(f"{base_url}{endpoint}", timeout=5)
            status = response.status_code
            
            if status == 200:
                print(f"✅ {endpoint}: {status} - FUNCIONANDO")
                working_endpoints.append(endpoint)
            elif status == 500:
                print(f"⚠️ {endpoint}: {status} - API OK, erro de banco")
                working_endpoints.append(endpoint)
            elif status == 404:
                print(f"❌ {endpoint}: {status} - Não encontrado")
            else:
                print(f"🔶 {endpoint}: {status} - Status: {status}")
                
        except Exception as e:
            print(f"💥 {endpoint}: Erro - {str(e)[:50]}")
    
    print("\n📋 ENDPOINTS QUE FUNCIONAM:")
    for endpoint in working_endpoints:
        print(f"   {endpoint}")
    
    return working_endpoints

def get_swagger_info():
    """Busca informações do Swagger"""
    try:
        response = requests.get("http://localhost:5221/swagger/v1/swagger.json", timeout=5)
        if response.status_code == 200:
            swagger_data = response.json()
            print("\n📚 INFORMAÇÕES DO SWAGGER:")
            print("=" * 30)
            
            if 'paths' in swagger_data:
                print("🔗 Endpoints disponíveis:")
                for path in swagger_data['paths'].keys():
                    methods = list(swagger_data['paths'][path].keys())
                    print(f"   {path} [{', '.join(methods).upper()}]")
            
            return swagger_data
        else:
            print(f"❌ Swagger não disponível: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"❌ Erro ao acessar Swagger: {e}")
        return None

if __name__ == "__main__":
    print("🏍️ IDEATEC - TESTE DETALHADO API .NET")
    print("🌐 URL: http://localhost:5221")
    print("=" * 50)
    
    # Testar endpoints
    working_endpoints = test_api_endpoints()
    
    # Buscar informações do Swagger
    swagger_info = get_swagger_info()
    
    print("\n" + "=" * 50)
    print("💡 ACESSE SWAGGER EM: http://localhost:5221/swagger")
    print("📋 Lá você verá todos os endpoints corretos da sua API")
    print("=" * 50)