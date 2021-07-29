from confluent_kafka import Consumer
import producer
import json
import time
import conf

mensagem = {"mensagem":"",
              "payload": [],
              "id":0}


def processaFraude(pedido):
    print('Avaliando pedido')
    id = pedido['id']
    time.sleep(0.2)
    if id%3==0:
       return True
    return False

if __name__ == '__main__':

    key = 'Fraudes'
    topic_fraudes= 'Fraudes'
    topic_pedidos_valido= 'Pedidos_validos'
    topic = 'Pedidos'
    topic_notificacoes = 'Notificacoes'
    
    #e “earliest” offset or the “latest” offset (the default). You can also select “none” i
    consumer = Consumer({
        'bootstrap.servers' : conf.bootstrap_servers
        ,'security.protocol' : conf.security_protocol
        ,'sasl.mechanisms'   : conf.sasl_mechanisms
        ,'sasl.username'     : conf.sasl_username
        ,'sasl.password'     : conf.sasl_password
        ,'group.id':'ML_FRAUDES_DETECT'
        ,'auto.offset.reset':'earliest'})
    
    consumer.subscribe([topic])
    total_count = 0
    try:
        while True:
            msg = consumer.poll(1.0)
            if msg is None:
                #print("Waiting for message or event/error in poll()")
                continue
            elif msg.error():
                print('error: {}'.format(msg.error()))
            else:
                record_key = msg.key()
                record_value = msg.value()
                
                print("processando um pedido")
                data = json.loads(record_value)

                payload = json.loads(data['dados'])
                usuario =  payload['usuario']
                if processaFraude(payload):
                    mensagem['dados'] = json.dumps(payload)
                    mensagem['status'] = 'Recusado'
                    mensagem['mensagem'] = "Pedido {} {} {} é fraude".format(payload['id'],payload['usuario'],payload['produto'])
                    mensagem['id']= payload['id']
                    print(usuario)
                    producer.produceKafka(topic_notificacoes,json.dumps(mensagem),usuario)
                    producer.produceKafka(topic_fraudes,json.dumps(mensagem),None)
                else:
                    print("Enviando pedido {} para processar".format(payload['id']))
                    mensagem['dados'] = json.dumps(payload)
                    mensagem['mensagem'] = "Pedido {} {} {} aprovado".format(payload['id'],payload['usuario'],payload['produto'])
                    mensagem['status'] = 'Aprovado'
                    mensagem['id']= payload['id']
                    producer.produceKafka(topic_notificacoes,json.dumps(mensagem),usuario)  
                    producer.produceKafka(topic_pedidos_valido,json.dumps(mensagem),None)                    
                    total_count = total_count +1                
    except KeyboardInterrupt:
        pass
    finally:
        # Leave group and commit final offsets
        consumer.close()
