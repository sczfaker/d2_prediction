Skip to content
 
Search…
All gists
Back to GitHub
 @tisttsf 
@Da-Capo
Da-Capo
/
DOTADownload.py
Last active 5 months ago • Report abuse
0
0
 Code  Revisions 9
 
<script src="https://gist.github.com/Da-Capo/6c818e7f3c8be341a6c8804e11db075a.js"></script>
  
 DOTADownload.py
import requests
import json
import os
import pandas as pd
import tqdm
import time
import urllib
import shutil
import bz2
from bz2 import decompress
from pathlib import Path

def get_page_source(url):
    headers = {'Accept': '*/*',
               'Accept-Language': 'en-US,en;q=0.8',
               'Cache-Control': 'max-age=0',
               'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36',
               'Connection': 'keep-alive',
               'Referer': 'http://www.baidu.com/'
               }
    for x in range(3):
        req = requests.get(url, headers=headers, timeout = 60)
        if req and req.status_code == 200:
            return req.content
        time.sleep((1 + x) * 3)
    
    return None

def get_match_id(match_id):   
    request_url = "https://api.opendota.com/api/publicMatches?mmr_descending=1&less_than_match_id=" + str(match_id)
    # print(i, request_url)
    while 1:
        try:
            content = get_page_source(request_url).decode("utf-8")
            if content != None:
                json_info = json.loads(content)
                print('get', request_url)
                break
            else:
                print('get error', request_url)
                raise
        except:
            print('get error1', request_url)
            pass
    return json_info

# match_id => replay salt
def get_replay_salt(match_id):
    request_url = "https://api.opendota.com/api/replays?match_id=" + str(match_id)
    # print(i, request_url)
    while 1:
        try:
            content = get_page_source(request_url).decode("utf-8")
            if content != None:
                replay_salt = json.loads(content)
                print('get', request_url)
                break
            else:
                print('get error', request_url)
                raise
        except:
            print('get error1', request_url)
            pass
    return replay_salt

def download_replay(match_id, 
                    cluster,
                    replay_salt):
    url = "http://replay%s.valve.net/570/%s_%s.dem.bz2"%(cluster, match_id, replay_salt)
    dest = "%s_%s.dem.bz2"%(match_id, replay_salt)
    dest1 = "%s_%s.dem"%(match_id, replay_salt)
    try:
        urllib.request.urlretrieve(url, dest)
        print("D", url, dest)
        t = time.time()
        with open(dest1, 'wb') as new_file, bz2.BZ2File(dest, 'rb') as file:  
            for data in iter(lambda : file.read(100 * 1024), b''):
                new_file.write(data)
        print("Bzip2", dest1, time.time()-t)
        return True, dest.split(".")[0]
    except urllib.error.URLError as e:
        print(e.reason, url)
        return False, dest.split(".")[0]

