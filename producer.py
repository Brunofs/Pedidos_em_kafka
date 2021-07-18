from confluent_kafka import Producer
import json
import conf

p = Producer({
     'bootstrap.servers' : conf.bootstrap_servers
    ,'security.protocol' : conf.security_protocol
    ,'sasl.mechanisms'   : conf.sasl_mechanisms
    ,'sasl.username'     : conf.sasl_username
    ,'sasl.password'     : conf.sasl_password
})

def delivery_report(err, msg):

    if err is not None:
        print('Falha no envio de mensagem: {}'.format(err))
    else:
        print('Mensagem entregue para {} [{}]'.format(msg.topic(), msg.partition()))





def produceKafka(topico,mensagem,key):
 
    p.poll(0)
    if key is not None:
        p.produce(topico,key=key,value= mensagem, on_delivery=delivery_report)
    else:
        p.produce(topico,value= mensagem, on_delivery=delivery_report)
    p.flush()
    

# Wait for any outstanding messages to be delivered and delivery report
# callbacks to be triggered.
