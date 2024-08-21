# Discord Quiz Bot Gamer

Este projeto é um bot de jogo de perguntas e respostas para Discord, desenvolvido em Python usando a biblioteca `discord.py`. O bot permite que dois jogadores participem de um jogo de perguntas e respostas com um limite de tempo para cada pergunta.

## Funcionalidades

- Iniciar um jogo de perguntas e respostas com o comando `!illumi start`.
- Jogar com até 2 jogadores simultaneamente.
- Adicionar jogadores ao jogo com o comando `!join`.
- Enviar perguntas e opções para os jogadores via mensagem direta.
- Finalizar o jogo e mostrar as pontuações com o comando `!illumi score`.

## Pré-requisitos

- Python 3.8 ou superior
- Biblioteca `discord.py`

## Instalação

1. Clone este repositório:

    ```bash
    git clone https://github.com/seu-usuario/seu-repositorio.git
    cd seu-repositorio
    ```

2. Instale as dependências:

    ```bash
    pip install discord.py
    ```

3. Crie um arquivo chamado `Token.py` no mesmo diretório do seu script e adicione o seguinte código, substituindo `YOUR_BOT_TOKEN` pelo token do seu bot:

    ```python
    token = 'YOUR_BOT_TOKEN'
    ```

## Uso

1. Inicie o bot:

    ```bash
    python seu_script.py
    ```

2. Use os seguintes comandos no Discord:

    - `!illumi start` - Inicia um novo jogo de jogo de perguntas e respostas.
    - `!illumi score` - Mostra a pontuação atual do jogo.
    - `!join` - Adiciona o jogador atual ao jogo.

## Estrutura do Código

- **Configuração do Bot**: Define os intents e cria a instância do bot.
- **Comandos**:
  - `!illumi start`: Inicia o jogo e seleciona duas perguntas aleatórias.
  - `!illumi score`: Mostra as pontuações dos jogadores.
  - `!join`: Adiciona o jogador ao jogo, se o jogo estiver ativo e se houver espaço.
- **Eventos**:
  - `on_ready()`: Notifica quando o bot está pronto para uso.
  - `on_message(message)`: Processa as respostas dos jogadores e atualiza a pontuação.
- **Funções Auxiliares**:
  - `start_game()`: Envia as perguntas para os jogadores.
  - `end_game()`: Finaliza o jogo e anuncia o vencedor.
  - `show_score(ctx)`: Mostra as pontuações dos jogadores.

## Contribuição

Contribuições são bem-vindas! Se você encontrar algum problema ou tiver sugestões de melhorias, sinta-se à vontade para abrir uma issue ou enviar um pull request.

## Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para mais detalhes.