def main(data_dir, query_condition, ex_list=None):
    dem_dir = os.path.join(data_dir, "dem")
    dembz_dir = os.path.join(data_dir, "dembz")
    log_dir = os.path.join(data_dir, "log")
    csv_dir = os.path.join(data_dir, "csv")

    last_match_id = ""
    if ex_list is None:
        exist_list = [fn.name.split("_")[0] for fn in list(Path(csv_dir).glob("*.csv"))]
    else:
        exist_list = ex_list
    while True:
        matches_json = get_match_id(last_match_id)
        if len(matches_json)<=0:
            last_match_id = ""
            continue
        df_matches_all = pd.DataFrame(matches_json)
        last_match_id = df_matches_all['match_id'].values[-1]
        # matches_file = os.path.join(data_dir, "data_5236503318_8w.csv")
        # df_matches_all = pd.read_csv(matches_file)[20000:]
        df_matches = df_matches_all.query(query_condition).reset_index()
        
        from google.colab import output
        output.clear()
        
        for i in range(df_matches.shape[0]):
            print(i, "/",df_matches.shape[0])

            match_id = df_matches['match_id'][i]
            replay_json = get_replay_salt(match_id)
            cluster = replay_json[0]["cluster"]
            replay_salt = replay_json[0]["replay_salt"]
            done, filename = download_replay(match_id, cluster, replay_salt)
                
            if done:
                try:
                    t = time.time()
                    os.system('curl localhost:5600 --data-binary "@%s.dem" > %s.json | exit 1'%(filename, filename))
                    os.system("python ParseJsonRecord.py %s.json %s.csv"%(filename, filename))
                    dur = time.time()-t
                    print("P", dur)
                    df_matches.loc[i].to_json("%s.info"%filename)
                    
                    assert os.path.exists(filename+".dem.bz2")
                    assert os.path.exists(filename+".dem")
                    assert os.path.exists(filename+".json")
                    assert os.path.exists(filename+".csv")
                    assert os.path.exists(filename+".info")

                    # shutil.move(filename+".dem.bz2", os.path.join(dembz_dir, filename+".dem.bz2"))
                    # shutil.move(filename+".dem", os.path.join(dem_dir, filename+".dem"))
                    # shutil.move(filename+".json", os.path.join(log_dir, filename+".json"))
                    
                    os.remove(filename+".dem.bz2")
                    os.remove(filename+".dem")
                    os.remove(filename+".json")

                    shutil.move(filename+".info", os.path.join(csv_dir, filename+".info"))
                    shutil.move(filename+".csv", os.path.join(csv_dir, filename+".csv"))
                    exist_list.append(match_id)
                    print("saved", filename)
                except:
                    exist_list.append(match_id)
                    print("save failed", filename)
                    raise
 ParseJsonRecord.py
import json
import pandas as pd
import itertools
from collections import defaultdict
import sys


# with open("item.json") as f:
#     item_dct=json.load(f)
# with open("hero.json") as f:
#     hero_dct=json.load(f)

