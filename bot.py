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

# Criação do bot com o prefixo de comando
bot = commands.Bot(command_prefix='!', intents=intents)

# Perguntas do quiz
questions = [
    {"question": "Qual é a capital da França?", "options": ["A. Paris", "B. Londres", "C. Berlim", "D. Madrid"], "answer": "A"},
    {"question": "Qual é o maior planeta do sistema solar?", "options": ["A. Terra", "B. Marte", "C. Júpiter", "D. Saturno"], "answer": "C"},
    
    {"question": "Qual é a capital do Brasil?", "options": ["A. Rio de Janeiro", "B. Brasília", "C. São Paulo", "D. Salvador"], "answer": "B"},
    {"question": "Quem escreveu 'Dom Casmurro'?", "options": ["A. Machado de Assis", "B. José de Alencar", "C. Jorge Amado", "D. Graciliano Ramos"], "answer": "A"},
    {"question": "Qual é o maior oceano do mundo?", "options": ["A. Oceano Atlântico", "B. Oceano Pacífico", "C. Oceano Índico", "D. Oceano Ártico"], "answer": "B"},
    {"question": "Qual é a fórmula química da água?", "options": ["A. H2O", "B. CO2", "C. O2", "D. NaCl"], "answer": "A"},
    {"question": "Quem pintou a Mona Lisa?", "options": ["A. Leonardo da Vinci", "B. Michelangelo", "C. Rafael", "D. Van Gogh"], "answer": "A"},
    
    {"question": "Qual é o continente onde fica o Egito?", "options": ["A. Ásia", "B. África", "C. Europa", "D. América"], "answer": "B"},
    {"question": "Quem foi o primeiro homem a pisar na Lua?", "options": ["A. Neil Armstrong", "B. Buzz Aldrin", "C. Michael Collins", "D. Yuri Gagarin"], "answer": "A"},
    {"question": "Qual é a fórmula para calcular a área de um triângulo?", "options": ["A. (Base × Altura) / 2", "B. Base × Altura", "C. (Base + Altura) / 2", "D. 2 × (Base + Altura)"], "answer": "A"},
    {"question": "Quem escreveu '1984'?", "options": ["A. George Orwell", "B. Aldous Huxley", "C. Ray Bradbury", "D. Isaac Asimov"], "answer": "A"},
    {"question": "Qual é o maior animal terrestre?", "options": ["A. Elefante", "B. Girafa", "C. Hipopótamo", "D. Rinoceronte"], "answer": "A"},
    
    {"question": "Quem foi o último imperador romano?", "options": ["A. Júlio César", "B. Nero", "C. Constantino", "D. Rômulo Augusto"], "answer": "D"},
    {"question": "Qual é o principal gás responsável pelo efeito estufa?", "options": ["A. Dióxido de Carbono", "B. Metano", "C. Oxigênio", "D. Nitrogênio"], "answer": "A"},
    {"question": "Qual é a fórmula da área de um círculo?", "options": ["A. π × r²", "B. 2 × π × r", "C. π × d", "D. (r²) / π"], "answer": "A"},
    {"question": "Qual é o símbolo químico do ouro?", "options": ["A. Au", "B. Ag", "C. Fe", "D. Pb"], "answer": "A"},
    {"question": "Quem é o autor de 'O Senhor dos Anéis'?", "options": ["A. J.R.R. Tolkien", "B. J.K. Rowling", "C. C.S. Lewis", "D. George R.R. Martin"], "answer": "A"},
    
    {"question": "Qual é o maior deserto do mundo?", "options": ["A. Deserto do Saara", "B. Deserto de Gobi", "C. Deserto de Atacama", "D. Deserto da Antártida"], "answer": "D"},
    {"question": "Qual é o menor país do mundo?", "options": ["A. Mônaco", "B. San Marino", "C. Cidade do Vaticano", "D. Luxemburgo"], "answer": "C"},
    {"question": "Quem foi o líder da Revolução Francesa?", "options": ["A. Napoleão Bonaparte", "B. Maximilien Robespierre", "C. Luís XVI", "D. Georges Danton"], "answer": "B"},
    {"question": "Qual é o nome do livro sagrado do Islã?", "options": ["A. Bíblia", "B. Torá", "C. Alcorão", "D. Vedas"], "answer": "C"},
    {"question": "Qual é a fórmula para calcular o perímetro de um quadrado?", "options": ["A. Lado × 4", "B. Lado × 2", "C. Lado × 3", "D. Lado × 5"], "answer": "A"},
    
    {"question": "Quem pintou 'A Noite Estrelada'?", "options": ["A. Van Gogh", "B. Monet", "C. Picasso", "D. Cézanne"], "answer": "A"},
    {"question": "Qual é a capital da Itália?", "options": ["A. Milão", "B. Roma", "C. Veneza", "D. Florença"], "answer": "B"},
    {"question": "Qual é a moeda oficial do Japão?", "options": ["A. Dólar", "B. Iene", "C. Yuan", "D. Won"], "answer": "B"},
    {"question": "Qual é a fórmula para calcular a velocidade média?", "options": ["A. Distância / Tempo", "B. Tempo / Distância", "C. Distância × Tempo", "D. Distância + Tempo"], "answer": "A"},
    {"question": "Qual é o principal componente da atmosfera terrestre?", "options": ["A. Nitrogênio", "B. Oxigênio", "C. Dióxido de Carbono", "D. Argônio"], "answer": "A"},
    
    {"question": "Quem descobriu a penicilina?", "options": ["A. Alexander Fleming", "B. Louis Pasteur", "C. Jonas Salk", "D. Edward Jenner"], "answer": "A"},
    {"question": "Qual é a fórmula para calcular a área de um retângulo?", "options": ["A. Comprimento × Largura", "B. Comprimento + Largura", "C. (Comprimento + Largura) / 2", "D. (Comprimento × Largura) / 2"], "answer": "A"},
    {"question": "Qual é o planeta mais próximo do Sol?", "options": ["A. Mercúrio", "B. Vênus", "C. Terra", "D. Marte"], "answer": "A"},
    {"question": "Quem escreveu 'Orgulho e Preconceito'?", "options": ["A. Jane Austen", "B. Charlotte Brontë", "C. Emily Brontë", "D. Mary Shelley"], "answer": "A"},
    {"question": "Qual é a função dos ribossomos nas células?", "options": ["A. Sintetizar proteínas", "B. Produzir energia", "C. Armazenar informações genéticas", "D. Dividir a célula"], "answer": "A"},
    
    {"question": "Qual é a fórmula para calcular a área de um trapézio?", "options": ["A. (Base maior + Base menor) × Altura / 2", "B. Base maior × Base menor × Altura", "C. (Base maior - Base menor) × Altura / 2", "D. Base menor × Altura"], "answer": "A"},
    {"question": "Qual é o nome do fenômeno pelo qual a luz é curvada ao passar por um prisma?", "options": ["A. Refração", "B. Reflexão", "C. Difração", "D. Dispersão"], "answer": "D"},
    {"question": "Qual é o maior continente do mundo?", "options": ["A. Ásia", "B. África", "C. América do Norte", "D. Europa"], "answer": "A"},
    {"question": "Quem foi o primeiro presidente dos Estados Unidos?", "options": ["A. George Washington", "B. Abraham Lincoln", "C. Thomas Jefferson", "D. John Adams"], "answer": "A"},
    {"question": "Qual é o nome da primeira missão tripulada para a Lua?", "options": ["A. Apollo 11", "B. Apollo 13", "C. Apollo 8", "D. Apollo 15"], "answer": "A"},
    
    {"question": "Qual é a fórmula para calcular o volume de um cubo?", "options": ["A. Lado³", "B. Lado × 6", "C. Lado × 2", "D. Lado × 4"], "answer": "A"},
    {"question": "Quem é o autor de 'O Pequeno Príncipe'?", "options": ["A. Antoine de Saint-Exupéry", "B. Jules Verne", "C. Charles Dickens", "D. Mark Twain"], "answer": "A"},
    {"question": "Qual é o elemento químico com símbolo Fe?", "options": ["A. Ferro", "B. Flúor", "C. Fósforo", "D. Francio"], "answer": "A"},
    {"question": "Qual é a principal fonte de energia do Sol?", "options": ["A. Fusão nuclear", "B. Fissão nuclear", "C. Reação química", "D. Energia térmica"], "answer": "A"},
    {"question": "Quem escreveu 'A Divina Comédia'?", "options": ["A. Dante Alighieri", "B. Giovanni Boccaccio", "C. Petrarca", "D. Miguel de Cervantes"], "answer": "A"},
    
    {"question": "Qual é a menor unidade de um organismo vivo?", "options": ["A. Célula", "B. Molécula", "C. Átomo", "D. Organoide"], "answer": "A"},
    {"question": "Qual é o símbolo químico do hidrogênio?", "options": ["A. H", "B. He", "C. Hg", "D. Ho"], "answer": "A"},
    {"question": "Quem foi o líder da Revolução Russa de 1917?", "options": ["A. Vladimir Lenin", "B. Josef Stalin", "C. Leon Trotsky", "D. Nicolau II"], "answer": "A"},
    {"question": "Qual é o principal ingrediente da guacamole?", "options": ["A. Abacate", "B. Tomate", "C. Cebola", "D. Pimentão"], "answer": "A"},
    {"question": "Qual é a função das mitocôndrias nas células?", "options": ["A. Produzir energia", "B. Sintetizar proteínas", "C. Armazenar informações genéticas", "D. Dividir a célula"], "answer": "A"},
    
    {"question": "Qual é a fórmula para calcular a densidade?", "options": ["A. Massa / Volume", "B. Volume / Massa", "C. Massa × Volume", "D. Massa + Volume"], "answer": "A"},
    {"question": "Qual é o principal responsável pela mudança das estações do ano?", "options": ["A. Inclinação axial da Terra", "B. Distância da Terra ao Sol", "C. Rotação da Terra", "D. Movimento de translação"], "answer": "A"},
    {"question": "Qual é a principal função dos glóbulos vermelhos?", "options": ["A. Transportar oxigênio", "B. Combater infecções", "C. Coagular o sangue", "D. Produzir hormônios"], "answer": "A"},
    {"question": "Qual é a capital da Espanha?", "options": ["A. Madrid", "B. Barcelona", "C. Sevilha", "D. Valencia"], "answer": "A"},
    {"question": "Qual é o nome do fenômeno que ocorre quando a luz é separada em várias cores ao passar por um prisma?", "options": ["A. Dispersão", "B. Refração", "C. Reflexão", "D. Difração"], "answer": "A"},
    
    {"question": "Qual é a fórmula da lei de Ohm?", "options": ["A. V = I × R", "B. P = V × I", "C. I = V / R", "D. R = V / I"], "answer": "A"},
    {"question": "Qual é a unidade de medida da força no Sistema Internacional?", "options": ["A. Newton", "B. Joule", "C. Watt", "D. Pascal"], "answer": "A"},
    {"question": "Qual é o maior lago de água doce do mundo?", "options": ["A. Lago Baikal", "B. Lago Superior", "C. Lago Vitória", "D. Lago Ontário"], "answer": "A"},
    {"question": "Qual é o nome da famosa obra de Shakespeare que se passa em Verona, Itália?", "options": ["A. Romeu e Julieta", "B. Macbeth", "C. Hamlet", "D. Otelo"], "answer": "A"},
    {"question": "Qual é o nome da camada externa da Terra?", "options": ["A. Crosta", "B. Manto", "C. Núcleo", "D. Litosfera"], "answer": "A"},
    
    {"question": "Qual é o nome do processo pelo qual as plantas produzem seu próprio alimento?", "options": ["A. Fotossíntese", "B. Respiração", "C. Fermentação", "D. Osmose"], "answer": "A"},
    {"question": "Quem foi o fundador da Microsoft?", "options": ["A. Bill Gates", "B. Steve Jobs", "C. Mark Zuckerberg", "D. Elon Musk"], "answer": "A"},
    {"question": "Qual é o nome da teoria que explica a origem do universo?", "options": ["A. Big Bang", "B. Evolução", "C. Relatividade", "D. Quântica"], "answer": "A"},
    {"question": "Qual é o nome do oceano que banha a costa leste dos Estados Unidos?", "options": ["A. Oceano Atlântico", "B. Oceano Pacífico", "C. Oceano Índico", "D. Oceano Ártico"], "answer": "A"},
    {"question": "Quem é o autor de 'Cem Anos de Solidão'?", "options": ["A. Gabriel García Márquez", "B. Mario Vargas Llosa", "C. Julio Cortázar", "D. Carlos Fuentes"], "answer": "A"},
    
    {"question": "Qual é a unidade de medida da intensidade da corrente elétrica?", "options": ["A. Ampère", "B. Volt", "C. Ohm", "D. Watt"], "answer": "A"},
    {"question": "Qual é o nome do continente onde está localizado o deserto de Sahara?", "options": ["A. África", "B. Ásia", "C. América do Sul", "D. Oceania"], "answer": "A"},
    {"question": "Qual é a capital do Canadá?", "options": ["A. Toronto", "B. Montreal", "C. Ottawa", "D. Vancouver"], "answer": "C"},
    {"question": "Qual é o nome do fenômeno natural que ocorre quando um corpo celeste passa entre a Terra e o Sol?", "options": ["A. Eclipse Solar", "B. Eclipse Lunar", "C. Translação", "D. Rotação"], "answer": "A"},
    {"question": "Qual é o nome do sistema de escrita utilizado na Antiga Roma?", "options": ["A. Alfabeto Romano", "B. Alfabeto Grego", "C. Alfabeto Hebraico", "D. Alfabeto Árabe"], "answer": "A"}
]

