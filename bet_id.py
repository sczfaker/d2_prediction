def clear():
    with open ("F:\\cl\\req_gamesportsdata\\raybet_id.log","r+",encoding="utf-8") as f:
        list_of_url=f.readlines()
    key_nonrepeat=[i.split("/api")[-1] for i in list_of_url]
    dict_nonrepeat={}
    for key,value in zip(key_nonrepeat,list_of_url):
    	dict_nonrepeat[key]=value
    list_norepeat=list(dict_nonrepeat.values())
    print (list_norepeat)
    # assert 1>2
    with open ("F:\\cl\\req_gamesportsdata\\request.log","w+",encoding="utf-8") as f:
    	f.writelines(list_norepeat)