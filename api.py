from time import sleep
from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime,date
from producer import produceKafka
import json


mensagem = {"mensagem":"",
              "payload": [],
              "id":0,
              "status":""}


app = FastAPI()


class Pedido(BaseModel):
    id: int
    usuario:str
    produto:str
    dataSolicitacao:str


pedidos = []

@app.get('/Pedidos')
def buscaPedidos():
    return pedidos

@app.get('/Pedidos/{id_usuario}')
def buscaPedido(id_usuario:int):
    for pe in pedidos:
        if pe.id == id_usuario:
            return pe
    return 'Pedido não encontrado'


idpedidos = 0
@app.post('/Pedidos')
def novoPedido(pedido:Pedido):
    global idpedidos
    pedido.dataSolicitacao = str(datetime.now())
    pedido.id = idpedidos
    idpedidos = idpedidos+1
    mensagem['dados']= json.dumps(pedido.__dict__)
    mensagem['mensagem']= 'Novo Pedido id {} {}'.format(pedido.id,pedido.usuario,pedido.produto)
    mensagem['status'] = 'Analise'
    produceKafka("Pedidos",json.dumps(mensagem),pedido.usuario)
    return "Seu pedido gerou o ticket {} e foi enviado com sucesso!".format(pedido.id)
