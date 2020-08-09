from random import shuffle
from json import dump,load
from itertools import combinations
def team_view(ta,tb):
    with open ("current_p_team.json","r+",encoding="utf-8") as f:
        dict_teamplayer=load(f)
    total,total_du=len([team for team in dict_teamplayer]),len(set([team for team in dict_teamplayer]))
    for team in dict_teamplayer:
        print (team)
        # for player in dict_teamplayer[team]["current_state"]["teammate"]:
            # print(dict_teamplayer[team]             
    teama,teamb=[i["game_id"] for i in dict_teamplayer[ta]["current_state"]["teammate"].values()],[i["game_id"] for i in dict_teamplayer[tb]["current_state"]["teammate"].values()]
    print (teamb,teama)
    for i,j in zip(teama,teamb):
        print (i,"vs",j)
    print (total,total_du)
def team_possibles():
    with open ("current_p_team.json","r+",encoding="utf-8") as f:
        dict_teamplayer=load(f)
    total=[team for team in dict_teamplayer]
    string_list=[]
    for fight in combinations(total,2):
        x="".join([fight[0],"-",fight[1]])
        string_list.append(x)
    shuffle(string_list)
    for fight in string_list:
        print (fight)


if __name__ == '__main__':
    team_possibles()
    # a=input().split("-")
    # team_view(a[0],a[1])

"""
The Toenails
Warriors of the World
Pumpkin Spice Latte
Warwick Ducks
Little Children of Stonehenge
LDN UTD
Into The Breach
Peach
C's Better
Spag and Sons
Bokebi
NoBKB
Your Soul is Mine
Sincerely Fury
Adió Chula
Power of Friendship
Cuteanimegirls
Shadownet
Quincy Crew
4 Zoomers
business associates
beastcoast
Thunder Predator
Infamous
Boonz + Goonz
Pace University
Omega Gaming
Team Brasil
airGERlich
Abfahrt
Recast Gaming
eSport Rhein-Neckar
EURONICS Gaming
Playing Ducks
hehe united
Topf voll Otter
Kolossus
5UpJungz
Team Destiny
IVY
Fnatic
BOOM Esports
Geek Fam
TNC Predator
T1
Team Trust
Sparking Arrow Gaming
Aster.Aries
Motivate.Trust Gaming
Question Mark
Neon Esports
Adroit Esports
NEW Esports
496 Gaming
Execration
032
CR4ZY
Team Zero
Havan Liberty
Infinity Esports
FlyToMoon
Natus Vincere
Cyber Legacy
HellRaisers
Tempo Esports
Khan
Voldemort
Cyberium Seed
EXTREMUM
Gorillaz-Pride
PSG.LGD
EHOME
Vici Gaming
Royal Never Give Up
Invictus Gaming
Team Aster
Team MagMa
LBZS
OG
Team Nigma
Alliance
Team Liquid
VP.Prodigy
Team Secret
84 84
"""