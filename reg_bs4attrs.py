from bs4 import BeautifulSoup
import re
with open("1_ESL Meisterschaft 2020 Season 1_31477.txt","r+",encoding="utf-8") as f:
    one_tour_text=f.read()
    bs4_obejct=BeautifulSoup(one_tour_text,"html.parser")
    p_object=bs4_obejct.find("div",attrs={"style":re.compile("max-width:\d{4}")})#max-width:1200px;
    print (p_object)
    if p_object:
        team_list=p_object.find_all("div",class_="template-box")
    else:
        print (p_object)