# Armazenamento dos jogadores e suas pontuações
players = {}
current_game = None
question_timer = None

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
            current_game = {"players": [], "questions": random.sample(questions, 2), "scores": {}, "question_index": 0}
            await ctx.send("Jogo de trivia iniciado! Use !illumi join para participar.")
    elif action == 'score':
        await show_score(ctx)
    else:
        await ctx.send("Uso: !illumi [start|score]")

# Comando para um jogador entrar no jogo
@bot.command()
async def join(ctx):
    global current_game
    if current_game:
        if ctx.author.id in current_game["players"]:
            await ctx.send("Você já está participando do jogo.")
        elif len(current_game["players"]) < 2:
            current_game["players"].append(ctx.author.id)
            current_game["scores"][ctx.author.id] = 0
            if len(current_game["players"]) == 2:
                await ctx.send("Todos os jogadores entraram. O jogo está começando!")
                await start_game()
            else:
                await ctx.send(f"{ctx.author.mention} entrou no jogo. Aguardando o segundo jogador...")
        else:
            await ctx.send("O jogo já está completo.")
    else:
        await ctx.send("Nenhum jogo está em andamento. Use !illumi start para iniciar um jogo.")

async def start_game():
    global current_game, question_timer
    players = current_game["players"]
    questions = current_game["questions"]

    for player_id in players:
        user = await bot.fetch_user(player_id)
        question = questions[current_game["question_index"]]
        options = "\n".join(question['options'])
        question_message = (f"{question['question']}\n{options}\n"
                            "Você tem 30 segundos para responder.")
        await user.send(question_message)

    # Define o temporizador para terminar o jogo após 30 segundos
    question_timer = asyncio.create_task(end_game_after_delay(30))

