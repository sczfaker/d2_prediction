# 电竞游戏比赛数据分析(dota2)
## 机器学习算法参考这两个库
[用keras抓取分析数据](https://github.com/NosenLiu/Dota2_data_analysis)
[用sklearn分析数据](https://github.com/andreiapostoae/dota2-predictor.git)
## 程序功能使用
|功能描述|相关文件|使用方法|完成程度|
|-|
|给定当前开始的单场比赛的两边选人|dotadata_stat_match_0727.py,dotadata_mining_banpick.py,dotadata_deepkeras.py,dota_pro.py|-|-|-|
|数据清洗|view_data.py,|-|-|-|
|清洗分析除了选人数据以外的数据,以获得更好的模型|dota2_ingame_data_analysis.py,dotadata_teamvalue.py|-|-|-|
|相关数据文件夹|promatch_replay,data_recent_mmr|-|-|-|
|根目录数据文件|matches_list_ranking_2e6_0915.csv,|-|-|
|模型验证|compare_and_backup.py,matches_0727_pro.csv,matches_testset_0727_pro.csv|-|-|
|数据抓取|dota_matchid_0727.py,dotadata_opendota.py,get_games_BY_id_writefile.py,dotadata_teamvalue.py|

## 其他辅助文件功能描述
- *.fdscript
+ 用于修改fiddler根据域名自动保存数据到文件的规则
- one_*.py
+ 用于测试相关片段代码功能
- *.txt
+ html文件保存到本地用于bs4,re模块处理
- *.json文件
+ 保存重要数据用于使用
- inspect_v0727_5536274972.txt
+ 录像文件数据抽取后示例
- mal_*.py
+ 机器学习算法示例
- dotadata*.py
+ 游戏内属性数据
- matchid_*.txt
+ 含比赛奖金比赛的比赛id列表
- promodel_*.pkl|model_*.pkl
+ 职业比赛和普通天梯比赛的生成的预测模型


