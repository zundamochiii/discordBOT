# インストールした pycord を読み込む
import discord
import asyncio
import random
import yaml

#ファイルからの読み出し
f = open("./list.txt","r")
list_row = []
for x in f:
    list_row.append(x.rstrip("\n"))
f.close()

with open('config.yaml','r') as yml:
    config = yaml.safe_load(yml)
TOKEN =config['botconfig']['appTOKEN']
CHANNEL_ID =config['botconfig']['messageCHANNEL_ID']


client = discord.Client()
async def greetings():#挨拶
    channel = client.get_channel(CHANNEL_ID)
    await channel.send('こんにちは！')



class Myclass:
    letters = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]
    flag = 0
    gamecount = 0
    def __init__(self):
        self.letters = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]
        self.flag = 0
        self.gamecount = 0

async def greetings():#挨拶
    channel = client.get_channel(CHANNEL_ID)
    await channel.send('こんにちは！')
# 起動時に動作
@client.event
async def on_ready():
    # 起動したらターミナルにログイン通知が表示される
    print('ログインしました')
    await greetings()

# メッセージ受信時に動作する処理
@client.event
async def on_message(message:discord.Message):
    # メッセージ送信者がBotだった場合は無視する
    if message.author.bot:
        return
    # 「/neko」と発言したら「にゃーん」が返る処理
    if message.content == '/neko':
        await message.channel.send('にゃーん')

    if message.content == '/wordle':
        trial = Myclass()
        answer = random.choice(list_row)
        print(f"answer:{answer}")

        while (trial.flag == 0 and trial.gamecount <6):
            await message.channel.send(f"take{trial.gamecount+1}/6 input words here:")
            def check(m):
                #return len(message.content) == 5
                print(m.content)
                return True
            try:
                # wait_forを用いて、イベントが発火し指定した条件を満たすまで待機する
                inpcha = await client.wait_for('message', check=check, timeout=90)
            except asyncio.TimeoutError:
                await message.channel.send(f'{message.author.mention}さん、時間切れです')
                trial.gamecount = trial.gamecount+1
            else:
                # メンション付きでメッセージを送信する。
                chars=inpcha.content
                    #各回限りの配列、緑カウントの初期化
                letterlist= [0 for x in range(5)]
                gcount = 0
                for i in range (5):#lettersの処理
                    if chars[i] in trial.letters:
                        trial.letters.remove(chars[i])
                for i in range (5):#greenの処理
                    if answer[i] == chars[i]:
                        gcount = gcount +1
                        letterlist[i]=2
                for i in range(5):#yellowの処理
                    for j in range(5):
                        if answer[i] != chars[i] and answer[i] == chars[j] and letterlist[j] == 0:
                            letterlist[j]=1
                if gcount != 5:#ここから出力
                    await message.channel.send(f"Correcting:{letterlist}")
                    await message.channel.send(f"Remaining letters:{' '.join(trial.letters)}")
                else:
                    trial.flag = 1
                trial.gamecount = trial.gamecount+1
        await message.channel.send("Game has finished.")
        await message.channel.send(f"Answer is {''.join(answer)}.")
        return



# Botの起動とDiscordサーバーへの接続
client.run(TOKEN)