async def end_game_after_delay(seconds):
    await asyncio.sleep(seconds)
    await end_game()

async def end_game():
    global current_game, question_timer
    if current_game:
        for player_id in current_game["players"]:
            user = await bot.fetch_user(player_id)
            await user.send("O tempo acabou! O jogo terminou. Use !illumi score para ver as pontuações.")

        winner = max(current_game["scores"], key=current_game["scores"].get, default=None)
        if winner:
            winner_user = await bot.fetch_user(winner)
            await winner_user.send(f"Parabéns, {winner_user.mention}! Você venceu com {current_game['scores'][winner]} pontos.")

        current_game = None
        if question_timer:
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

    if current_game and message.author.id in current_game["players"]:
        answer = message.content.upper()
        if answer in ["A", "B", "C", "D"]:
            if message.author.id in current_game["scores"]:
                question = current_game["questions"][current_game["question_index"]]
                if answer == question["answer"]:
                    current_game["scores"][message.author.id] += 1
                    await message.channel.send(f"Correto, {message.author.mention}! Você agora tem {current_game['scores'][message.author.id]} pontos.")
                else:
                    await message.channel.send(f"Resposta incorreta, {message.author.mention}.")
                
                # Move para a próxima pergunta
                current_game["question_index"] += 1
                if current_game["question_index"] < len(current_game["questions"]):
                    # Envia a próxima pergunta
                    question = current_game["questions"][current_game["question_index"]]
                    options = "\n".join(question['options'])
                    question_message = (f"{question['question']}\n{options}\n"
                                        "Você tem 30 segundos para responder.")
                    for player_id in current_game["players"]:
                        user = await bot.fetch_user(player_id)
                        await user.send(question_message)
                else:
                    # Fim do jogo
                    await end_game()
            else:
                await message.channel.send(f"Você não está jogando no momento, {message.author.mention}.")
        else:
            await message.channel.send(f"Resposta inválida, {message.author.mention}. Responda com A, B, C ou D.")
    
    # Processa outros comandos
    await bot.process_commands(message)

bot.run(token)