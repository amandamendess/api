
from fastapi import FastAPI, Security, status, Response
from fastapi.security.api_key import APIKeyHeader
from pydantic import BaseModel
from typing import Optional

class Clientes(BaseModel):
    id: Optional[int] = 0
    nome: str
    tipo_atendimento: str
    data : str
    atendido: bool
    posicao: Optional[int] = 0
    desc: Optional[str] = None

db_clientes = [
    Clientes(id=1, nome='João', tipo_atendimento = 'P', data = '2023-11-21 12:21:43', posicao= 1, atendido= False),
    Clientes(id=2, nome='Joana', tipo_atendimento = 'N', data = '2023-11-21 12:25:08', posicao= 4, atendido= False),
    Clientes(id=3, nome='Francisco', tipo_atendimento = 'N', data = '2023-11-21 12:33:05', posicao= 5, atendido= False),
    Clientes(id=4, nome='Rafaela', tipo_atendimento = 'P', data = '2023-11-21 12:55:50', posicao=6 , atendido= False),
]

app = FastAPI()

@app.get('/fila', status_code = status.HTTP_200_OK)
def buscarTodos():
    if len(db_clientes) > 0 :
        return {'cliente': db_clientes}
    else:       
        return{'mensagem': 'Nenhum cliente na fila' }

@app.get('/fila/{id}')
def buscarcliente(id: int, response: Response):
    cli =  [cliente for cliente in db_clientes if cliente.id==id]
    if len(cli) > 0:
        return {'cliente': cli}
    else:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {'mensagem': 'Nenhum cliente encontrado'}

@app.post('/fila')
def add_cliente(cliente: Clientes):
    cliente.id= db_clientes[-1].id + 1
    cliente.posicao= db_clientes[-1].posicao + 1
    cliente.atendido = False
    if len(cliente.nome) > 20 and len(cliente.tipo_atendimento) == 1: 
        db_clientes.append(cliente)
        return{'mensagem': 'Cliente adicionado na fila'}
    else :
        return {'mensagem': 'Nome deve conter no mínimo 20 caracteres e o tipo de atendimento N ou P'}
    
@app.put('/fila')
def atualiza_cliente(cliente: Clientes):
    index = db_clientes
    for cliente in index:
        if cliente.posicao == 1:
            cliente.posicao = 0
            cliente.atendido = True 
        else :
            cliente.posicao = cliente.posicao - 1  
           
        
    return {'retorno': cliente}

@app.delete('/fila/{id}')
def deletar_cliente(id:int, cliente: Clientes, response: Response):
    client = [cliente for cliente in db_clientes if cliente.id == id]

    if len(client) == 0:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {'mensagem': 'Nenhum cliente encontrado'}
    
    db_clientes.remove(client[0])
    fila = db_clientes  
    counter = 0   
    for cliente in fila:
        counter += 1
        cliente.posicao = counter 

  
