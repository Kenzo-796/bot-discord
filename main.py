import discord
from discord.ext import commands
from datetime import timedelta
import json
import random

TOKEN = "Orion Tokens"

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

# ===== WARN SYSTEM =====

def load_warns():
    try:
        with open("warns.json", "r") as f:
            return json.load(f)
    except:
        return {}

def save_warns(data):
    with open("warns.json", "w") as f:
        json.dump(data, f, indent=4)

warns = load_warns()

# ===== READY =====

@bot.event
async def on_ready():
    print(f"✅ Bot online como {bot.user}")

# ===== MODERAÇÃO =====

@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, motivo="Sem motivo"):
    await member.ban(reason=motivo)
    await ctx.send(f"🔨 {member.mention} foi banido.\nMotivo: {motivo}")


@bot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, motivo="Sem motivo"):
    await member.kick(reason=motivo)
    await ctx.send(f"👢 {member.mention} foi expulso.\nMotivo: {motivo}")


@bot.command()
@commands.has_permissions(moderate_members=True)
async def mute(ctx, member: discord.Member, minutos: int):
    tempo = timedelta(minutes=minutos)
    await member.timeout(tempo)
    await ctx.send(f"🔇 {member.mention} mutado por {minutos} minutos.")


@bot.command()
@commands.has_permissions(moderate_members=True)
async def unmute(ctx, member: discord.Member):
    await member.timeout(None)
    await ctx.send(f"🔊 {member.mention} desmutado.")


# ===== WARN =====

@bot.command()
@commands.has_permissions(manage_messages=True)
async def warn(ctx, member: discord.Member, *, motivo="Sem motivo"):
    gid = str(ctx.guild.id)
    uid = str(member.id)

    if gid not in warns:
        warns[gid] = {}

    if uid not in warns[gid]:
        warns[gid][uid] = []

    warns[gid][uid].append(motivo)
    save_warns(warns)

    await ctx.send(f"⚠️ {member.mention} recebeu um aviso.\nMotivo: {motivo}")


@bot.command()
async def warnings(ctx, member: discord.Member):
    gid = str(ctx.guild.id)
    uid = str(member.id)

    if gid in warns and uid in warns[gid]:
        lista = warns[gid][uid]
        texto = "\n".join([f"{i+1}. {w}" for i, w in enumerate(lista)])
        await ctx.send(f"📄 Avisos de {member.mention}:\n{texto}")
    else:
        await ctx.send("Esse usuário não possui avisos.")


# ===== ENTRETENIMENTO =====

@bot.command()
async def dado(ctx):
    await ctx.send(f"🎲 Número: {random.randint(1,6)}")


@bot.command()
async def piada(ctx):
    piadas = [
        "Por que o computador foi ao médico? Porque estava com vírus 😂",
        "Qual é o café mais perigoso? O ex-presso ☕",
        "Por que o livro de matemática ficou triste? Porque tinha muitos problemas 📚"
    ]
    await ctx.send(random.choice(piadas))


@bot.command()
async def oito_bola(ctx, *, pergunta):
    respostas = ["Sim", "Não", "Talvez", "Com certeza", "Pergunte depois"]
    await ctx.send(f"🔮 {random.choice(respostas)}")

import random

@bot.command()
async def ptt(ctx, escolha: str):
    opcoes = ["pedra", "papel", "tesoura"]
    bot_escolha = random.choice(opcoes)

    if escolha.lower() not in opcoes:
        await ctx.send("Escolha pedra, papel ou tesoura.")
        return

    if escolha.lower() == bot_escolha:
        resultado = "Empate!"
    elif (
        (escolha.lower() == "pedra" and bot_escolha == "tesoura") or
        (escolha.lower() == "papel" and bot_escolha == "pedra") or
        (escolha.lower() == "tesoura" and bot_escolha == "papel")
    ):
        resultado = "Você ganhou!"
    else:
        resultado = "Você perdeu!"

    await ctx.send(f"Eu escolhi **{bot_escolha}**. {resultado}")


@bot.command()
async def coin(ctx):
    await ctx.send(f"🪙 Resultado: {random.choice(['Cara', 'Coroa'])}")


@bot.command()
async def numero(ctx, maximo: int = 100):
    await ctx.send(f"🎲 Número: {random.randint(0, maximo)}")


@bot.command()
async def ship(ctx, user1: discord.Member, user2: discord.Member):
    porcentagem = random.randint(0, 100)
    await ctx.send(f"❤️ Compatibilidade entre {user1.mention} e {user2.mention}: **{porcentagem}%**")


@bot.command()
async def taxa(ctx, *, coisa):
    nota = random.randint(0, 100)
    await ctx.send(f"🔥 Eu dou **{nota}%** para {coisa}")


@bot.command()
async def sorte(ctx):
    frases = [
        "Hoje será um ótimo dia!",
        "Algo inesperado vai acontecer.",
        "Boa sorte está chegando.",
        "Talvez seja melhor descansar hoje.",
        "Uma surpresa vem aí."
    ]
    await ctx.send(f"🍀 {random.choice(frases)}")


@bot.command()
async def biscoito(ctx):
    frases = [
        "Você encontrará felicidade em breve.",
        "Grandes oportunidades estão vindo.",
        "Confie mais em si mesmo.",
        "Uma amizade nova surgirá.",
        "Algo bom está para acontecer."
    ]
    await ctx.send(f"🥠 {random.choice(frases)}")

bot.run("MTQ3NTU4OTM0MzQzODQzODQ2MA.GDVK32.06OZ6pE3uSry70Tx6gdDKEl3sBOjFdXa2akB5M")
