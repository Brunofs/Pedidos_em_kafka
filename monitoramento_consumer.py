from confluent_kafka import Consumer
import producer
import json
import conf

if __name__ == '__main__':
    key = 'Fraudes'
    topic_fraudes= 'Fraudes'
    topic_pedidos_valido= 'Pedidos_validos'
    topic = 'Pedidos'
    consumer = Consumer({
        'bootstrap.servers' : conf.bootstrap_servers
        ,'security.protocol' : conf.security_protocol
        ,'sasl.mechanisms'   : conf.sasl_mechanisms
        ,'sasl.username'     : conf.sasl_username
        ,'sasl.password'     : conf.sasl_password
    ,'group.id':'MONITORAMENTO_LOG'
    ,'auto.offset.reset':'earliest'})

    consumer.subscribe([topic,topic_fraudes,topic_pedidos_valido])
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
                print(json.loads(record_value)["mensagem"])             
    except KeyboardInterrupt:
        pass
    finally:
        # Leave group and commit final offsets
        consumer.close()
