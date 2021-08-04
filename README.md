# Pedidos_em_kafka
Este repositório tem por objetivo apresentar um estudo de caso com kafka na Confluent Cloud, aplicado a uma simulação de processamento de pedidos.

Requisitos:
- Python 3
- Conta na Confluent

Kafka na confluent cloud:
- Acesse https://www.confluent.io/confluent-cloud/  e siga as orientações de cadastro, a confluente cloud tem uma versão free que te da $200 para teste.
- Apos concluir a etapa de cadastro precisamos criar os tópicos:
   - Acesse o "cluster" que você criou no processo da cadastro, vá em "Topics",  depois em " + Add topic".
   - Para este trabalho precisamos criar os tópicos: "Pedidos_recusados", "Notificacoes", "Pedidos" e "Pedidos_validos" (Todos os tópicos precisam de no máximo 3 partições).
- Após criar os tópicos precisamos criar uma API key para dar acesso aos nossos recursos no cluster.
   - Acesse o menu "CLI and tools" e vá na aba "CLI Tools".
   - Aperte o botão "Create Kafka cluster API key & secret", logo abaixo  na parte "Create a configuration file" copie os dados da caixa dessa etapa.
- Em posse dos dados da API e do cluster obtidos na etapa 3, vamos criar nosso arquivo de configuração.
   - Entre na pasta do projeto "Pedidos_em_kafka" e crie o arquivo conf.py
   - Preencha o arquivo com os dados coletados na etapa 3 da seguinte forma:
   ```
       bootstrap_servers = 'XXX' <- Troque os X pelo bootstrap_servers da etapa 3.
       security_protocol ='XXX'  <- Troque os X pelo security_protocol da etapa 3.
       sasl_mechanisms = 'XXXX'  <- Troque os X pelo sasl_mechanisms da etapa 3.
       sasl_username ='XXXXX'    <- Troque os X pelo username da etapa 3.
       sasl_password = 'XXXXXXXXXXXXXXXXX'  <- Troque os X pelo password da etapa 3.

Entendendo os recursos:
- api.py -> Uma api bem simples para receber as requisições de pedidos, com o endpoint /Pedidos e com acesso a documentação em /docs
- monitoramento_consumer_py -> Um serviço que basicamente centraliza os logs dos dados de comunição de todos os outros recursos.
- notificacao_consumer.py -> Um recurso que fica simulando um notificação de estatos de pedido ao cliente.
- fraudes_consumer_producer.py -> Um recurso responsável por processar todos os pedidos e "simular" uma deteccção de fraude no pedido.
 


Iniciando a aplicação:
Levantando API de pedidos:
- Dentro do projeto execute o comando pip install requirements para instalar todas as dependências do projeto.
- Execute o comando uvicorn api:app, para subir a api de pedidos (por default deve subir na porta 8000).
- Acessando a API, abra o navegador e acesse localhost:8000/docs (endpoint da documentação da API).
- Ao final você já tera sua api funcionando.
- Sendo possivel criar pedidos pela própria interface da documentação.


Iniciando outros recursos:
- Iniciando o serviço de fraudes
  - Abra um terminal e digite python fraudes_consumer_producer.py
- Iniciando o serviço de monitoramento
  - Abra um terminal e digite python monitoramento_consumer.py
- Iniciando o serviço de notificacao
  - Abra um terminal e digite python notificacao_consumer.py


Entendo o fluxo da aplicação:

- A API recebe um pedido
  - API posta pedido no tópico /Pedidos e posta no tópico /Notificacoes a atualização de status do pedido
- Recurso fraudes escuta o tópico /Pedidos
  - Recurso Fraudes processa o pedido 
    - Se for fraude, posta no topico /Fraudes e posta no tópico /Notificaoes a atualização de status do pedido
    - Se não for fraude, posta na tópico /Pedidos_validos e posta no tópico /Notificaoes a atualização de status do pedido
- Recurso Notificacao escuta o tópico /Notificacoes
  - Simula o envio de notificação de status do pedido ao cliente.
- Recurso Monitoramento escuta os tópicos /Pedidos, /Fraudes, /Notificacoes, /Pedidos_validos
  - Seu papel e gravar todo log de comunicação entre os recursos que compõe a aplicação.



Para exemplo deste trabalho foi utilizado a solução do Kafka na concluent, entretanto deixo nas referencias um video explicando como instalar e configurar o kafka localmente.


Referências: 
- https://www.confluent.io/
- https://www.youtube.com/watch?v=BgbKAaWKMn8&t=1368s
- https://www.youtube.com/watch?v=LX19wk2B5Ak&t=1108s