item_dct={"item_blink": 1, "item_blades_of_attack": 2, "item_broadsword": 3, "item_chainmail": 4, "item_claymore": 5, "item_helm_of_iron_will": 6, "item_javelin": 7, "item_mithril_hammer": 8, "item_platemail": 9, "item_quarterstaff": 10, "item_quelling_blade": 11, "item_faerie_fire": 237, "item_infused_raindrop": 265, "item_wind_lace": 244, "item_ring_of_protection": 12, "item_stout_shield": 182, "item_recipe_moon_shard": 246, "item_moon_shard": 247, "item_gauntlets": 13, "item_slippers": 14, "item_mantle": 15, "item_branches": 16, "item_belt_of_strength": 17, "item_boots_of_elves": 18, "item_robe": 19, "item_circlet": 20, "item_crown": 261, "item_ogre_axe": 21, "item_blade_of_alacrity": 22, "item_staff_of_wizardry": 23, "item_ultimate_orb": 24, "item_gloves": 25, "item_lifesteal": 26, "item_ring_of_regen": 27, "item_ring_of_tarrasque": 279, "item_sobi_mask": 28, "item_boots": 29, "item_gem": 30, "item_cloak": 31, "item_talisman_of_evasion": 32, "item_cheese": 33, "item_magic_stick": 34, "item_recipe_magic_wand": 35, "item_magic_wand": 36, "item_ghost": 37, "item_clarity": 38, "item_enchanted_mango": 216, "item_flask": 39, "item_dust": 40, "item_bottle": 41, "item_ward_observer": 42, "item_ward_sentry": 43, "item_recipe_ward_dispenser": 217, "item_ward_dispenser": 218, "item_tango": 44, "item_tango_single": 241, "item_courier": 45, "item_flying_courier": 286, "item_tpscroll": 46, "item_recipe_travel_boots": 47, "item_recipe_travel_boots_2": 219, "item_travel_boots": 48, "item_travel_boots_2": 220, "item_recipe_phase_boots": 49, "item_phase_boots": 50, "item_demon_edge": 51, "item_eagle": 52, "item_reaver": 53, "item_relic": 54, "item_hyperstone": 55, "item_ring_of_health": 56, "item_void_stone": 57, "item_mystic_staff": 58, "item_energy_booster": 59, "item_point_booster": 60, "item_vitality_booster": 61, "item_recipe_power_treads": 62, "item_power_treads": 63, "item_recipe_hand_of_midas": 64, "item_hand_of_midas": 65, "item_recipe_oblivion_staff": 66, "item_oblivion_staff": 67, "item_recipe_pers": 68, "item_pers": 69, "item_recipe_poor_mans_shield": 70, "item_poor_mans_shield": 71, "item_recipe_bracer": 72, "item_bracer": 73, "item_recipe_wraith_band": 74, "item_wraith_band": 75, "item_recipe_null_talisman": 76, "item_null_talisman": 77, "item_recipe_mekansm": 78, "item_mekansm": 79, "item_recipe_vladmir": 80, "item_vladmir": 81, "item_recipe_buckler": 85, "item_buckler": 86, "item_recipe_ring_of_basilius": 87, "item_ring_of_basilius": 88, "item_recipe_holy_locket": 268, "item_holy_locket": 269, "item_recipe_pipe": 89, "item_pipe": 90, "item_recipe_urn_of_shadows": 91, "item_urn_of_shadows": 92, "item_recipe_headdress": 93, "item_headdress": 94, "item_recipe_sheepstick": 95, "item_sheepstick": 96, "item_recipe_orchid": 97, "item_orchid": 98, "item_recipe_bloodthorn": 245, "item_bloodthorn": 250, "item_recipe_echo_sabre": 251, "item_echo_sabre": 252, "item_recipe_cyclone": 99, "item_cyclone": 100, "item_recipe_aether_lens": 233, "item_aether_lens": 232, "item_recipe_force_staff": 101, "item_force_staff": 102, "item_recipe_hurricane_pike": 262, "item_hurricane_pike": 263, "item_recipe_dagon": 103, "item_recipe_dagon_2": 197, "item_recipe_dagon_3": 198, "item_recipe_dagon_4": 199, "item_recipe_dagon_5": 200, "item_dagon": 104, "item_dagon_2": 201, "item_dagon_3": 202, "item_dagon_4": 203, "item_dagon_5": 204, "item_recipe_necronomicon": 105, "item_recipe_necronomicon_2": 191, "item_recipe_necronomicon_3": 192, "item_necronomicon": 106, "item_necronomicon_2": 193, "item_necronomicon_3": 194, "item_recipe_ultimate_scepter": 107, "item_ultimate_scepter": 108, "item_recipe_ultimate_scepter_2": 270, "item_ultimate_scepter_2": 271, "item_recipe_refresher": 109, "item_refresher": 110, "item_recipe_assault": 111, "item_assault": 112, "item_recipe_heart": 113, "item_heart": 114, "item_recipe_black_king_bar": 115, "item_black_king_bar": 116, "item_aegis": 117, "item_recipe_shivas_guard": 118, "item_shivas_guard": 119, "item_recipe_bloodstone": 120, "item_bloodstone": 121, "item_recipe_sphere": 122, "item_sphere": 123, "item_recipe_lotus_orb": 221, "item_lotus_orb": 226, "item_recipe_meteor_hammer": 222, "item_meteor_hammer": 223, "item_recipe_nullifier": 224, "item_nullifier": 225, "item_recipe_aeon_disk": 255, "item_aeon_disk": 256, "item_recipe_kaya": 258, "item_kaya": 259, "item_trident": 369, "item_combo_breaker": 276, "item_refresher_shard": 260, "item_recipe_spirit_vessel": 266, "item_spirit_vessel": 267, "item_recipe_vanguard": 124, "item_vanguard": 125, "item_recipe_crimson_guard": 243, "item_crimson_guard": 242, "item_recipe_blade_mail": 126, "item_blade_mail": 127, "item_recipe_soul_booster": 128, "item_soul_booster": 129, "item_recipe_hood_of_defiance": 130, "item_hood_of_defiance": 131, "item_recipe_rapier": 132, "item_rapier": 133, "item_recipe_monkey_king_bar": 134, "item_monkey_king_bar": 135, "item_recipe_radiance": 136, "item_radiance": 137, "item_recipe_butterfly": 138, "item_butterfly": 139, "item_recipe_greater_crit": 140, "item_greater_crit": 141, "item_recipe_basher": 142, "item_basher": 143, "item_recipe_bfury": 144, "item_bfury": 145, "item_recipe_manta": 146, "item_manta": 147, "item_recipe_lesser_crit": 148, "item_lesser_crit": 149, "item_recipe_dragon_lance": 234, "item_dragon_lance": 236, "item_recipe_armlet": 150, "item_armlet": 151, "item_recipe_invis_sword": 183, "item_invis_sword": 152, "item_recipe_silver_edge": 248, "item_silver_edge": 249, "item_recipe_sange_and_yasha": 153, "item_sange_and_yasha": 154, "item_recipe_kaya_and_sange": 272, "item_kaya_and_sange": 273, "item_recipe_yasha_and_kaya": 274, "item_yasha_and_kaya": 277, "item_recipe_satanic": 155, "item_satanic": 156, "item_recipe_mjollnir": 157, "item_mjollnir": 158, "item_recipe_skadi": 159, "item_skadi": 160, "item_recipe_sange": 161, "item_sange": 162, "item_recipe_helm_of_the_dominator": 163, "item_helm_of_the_dominator": 164, "item_recipe_maelstrom": 165, "item_maelstrom": 166, "item_recipe_desolator": 167, "item_desolator": 168, "item_recipe_yasha": 169, "item_yasha": 170, "item_recipe_mask_of_madness": 171, "item_mask_of_madness": 172, "item_recipe_diffusal_blade": 173, "item_diffusal_blade": 174, "item_recipe_ethereal_blade": 175, "item_ethereal_blade": 176, "item_recipe_soul_ring": 177, "item_soul_ring": 178, "item_recipe_arcane_boots": 179, "item_arcane_boots": 180, "item_recipe_octarine_core": 228, "item_octarine_core": 235, "item_orb_of_venom": 181, "item_blight_stone": 240, "item_recipe_ancient_janggo": 184, "item_ancient_janggo": 185, "item_recipe_medallion_of_courage": 186, "item_medallion_of_courage": 187, "item_recipe_solar_crest": 227, "item_solar_crest": 229, "item_smoke_of_deceit": 188, "item_tome_of_knowledge": 257, "item_recipe_veil_of_discord": 189, "item_veil_of_discord": 190, "item_recipe_guardian_greaves": 230, "item_guardian_greaves": 231, "item_recipe_rod_of_atos": 205, "item_rod_of_atos": 206, "item_recipe_iron_talon": 238, "item_iron_talon": 239, "item_recipe_abyssal_blade": 207, "item_abyssal_blade": 208, "item_recipe_heavens_halberd": 209, "item_heavens_halberd": 210, "item_recipe_ring_of_aquila": 211, "item_ring_of_aquila": 212, "item_recipe_tranquil_boots": 213, "item_tranquil_boots": 214, "item_shadow_amulet": 215, "item_recipe_glimmer_cape": 253, "item_glimmer_cape": 254, "item_river_painter": 1021, "item_river_painter2": 1022, "item_river_painter3": 1023, "item_river_painter4": 1024, "item_river_painter5": 1025, "item_river_painter6": 1026, "item_river_painter7": 1027, "item_mutation_tombstone": 1028, "item_super_blink": 1029, "item_pocket_tower": 1030, "item_pocket_roshan": 1032, "item_keen_optic": 287, "item_grove_bow": 288, "item_quickening_charm": 289, "item_philosophers_stone": 290, "item_force_boots": 291, "item_desolator_2": 292, "item_phoenix_ash": 293, "item_seer_stone": 294, "item_greater_mango": 295, "item_elixer": 302, "item_vampire_fangs": 297, "item_craggy_coat": 298, "item_greater_faerie_fire": 299, "item_timeless_relic": 300, "item_mirror_shield": 301, "item_recipe_ironwood_tree": 303, "item_ironwood_tree": 304, "item_mango_tree": 328, "item_royal_jelly": 305, "item_pupils_gift": 306, "item_tome_of_aghanim": 307, "item_repair_kit": 308, "item_mind_breaker": 309, "item_third_eye": 310, "item_spell_prism": 311, "item_princes_knife": 325, "item_witless_shako": 330, "item_imp_claw": 334, "item_flicker": 335, "item_spy_gadget": 336, "item_spider_legs": 326, "item_helm_of_the_undying": 327, "item_recipe_vambrace": 329, "item_vambrace": 331, "item_horizon": 312, "item_fusion_rune": 313, "item_ocean_heart": 354, "item_broom_handle": 355, "item_trusty_shovel": 356, "item_nether_shawl": 357, "item_dragon_scale": 358, "item_essence_ring": 359, "item_clumsy_net": 360, "item_enchanted_quiver": 361, "item_ninja_gear": 362, "item_illusionsts_cape": 363, "item_havoc_hammer": 364, "item_panic_button": 365, "item_apex": 366, "item_ballista": 367, "item_woodland_striders": 368, "item_recipe_trident": 275, "item_demonicon": 370, "item_recipe_fallen_sky": 317, "item_fallen_sky": 371, "item_pirate_hat": 372, "item_dimensional_doorway": 373, "item_ex_machina": 374, "item_faded_broach": 375, "item_paladin_sword": 376, "item_minotaur_horn": 377, "item_orb_of_destruction": 378, "item_the_leveller": 379, "item_arcane_ring": 349, "item_titan_sliver": 381}
hero_dct={"npc_dota_hero_antimage": 1, "npc_dota_hero_axe": 2, "npc_dota_hero_bane": 3, "npc_dota_hero_bloodseeker": 4, "npc_dota_hero_crystal_maiden": 5, "npc_dota_hero_crystalmaiden": 5, "npc_dota_hero_drow_ranger": 6, "npc_dota_hero_drowranger": 6, "npc_dota_hero_earthshaker": 7, "npc_dota_hero_juggernaut": 8, "npc_dota_hero_mirana": 9, "npc_dota_hero_nevermore": 11, "npc_dota_hero_morphling": 10, "npc_dota_hero_phantom_lancer": 12, "npc_dota_hero_phantomlancer": 12, "npc_dota_hero_puck": 13, "npc_dota_hero_pudge": 14, "npc_dota_hero_razor": 15, "npc_dota_hero_sand_king": 16, "npc_dota_hero_sandking": 16, "npc_dota_hero_storm_spirit": 17, "npc_dota_hero_stormspirit": 17, "npc_dota_hero_sven": 18, "npc_dota_hero_tiny": 19, "npc_dota_hero_vengefulspirit": 20, "npc_dota_hero_windrunner": 21, "npc_dota_hero_zuus": 22, "npc_dota_hero_kunkka": 23, "npc_dota_hero_lina": 25, "npc_dota_hero_lich": 31, "npc_dota_hero_lion": 26, "npc_dota_hero_shadow_shaman": 27, "npc_dota_hero_shadowshaman": 27, "npc_dota_hero_slardar": 28, "npc_dota_hero_tidehunter": 29, "npc_dota_hero_witch_doctor": 30, "npc_dota_hero_witchdoctor": 30, "npc_dota_hero_riki": 32, "npc_dota_hero_enigma": 33, "npc_dota_hero_tinker": 34, "npc_dota_hero_sniper": 35, "npc_dota_hero_necrolyte": 36, "npc_dota_hero_warlock": 37, "npc_dota_hero_beastmaster": 38, "npc_dota_hero_queenofpain": 39, "npc_dota_hero_venomancer": 40, "npc_dota_hero_faceless_void": 41, "npc_dota_hero_facelessvoid": 41, "npc_dota_hero_skeleton_king": 42, "npc_dota_hero_skeletonking": 42, "npc_dota_hero_death_prophet": 43, "npc_dota_hero_deathprophet": 43, "npc_dota_hero_phantom_assassin": 44, "npc_dota_hero_phantomassassin": 44, "npc_dota_hero_pugna": 45, "npc_dota_hero_templar_assassin": 46, "npc_dota_hero_templarassassin": 46, "npc_dota_hero_viper": 47, "npc_dota_hero_luna": 48, "npc_dota_hero_dragon_knight": 49, "npc_dota_hero_dragonknight": 49, "npc_dota_hero_dazzle": 50, "npc_dota_hero_rattletrap": 51, "npc_dota_hero_leshrac": 52, "npc_dota_hero_furion": 53, "npc_dota_hero_life_stealer": 54, "npc_dota_hero_lifestealer": 54, "npc_dota_hero_dark_seer": 55, "npc_dota_hero_darkseer": 55, "npc_dota_hero_clinkz": 56, "npc_dota_hero_omniknight": 57, "npc_dota_hero_enchantress": 58, "npc_dota_hero_huskar": 59, "npc_dota_hero_night_stalker": 60, "npc_dota_hero_nightstalker": 60, "npc_dota_hero_broodmother": 61, "npc_dota_hero_bounty_hunter": 62, "npc_dota_hero_bountyhunter": 62, "npc_dota_hero_weaver": 63, "npc_dota_hero_jakiro": 64, "npc_dota_hero_batrider": 65, "npc_dota_hero_chen": 66, "npc_dota_hero_spectre": 67, "npc_dota_hero_doom_bringer": 69, "npc_dota_hero_doombringer": 69, "npc_dota_hero_ancient_apparition": 68, "npc_dota_hero_ancientapparition": 68, "npc_dota_hero_ursa": 70, "npc_dota_hero_spirit_breaker": 71, "npc_dota_hero_spiritbreaker": 71, "npc_dota_hero_gyrocopter": 72, "npc_dota_hero_alchemist": 73, "npc_dota_hero_invoker": 74, "npc_dota_hero_silencer": 75, "npc_dota_hero_obsidian_destroyer": 76, "npc_dota_hero_obsidiandestroyer": 76, "npc_dota_hero_lycan": 77, "npc_dota_hero_brewmaster": 78, "npc_dota_hero_shadow_demon": 79, "npc_dota_hero_shadowdemon": 79, "npc_dota_hero_lone_druid": 80, "npc_dota_hero_lonedruid": 80, "npc_dota_hero_chaos_knight": 81, "npc_dota_hero_chaosknight": 81, "npc_dota_hero_meepo": 82, "npc_dota_hero_treant": 83, "npc_dota_hero_ogre_magi": 84, "npc_dota_hero_ogremagi": 84, "npc_dota_hero_undying": 85, "npc_dota_hero_rubick": 86, "npc_dota_hero_disruptor": 87, "npc_dota_hero_nyx_assassin": 88, "npc_dota_hero_nyxassassin": 88, "npc_dota_hero_naga_siren": 89, "npc_dota_hero_nagasiren": 89, "npc_dota_hero_keeper_of_the_light": 90, "npc_dota_hero_keeperofthelight": 90, "npc_dota_hero_wisp": 91, "npc_dota_hero_visage": 92, "npc_dota_hero_slark": 93, "npc_dota_hero_medusa": 94, "npc_dota_hero_troll_warlord": 95, "npc_dota_hero_trollwarlord": 95, "npc_dota_hero_centaur": 96, "npc_dota_hero_magnataur": 97, "npc_dota_hero_shredder": 98, "npc_dota_hero_bristleback": 99, "npc_dota_hero_tusk": 100, "npc_dota_hero_skywrath_mage": 101, "npc_dota_hero_skywrathmage": 101, "npc_dota_hero_abaddon": 102, "npc_dota_hero_elder_titan": 103, "npc_dota_hero_eldertitan": 103, "npc_dota_hero_legion_commander": 104, "npc_dota_hero_legioncommander": 104, "npc_dota_hero_ember_spirit": 106, "npc_dota_hero_emberspirit": 106, "npc_dota_hero_earth_spirit": 107, "npc_dota_hero_earthspirit": 107, "npc_dota_hero_terrorblade": 109, "npc_dota_hero_phoenix": 110, "npc_dota_hero_oracle": 111, "npc_dota_hero_techies": 105, "npc_dota_hero_winter_wyvern": 112, "npc_dota_hero_winterwyvern": 112, "npc_dota_hero_arc_warden": 113, "npc_dota_hero_arcwarden": 113, "npc_dota_hero_abyssal_underlord": 108, "npc_dota_hero_abyssalunderlord": 108, "npc_dota_hero_monkey_king": 114, "npc_dota_hero_monkeyking": 114, "npc_dota_hero_pangolier": 120, "npc_dota_hero_dark_willow": 119, "npc_dota_hero_darkwillow": 119, "npc_dota_hero_grimstroke": 121, "npc_dota_hero_mars": 129, "npc_dota_hero_void_spirit": 126, "npc_dota_hero_voidspirit": 126, "npc_dota_hero_snapfire": 128}


