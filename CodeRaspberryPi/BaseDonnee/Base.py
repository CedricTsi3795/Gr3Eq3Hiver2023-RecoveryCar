import sqlite3
import hashlib
#variable qui me permet d'établir ma connexion
con = sqlite3.connect("info.db")
#mes deux curseurs qui me permettent de parcourir ma base de donnée
cur2=con.cursor()
cur = con.cursor()
## nouv base: cur.execute("CREATE TABLE info(identifiants,motDePasse )")
#va permettre de crypter nos mots de passe
def crypter(mdp):
    mdp=mdp.encode()
    #J'ai utilisé sha3_256 pour hasher
    mdp = hashlib.sha3_256(mdp).hexdigest()
    return mdp

##va permettre d'ajouter un nouvel utilisateur dans notre base de donnée
def ajouterUtilisateur(id, mdp):
    mdp=crypter(mdp)
    values = [
    (id, mdp)
    ]
    cur.executemany("INSERT INTO info VALUES(?, ?)", values)
    con.commit()

        
#ajouterUtilisateur("Admin","admin")

##comparer les mots de passe et les noms d'utilisateurs proposés pas les utilisateurs à ceux qui sont dans la base de donnée
#retourne true ou false selon la validité de ce qui a été entré
def comparerMdp(id2, mdp2):
    for row in cur.execute("SELECT identifiants,motDePasse FROM info"):
        #Je convertis la ligne de byte à String
        row=str(row)
        # ce qui a été noté par l'usager
        infoFournie="('"+id2+"', '"+crypter(mdp2)+"')"
        print(infoFournie)
        print(row)
        if infoFournie==row:
            return True
    return False
       

