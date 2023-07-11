# 1- Problema de negócio
A empresa Fome Zero é uma marketplace de restaurantes. Ou seja, seu core business é facilitar o encontro e negociações de clientes e restaurantes. Os restaurantes fazem o cadastro dentro da plataforma da Fome Zero, que disponibiliza informações como endereço, tipo de culinária servida, se possui reservas, se faz entregas e também uma nota de avaliação dos serviços e produtos do restaurante, dentre outras informações.

O Desafio é ajudar o novo CEO a entender melhor o negócio para conseguir tomar as melhores decisões estratégicas e alavancar ainda mais a Fome Zero. Para isto foi feita uma análise nos dados da empresa e gerados dashboards, a partir dessas análises.

# 2- Premissas do negócio
1. O dataset possui 6929 registros validos para análise;
2. Marketplace foi o modelo de negócio assumido;
3. As 4 principais visões de negócio foram: Visão geral, visão países, visão cidades e visão tipos culinários e restaurantes.

# 3- Estratégia da solução
O painel estratégico foi desenvolvido utilizando as métricas que refletem as 4 principais visões do modelo de negócio da empresa:
1. Visão geral
2. Visão países
3. Visão cidades
4. Visão tipos culinários e restaurantes
   
Cada visão é representada pelo seguinte conjunto de métricas:
1. Visão geral
	1. Quantos restaurantes únicos estão registrados?
	2. Quantos países únicos estão registrados?
	3. Quantas cidades únicas estão registradas?
	4. Qual o total de avaliações feitas?
	5. Qual o total de tipos de culinária registrados?
2. Visão países
	1. Qual o nome do país que possui mais cidades registradas?
	2. Qual o nome do país que possui mais restaurantes registrados?
	3. Qual o nome do país que possui, na média, a maior quantidade de avaliações registrada?
	4. Qual a média de preço de um prato para dois por país?
3. Visão cidades
	1. Qual o nome da cidade que possui mais restaurantes registrados?
	2. Qual o nome da cidade que possui mais restaurantes com nota média acima de 4?
	3. Qual o nome da cidade que possui mais restaurantes com nota média abaixo de 2.5?
	4. Qual o nome da cidade que possui a maior quantidade de tipos de culinária distintas?
4. Visão tipos culinários e restaurantes
	1. O melhor e pior restaurante de para cada tipo de culinária
	2. Qual o nome do restaurante com a maior nota média?
	3. Qual o tipo de culinária que possui a maior nota média?
	4. Qual o tipo de culinária que possui a menor nota média?
# 4- Top 3 insights de dados
1. Índia é o país com a maior quantidade de restaurantes, por consequência, quando realizamos outras contagens na análise frequentemente o país aparece em primeira posição;
2. Os restaurantes que realizam Delivery online possuem uma maior quantidade de avaliações registradas;
3. A plataforma possui apenas 15 países diferentes cadastrados, o que demonstra que existe grande oportunidade de crescimento visto todo o mercado mundial que ainda pode ser explorado.

# 5- O produto final do Projeto
Painel online, hospedado em uma Cloud e disponível para acesso em qualquer dispositivo conectado à internet.

O painel pode ser acessado através desse link: https://projetofomezero-michele.streamlit.app/Cuisines
# 6- Conclusão
O objetivo foi criar um conjunto de gráficos e tabelas que exibam essas métricas da melhor forma possível para o CEO.

# 7- Próximos passos
1. Desenvolver novos Dashboards e responder outras perguntas de negócio;
2. Realizar análises específicas para a Índia, como é o país com mais representativadade no Dashboard;
3. Criar novos filtros para uma visão mais interativa no Dashboard.
