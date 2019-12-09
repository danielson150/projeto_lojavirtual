# Dupla: 
- Guilherme Sousa da Silva 
- Danielson da Silva Alencar
## Atividade Programação para Internet II - PROJETO WEB API

### Sobre a Atividade
A atividade se refere a implementação da Atividade nomeada de projeto_web_apis_01.pdf localizado neste [link](https://drive.google.com/drive/u/1/folders/1GCKSVXMMiTQO2pVaTWF3WNi4P99p8iIK) juntamente com um documento detalhado explicando a API e um video explicativo.

#### Atividade / Questão Nº1
A API possui no total de 6 entidade mais a utilização do User do próprio Django, sendo elas **Categoria, Item, ItemPurchase, Purchase, InformacoesUsuario e Carteira Digital.**
Categoria é uma entidade mais relacionada a buscas possuindo somente dois campos(name,description) já Item é uma entidade mais forte pois possui maiores interações com outras entidades e outras também dependem dela ja que muitas ações podem ser negadas de acordo com a quantidade do item no estoque.
ItemPurchase se da melhor explicada como um carrinho onde tempos a quantidade dos itens comprado relacionanado ele a uma compra em aberto.
Purchase tem se valor total calculado de acordo com os preços no carrinho a criação de suas instâncias se da automaticamente não sendo permitido a criação de novas por vontade própria ou deleta-las.
InformacoesUsuario assim como Categoria não possui uma ligação tão forte ela seria utilizado em conjunto a alguma outra API que calculasse fretes pegando informações extras dos usuarios que não podem armazenadas em User e por fim a Carteira uma entidade que guardaria créditos virtuais que seriam utilizados nas compras e depedendo dos créditos as compras são restritas.

#### Atividade / Questão Nº2
Temos 3 tipos de usuarios: Usuario Anônimo, Autenticado Não SuperUser e Super User, sobre o tratamento de acessibilades não há uma padronização do acesso as views, depedendo da view os usuarios possuem permissoes e dados diferentes. Um exemplo é a view sobre o detalhe de Usuários, onde o anônimo não possui acesso já que não possui dados sobre ele, o autenticado pode somente acessar a seus proprios dados e alterar atributos como nome, email e senha e o super que pode acessar a todos os usuários mas podendo somente modificar atributos como is_super, is_staff e is_active de outros usuários.

#### Atividade / Questão Nº3, Nº4, Nº5
Como essas questões são mais configurações no arquivo de sao bem simples de ser implementadas, sobre autenticação foi utilizado o JWT pois se tornou mais viável, sobre Throttling a quantidade de requisições se manteve alta ja que em um site de compras geralmente se tem muitas pesquisas sobre itens diferentes e até mesmos preços diferentes e sobre filtros, pesquisas e ordenação é demonstrado no video.

#### Atividade / Questão Nº6
Não foi completada devido a erros desconhecidos que não contecem em tempo de teste no PostMan, tornando inviavel a correção para poder torna possível a entrega a tempo da data especificada.

#### Em Geral sobre a API
A API foi construida sobre regras de negocios especificas para poder simular o mais proximo possivel de uma loja virtual real, tendo muitas verificações e permissões diferentes para as mais diferentes views, sem contar que a alterações de dados geravam alterações em outras entidades que também fazem partye da API como por exemplo ao adicionar um item ao carrinho será aumentado o preço da compra.


### Vídeo

https://youtu.be/DdJffYmrwM8

