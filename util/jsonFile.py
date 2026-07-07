from datetime import datetime
from fastapi import HTTPException
import json
import os

diretorio = "pathJson"
file = "pathJson/task.json"

def readJson():
    if not os.path.exists(file): # Cria o arquivo caso não exista
        os.mkdir(diretorio)
        with open(file, "w") as wArquivo:
            json.dump([], wArquivo)

    while True: # verifcar e retorna os dados corretos
        try:
            with open(file, "r", encoding="utf-8") as rArquivo:
                dados = json.load(rArquivo)
            
            return dados
        except json.decoder.JSONDecodeError as e:
            with open(file, "w") as wArquivo:
                json.dump([], wArquivo)

def createTarefa(nmTarefa):
    dados = readJson()

    for i in dados: # Verificar se tarefa já é existente
        if i["tarefa"] == nmTarefa:
            raise HTTPException(
                status_code=400,
                detail="Tarefa já está criada!!"
            )
        
    tarefa = { # adiciona dados na tarefa
        "id": len(dados)+1,
        "tarefa": nmTarefa,
        "feito": False,
        "data": datetime.now().strftime("%d/%m/%y"),
        "hora": datetime.now().strftime("%H:%M:%S")
    }
    dados.append(tarefa)

    with open (file, "w", encoding="utf-8") as arquivo: # Adiciona a tarefa no Json
        json.dump(dados, arquivo, indent=4)
        raise HTTPException(
            status_code=200,
            detail=f"Tarefa: '{nmTarefa}' foi criada com sucesso!!"
        )

def deleteTarefa(idTarefa):
    dados = readJson()
    nmTarefa = ""

    if dados ==[]: # verificar se a lista de tarefas está vazia
        raise HTTPException(
            status_code=404,
            detail="Lista de Tarefa está vazia"
        )
    
    if idTarefa > len(dados): # verificar se tarefa é existente
        raise HTTPException(
            status_code=404,
            detail="Tarefa Inválidia"
        )


    for i in dados: # deletar a tarefa desejada
        if i["id"] == idTarefa:
            nmTarefa = i["tarefa"]
            del dados[i["id"] -1]
    
    for n,i in enumerate(dados): # reorganizar os id das tarefas
        i["id"] = n+1
    
    with open(file, "w", encoding="utf-8") as arquivo:
        json.dump(dados, arquivo, indent=4)
        raise HTTPException(
            status_code=200,
            detail=f"A tarefa: '{nmTarefa}' foi deletada com sucesso!!"
        )

def update_feitoTarefa(idTarefa):
    dados = readJson()
    nmTarefa = ""

    if dados ==[]: # verificar se a lista de tarefas está vazia
        raise HTTPException(
            status_code=404,
            detail="Lista de Tarefa está vazia"
        )
    
    if idTarefa > len(dados): # verificar se tarefa é existente
        raise HTTPException(
            status_code=404,
            detail="Tarefa Inválidia"
        )

    status = ""
    for i in dados: # deletar a tarefa desejada
        if i["id"] == idTarefa:
            nmTarefa = i["tarefa"]
            if not i["feito"]:
                status = "Marcado"
                i["feito"] = True
            else:
                status = "Desmarcado"
                i["feito"] = False

    with open(file, "w", encoding="utf-8") as arquivo:
        json.dump(dados, arquivo, indent=4)
        raise HTTPException(
            status_code=200,
            detail=f"A tarefa: '{nmTarefa}' foi {status} com sucesso!!"
        )