import random as r, string as s, os, discord
def contra(largo):
    elements = s.ascii_letters+s.ascii_lowercase+s.ascii_uppercase+s.digits+s.punctuation
    password = ''
    for i in range(largo):
        password += r.choice(elements)
    return password
def coin():
    moneda = ["cara", "cruz"]
    select = r.choice(moneda)
    return select

def meme():
    with open("IMG/meme1.jpeg", "rb") as IMG:
        pic = discord.File(IMG)
    return pic

def momo():
    listmeme = r.choice(os.listdir("IMG"))
    with open(f"IMG/{listmeme}", "rb") as IMG:
        pic = discord.File(IMG)
    return pic