#item_max_num 349
# hero_max_num 119

reindex_item_dct={}
iReindex=1
for sItem in sorted(item_dct.keys()):
    reindex_item_dct[sItem]=iReindex
    iReindex+=1

item_dct=reindex_item_dct
item_max_num=len(item_dct)
# print("item_max_num",item_max_num)


# Character - hero id
# – Attributes: life state, gold, experience, coordinate(x, y)
# – Statistics:
# • deaths, kills, last hit, denies, assists
# • stacked creeps, stacked camps, killed towers, killed roshans
# • placed observer, placed sentry, rune pickup, team-fight participation
# Items: 244 types

#"hero_id"  "randomed","pred_vict",
proper_list=["hero_id","gold","lh","xp","x","y","stuns","life_state","level","kills"
    ,"deaths","assists","denies","obs_placed","sen_placed","creeps_stacked","camps_stacked",
    "rune_pickups","firstblood_claimed"
    ,"teamfight_participation","towers_killed","roshans_killed","observers_placed"]

item_list=["item_%s"%(i+1) for i in range(item_max_num)]
info_list=proper_list+item_list

heros_info_list=[]
for i in range(10):
    for sKey in info_list:
        hero_key=sKey+"_%s"%i
        heros_info_list.append(hero_key)

df=pd.DataFrame(columns=heros_info_list)



