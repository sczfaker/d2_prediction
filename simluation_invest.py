
class Simulation_Maxmize_Value(object):
	"""docstring for ClassName"""
	def __init__(self, arg):
		self.arg = arg
		self.PALYER_DICT_FNAME="player_dict.json"
		self.TOUR_FNAME="current_p_team.json"
		self.MATCH_PROCESS="portion_and_more_result.json"
		self.MODEL_DEEP_PREDICT=""
		self.MODEL_LOGIC_PREDICT=""
		self.MODEL_LOGIC_PREDICT_PRO=""
		self.simulation_money=500
		self.ratio_profit_maxmize=0
		self.ratio_profit_current=0
	def make_invest_to_every_possible(self):
		return
    def two_team_futuremeet(self):
        for i in self.match:
            r,d=self.match[i]["dire_team_id"],self.match[i]["radiant_team_id"]
            if r not in self.team_ana:#
                self.team_ana[r]={}
            if d not in self.team_ana:
                self.team_ana[r]={}
        for afight in combinations(self.team_ana.keys(),2):
            self.afight[afight]={}
        print (len(self.afight))
    def get_teamid_tostr(self,rtid,dtid):
        urlprefix="https://api.opendota.com/api/teams/"
        #print(rtid,dtid,len(self.teamid_to_name))
        if rtid in self.teamid_to_name:
            rname=self.teamid_to_name[rtid]["fullname"]
        else:
            rname=rtid
        if dtid in self.teamid_to_name:
            dname=self.teamid_to_name[dtid]["fullname"]
        else:
            dname=dtid
        return rname,dname

if __name__ == '__main__':
	instance=Simulation_Maxmize_Value()

