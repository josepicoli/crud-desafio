#!/usr/bin/env python3
"""
Script de teste para a API de Agenda Médica
Execute: python test_api.py
"""

import requests
import json

BASE_URL = "http://localhost:8000"

def test_api():
    print("=== Teste da API de Agenda Médica ===\n")
    
    # 1. Criar médicos
    print("1. Criando médicos...")
    medicos_data = [
        {"nome": "Dr. João Silva", "especialidade": "Cardiologia"},
        {"nome": "Dra. Maria Santos", "especialidade": "Pediatria"},
        {"nome": "Dr. Carlos Oliveira", "especialidade": "Ortopedia"},
        {"nome": "Dra. Ana Costa", "especialidade": "Dermatologia"}
    ]
    
    medicos_criados = []
    for medico in medicos_data:
        response = requests.post(f"{BASE_URL}/medicos/", json=medico)
        if response.status_code == 201:
            medico_criado = response.json()
            medicos_criados.append(medico_criado)
            print(f"   ✓ Criado: {medico_criado['nome']} - {medico_criado['especialidade']}")
        else:
            print(f"   ✗ Erro ao criar médico: {response.text}")
    
    print()
    
    # 2. Listar todos os médicos
    print("2. Listando todos os médicos...")
    response = requests.get(f"{BASE_URL}/medicos/")
    if response.status_code == 200:
        medicos = response.json()
        for medico in medicos:
            print(f"   - {medico['nome']} ({medico['especialidade']})")
    else:
        print(f"   ✗ Erro ao listar médicos: {response.text}")
    
    print()
    
    # 3. Buscar médicos por nome
    print("3. Buscando médicos por nome...")
    search_terms = ["João", "Maria", "Carlos", "Ana"]
    
    for term in search_terms:
        response = requests.get(f"{BASE_URL}/medicos/?nome={term}")
        if response.status_code == 200:
            medicos = response.json()
            print(f"   Busca por '{term}': {len(medicos)} resultado(s)")
            for medico in medicos:
                print(f"     - {medico['nome']}")
        else:
            print(f"   ✗ Erro na busca por '{term}': {response.text}")
    
    print()
    
    # 4. Buscar médico por ID
    if medicos_criados:
        medico_id = medicos_criados[0]['id']
        print(f"4. Buscando médico por ID ({medico_id})...")
        response = requests.get(f"{BASE_URL}/medicos/{medico_id}")
        if response.status_code == 200:
            medico = response.json()
            print(f"   ✓ Encontrado: {medico['nome']} - {medico['especialidade']}")
        else:
            print(f"   ✗ Erro ao buscar médico: {response.text}")
    
    print()
    
    # 5. Atualizar médico
    if medicos_criados:
        medico_id = medicos_criados[0]['id']
        print(f"5. Atualizando médico (ID: {medico_id})...")
        update_data = {"especialidade": "Cardiologia Intervencionista"}
        response = requests.put(f"{BASE_URL}/medicos/{medico_id}", json=update_data)
        if response.status_code == 200:
            medico_atualizado = response.json()
            print(f"   ✓ Atualizado: {medico_atualizado['nome']} - {medico_atualizado['especialidade']}")
        else:
            print(f"   ✗ Erro ao atualizar médico: {response.text}")
    
    print()
    
    # 6. Deletar médico
    if medicos_criados:
        medico_id = medicos_criados[-1]['id']  # Deletar o último médico criado
        print(f"6. Deletando médico (ID: {medico_id})...")
        response = requests.delete(f"{BASE_URL}/medicos/{medico_id}")
        if response.status_code == 200:
            print(f"   ✓ Médico deletado com sucesso")
        else:
            print(f"   ✗ Erro ao deletar médico: {response.text}")
    
    print("\n=== Teste concluído ===")

if __name__ == "__main__":
    try:
        test_api()
    except requests.exceptions.ConnectionError:
        print("❌ Erro: Não foi possível conectar à API.")
        print("Certifique-se de que a aplicação está rodando em http://localhost:8000")
        print("Execute: uvicorn main:app --reload")
    except Exception as e:
        print(f"❌ Erro inesperado: {e}") 