iGap=60
input_file=sys.argv[1]
output_file=sys.argv[2]
assert ".json" in input_file
assert ".csv" in output_file

heros_item_dct=a=defaultdict(lambda :defaultdict(int))#{heroid:{itemid:num}}
with open(input_file) as jsonfile:
    iTimeMax=-1
    iIndex=0
    iCount = 0
    for row in jsonfile:
        row_info=json.loads(row)
        if row_info["type"]=="interval":
            iTime=row_info["time"]
            if iTime<1:
                continue
            if iTime %iGap!=0:
                continue
            if  iCount==0:
                heros_info = [[] for _ in range(10)]
            info=[]
            iSlot=row_info["slot"]
            for sType in proper_list:
                val=row_info.get(sType)
                info.append(val)
            iHero=info[0]

            item_list=[0 for _ in range(item_max_num)]
            for item_id ,iNum in heros_item_dct[iHero].items():
                item_list[item_id-1]=iNum
            info+=item_list
            heros_info[iSlot]=info
            iCount+=1
            if iCount>=10:
                temp=list(itertools.chain(*heros_info))
                df.loc[iIndex] = temp
                iIndex+=1
                iCount=0
                if iTime>iTimeMax:
                    iTimeMax=iTime
        elif row_info["type"]=="DOTA_COMBATLOG_PURCHASE":
            item_name=row_info["valuename"]
            iItem_id=item_dct[item_name]
            # print("item_name",item_name,iItem_id)
            if iItem_id:
                owner=row_info["targetname"]
                hero_id=hero_dct.get(owner)
                if not hero_id:
                    print("errr",hero_id,owner)
                heros_item_dct[hero_id][iItem_id]+=1
# print("item_dct.keys",heros_item_dct.keys())
if df.shape[0]>1:
    df.to_csv(output_file)
 @tisttsf
 
 
Leave a comment

Attach files by dragging & dropping, selecting or pasting them.
© 2020 GitHub, Inc.
Terms
Privacy
Security
Status
Help
Contact GitHub
Pricing
API
Training
Blog
About
