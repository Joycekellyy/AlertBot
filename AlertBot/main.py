
import asyncio
from telethon import TelegramClient, events
from telegram import Bot

# ==========================
# CONFIGURAÇÕES
# ==========================

api_id = 32214311                                                     # ► API ID da sua conta do Telegram
api_hash = "8ea019885c2814bdd30e186180499e01"                         # ► API HASH da sua conta
BOT_TOKEN = "8360530327:AAEvQYxvzkIZaW5tCNje-PykNCkz4eq6d30"         # ► Token do bot criado no BotFather
CANAL_ALERTAS = -5022284156                                          # ► ID do canal/grupo que vai receber os alertas

# Onde o BOT do BotFather vai enviar os alertas
# Pode ser o username do canal/grupo (ex: "@meu_canal_alertas") OU o chat_id numérico (-100...)

# ========== CANAIS A SEREM MONITORADOS (links públicos) ==========
CANAIS = [
    "https://t.me/SetupHumilde",
    "https://t.me/ctofertascelulares",
    "https://t.me/TukOferta",
    "https://t.me/consumidorempoderad",
    "https://t.me/promotop",
    "https://t.me/ctofertascelulares",   # repetido na sua lista original (mantido)
    "https://t.me/Fraguas84Oficial",
    "https://t.me/fafaofertas",
    "https://t.me/testeAlertBotizinho",
    "https://t.me/gtOFERTAS",
    "https://t.me/ofertaskabum",
    "https://t.me/descontos_top",
    "https://t.me/ofertasthautec",
    "https://t.me/descontoemgames",
    "https://t.me/descontosmaebebe",
    "https://t.me/ktechpromocoes",
    "https://t.me/PromosdaMih",
    "https://t.me/smarteletrobarato",
    "https://t.me/cupons_desconto",
    "@santostecpromo",
    "https://t.me/opatanapromo"
]

# ========== PALAVRAS-CHAVE ==========
PALAVRAS_CHAVE = [
    "ib55",
    "s23",
    "lg ultragear",
    "mchose v9 pro",
    "mônaco",
    "travesseiro",
    "garrafa de café tramontina",
    "bowl",
    "balde",
    "espremedor de limão",
    "colher de sorvete",
    "organizador de talheres",
    "pano de chão",
    "copo medidor e colheres de medida",
    "saca rolhas",
    "forma de pizza",
    "tigelas bowl alumínio",
    "jarra de suco",
    "cesto de roupa suja",
    "galheteiro manhattan",
    "apoio para bucha e detergente",
    "coador de café inox",
    "potes herméticos com medidor",
    "organizador de ovos",
    "taças caneladas",
    "forma de bolo",
    "garrafa de café tramontina",
    "escorredor de louça",
    "travesseiros",
    "mop",
    "jogo tapete para banheiro",
    "tapete",
    "fronhas",
    "edredom",
    "mondial turbo glass",
    "leonora tramontina",
    "lençol casal buddemeyer",
    "ergonômico",
    "ergonômica",
    "Ergonomica",
    "nimbo",
    "Panasonic Máquina de Lavar",
    "atlas atenas glass",
    "Colchão Queen",
    "Micro-ondas",
    "Panificadora mondial",
    "Purificador de Água",
    "MasterSteam",
    "Air Fryer Gourmet Philco",
    "Chaleira Elétrica",
    "Lorenzetti Loren Shower",
    "Sanduicheira ",
    "Aspirador",
    "Criado-Mudo",
    "tv samsumg",
    "tv 50''", 
]

# (o matching abaixo ignora case)

# ========== INICIALIZA CLIENTES ==========
client = TelegramClient("monitor_bot", api_id, api_hash)
bot = Bot(token=BOT_TOKEN)  # Bot async da lib python-telegram-bot v20+

# ========== FUNÇÃO DE ENVIO DE ALERTA ==========
# Usa o bot (não sua conta) para enviar mensagens ao CANAL_ALERTAS,
# garantindo que as notificações com som aconteçam.
async def enviar_alerta(texto):
    # bot.send_message é coroutine na versão async da lib
    await bot.send_message(chat_id=CANAL_ALERTAS, text=texto)

# ========== FUNÇÃO DE CHECAGEM DAS CHAVES ==========
def contem_chave(texto):
    if not texto:
        return None
    texto = texto.lower()
    for chave in PALAVRAS_CHAVE:
        if chave.lower() in texto:
            return chave
    return None

# ========== HANDLER PRINCIPAL ==========
@client.on(events.NewMessage(chats=CANAIS))
async def handler(event):
    # usa raw_text para pegar texto limpo (ou event.message.message)
    texto_original = (event.message.message or event.raw_text or "")
    texto_lower = texto_original.lower()

    chave = contem_chave(texto_original)
    if chave:
        # tenta obter título do canal (se disponível)
        try:
            chat = await event.get_chat()
            nome_canal = getattr(chat, "title", None) or getattr(chat, "username", None) or str(event.chat_id)
        except Exception:
            nome_canal = str(event.chat_id)

        alerta = (
            f"⚠️ *PALAVRA-CHAVE DETECTADA!* ⚠️\n\n"
            f"*Palavra:* `{chave}`\n"
            f"*Canal:* {nome_canal}\n\n"
            f"*Mensagem detectada:*\n{texto_original}"
        )

        # envia via Bot (isso garantirá notificação sonora para os membros/assinantes)
        try:
            await enviar_alerta(alerta)
            print("Alerta enviado para CANAL_ALERTAS:", chave, "| canal:", nome_canal)
        except Exception as e:
            # loga erro e, como fallback, imprime no console
            print("Erro ao enviar alerta pelo bot:", e)
            print("Alerta (fallback):", alerta)

# ========== LOOP PRINCIPAL (compatível com Python 3.14) ==========
async def main():
    async with client:
        print("🚀 Monitor rodando — observando canais públicos...")
        # opcional: mostrar canais sendo monitorados
        for c in CANAIS:
            print(" -", c)
        await client.run_until_disconnected()

if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    loop.run_until_complete(main())
