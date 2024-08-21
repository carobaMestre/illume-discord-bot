import discord
from Token import token
from discord.ext import commands, tasks
import random
import asyncio

# Configuração dos intents para o bot
intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.message_content = True  # Habilita o acesso ao conteúdo das mensagens
intents.dm_messages = True  # Habilita o envio de mensagens privadas (DMs)

# Criação do bot com o prefixo de comando
bot = commands.Bot(command_prefix='!', intents=intents)

# Perguntas do quiz
questions = [
    {"question": "Qual é a capital da França?", "options": ["A. Paris", "B. Londres", "C. Berlim", "D. Madrid"], "answer": "A"},
    {"question": "Qual é o maior planeta do sistema solar?", "options": ["A. Terra", "B. Marte", "C. Júpiter", "D. Saturno"], "answer": "C"},
    #Escreva mais perguntas aqui!
]


# Armazenamento dos jogadores e suas pontuações
players = {}
current_game = None
question_timer = None
countdown_task = None  # Adicione uma variável para a tarefa da contagem regressiva

# Evento que é chamado quando o bot está pronto
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

# Comando para iniciar o jogo ou mostrar a pontuação
@bot.command()
async def illumi(ctx, action=None):
    global current_game
    if action == 'start':
        if current_game:
            await ctx.send("Um jogo já está em andamento.")
        else:
            # Inicia o jogo para 2 jogadores
            current_game = {"players": [], "questions": random.sample(questions, min(10, len(questions))), "scores": {}, "question_index": 0, "channel": ctx.channel}
            num_questions = len(current_game["questions"])
            if num_questions < 10:
                await ctx.send(f"O jogo será iniciado com {num_questions} perguntas. Para uma melhor experiência, recomenda-se contatar o administrador do bot para adicionar mais perguntas.")
            await ctx.send("Jogo de perguntas e respostas iniciado! Use !join para participar.")
    elif action == 'score':
        await show_score(ctx)
    else:
        await ctx.send("Uso: !illumi [start|score]")

# Comando para um jogador entrar no jogo
@bot.command()
async def join(ctx):
    global current_game, countdown_task
    if current_game:
        if ctx.author.id in current_game["players"]:
            await ctx.send("Você já está participando do jogo.")
        elif len(current_game["players"]) < 2:
            current_game["players"].append(ctx.author.id)
            current_game["scores"][ctx.author.id] = 0
            if len(current_game["players"]) == 2:
                await ctx.send(f"{ctx.author.mention} entrou no jogo. Aguardando o início do jogo...")
                if countdown_task:
                    countdown_task.cancel()  # Cancela qualquer contagem regressiva anterior
                countdown_task = asyncio.create_task(start_countdown())
            else:
                await ctx.send(f"{ctx.author.mention} entrou no jogo. Aguardando o segundo jogador...")
        else:
            await ctx.send("O jogo já está completo.")
    else:
        await ctx.send("Nenhum jogo está em andamento. Use !illumi start para iniciar um jogo.")

async def start_countdown():
    global current_game
    channel = current_game["channel"]

    # Envia uma mensagem de confirmação para cada jogador
    for player_id in current_game["players"]:
        user = await bot.fetch_user(player_id)
        await user.send("O jogo está prestes a começar! Prepare-se!")

    # Aguarda 10 segundos para que todos os jogadores possam se preparar
    await asyncio.sleep(10)

    # Inicia o jogo
    await start_game()

async def start_game():
    global current_game, question_timer
    players = current_game["players"]
    questions = current_game["questions"]
    channel = current_game["channel"]

    # Envia a primeira pergunta para os jogadores
    question = questions[current_game["question_index"]]
    options = "\n".join(question['options'])
    question_message = (f"{question['question']}\n{options}\n"
                        "Você tem 30 segundos para responder.")
    for player_id in players:
        user = await bot.fetch_user(player_id)
        await user.send(question_message)

    # Envia a pergunta no canal do servidor apenas uma vez
    await channel.send(f"Pergunta: {question['question']}\n{options}\n*Os jogadores têm 30 segundos para responder.*")

    # Define o temporizador para terminar o jogo após 30 segundos
    question_timer = asyncio.create_task(end_game_after_delay(30))

async def end_game_after_delay(seconds):
    await asyncio.sleep(seconds)
    await end_game()

async def end_game():
    global current_game, question_timer
    if current_game:
        channel = current_game["channel"]
        for player_id in current_game["players"]:
            user = await bot.fetch_user(player_id)
            await user.send("O tempo acabou! O jogo terminou. Use !illumi score para ver as pontuações.")

        winner = max(current_game["scores"], key=current_game["scores"].get, default=None)
        if winner:
            winner_user = await bot.fetch_user(winner)
            await winner_user.send(f"Parabéns, {winner_user.mention}! Você venceu com {current_game['scores'][winner]} pontos.")
            await channel.send(f"O jogo terminou! O vencedor é {winner_user.mention} com {current_game['scores'][winner]} pontos.")

        current_game = None
        question_timer.cancel()

async def show_score(ctx):
    if current_game:
        scores = [f"<@{user_id}>: {score} pontos" for user_id, score in current_game["scores"].items()]
        score_message = "Pontuações:\n" + "\n".join(scores)
    else:
        score_message = "Nenhum jogo está em andamento."
    await ctx.send(score_message)

# Evento para receber respostas dos jogadores
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    global current_game

    if current_game and message.author.id in current_game["players"]:
        answer = message.content.upper()
        if answer in ["A", "B", "C", "D"]:
            if message.author.id in current_game["scores"]:
                question = current_game["questions"][current_game["question_index"]]
                if answer == question["answer"]:
                    current_game["scores"][message.author.id] += 1
                    await message.author.send(f"Correto, {message.author.mention}! Você agora tem {current_game['scores'][message.author.id]} pontos.")
                else:
                    await message.author.send(f"Resposta incorreta, {message.author.mention}.")
                
                current_game["question_index"] += 1
                await update_scoreboard()

                if current_game["question_index"] < len(current_game["questions"]):
                    question = current_game["questions"][current_game["question_index"]]
                    options = "\n".join(question['options'])
                    question_message = (f"{question['question']}\n{options}\n"
                                        "Você tem 30 segundos para responder.")
                    for player_id in current_game["players"]:
                        user = await bot.fetch_user(player_id)
                        await user.send(question_message)

                    # Também envia a próxima pergunta no canal do servidor
                    channel = current_game["channel"]
                    await channel.send(f"Pergunta: {question['question']}\n{options}\n*Os jogadores têm 30 segundos para responder.*")
                else:
                    await end_game()
            else:
                await message.channel.send(f"Você não está jogando no momento, {message.author.mention}.")
        else:
            await message.author.send(f"Resposta inválida, {message.author.mention}. Responda com A, B, C ou D.")
    
    await bot.process_commands(message)

async def update_scoreboard():
    channel = current_game["channel"]
    scores = [f"<@{user_id}>: {score} pontos" for user_id, score in current_game["scores"].items()]
    score_message = "Placar atual:\n" + "\n".join(scores)
    await channel.send(score_message)

bot.run(token)
