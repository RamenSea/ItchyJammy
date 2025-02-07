from typing import Dict

import requests
import math
import sys

# funcs
def sort_list_by_rating(v):
	return v["rating_count"]

def sort_list_by_coolness(v):
	return v["coolness"]

def sort_list_by_karma(v):
	c = v["coolness"]
	r = v["rating_count"]
	return math.log(1 + c) - math.log(1 + r) / math.log(5)

def find_game_index(game_id, game_list):
	i = 0
	while i < len(game_list):
		game = game_list[i]
		# if game["game"]["title"] == game_name:
		# 	return i + 1
		if game["game"]["id"] == game_id:
			return i + 1
		i += 1
	return -1

def find_game_name(game_id: int, game_list: list):
	i = 0
	while i < len(game_list):
		game = game_list[i]
		if game["game"]["id"] == game_id:
			return game["game"]["title"]
		i += 1
	return -1


def web_game_filter(game: Dict) -> bool:
	if "game" in game and "platforms" in game.get("game") and "web" in game.get("game").get("platforms"):
		return True
	return False


def run_data(jam_id: str, game_id: int) -> str:
	r = requests.get(f"https://itch.io/jam/{jam_id}/entries.json")
	data = r.json()
	game_list = data["jam_games"]
	original_list = list(game_list)
	web_game_list =  list(filter(web_game_filter, original_list))
	game_count = len(game_list)
	web_game_count = len(web_game_list)
	round_to_digit = 2
	popular_num = find_game_index(game_id, original_list)
	web_popular_num = find_game_index(game_id, web_game_list)
	game_list.sort(reverse=True, key=sort_list_by_rating)
	web_game_list.sort(reverse=True, key=sort_list_by_rating)
	ranking_num = find_game_index(game_id, game_list)
	web_ranking_num = find_game_index(game_id, web_game_list)
	game_list.sort(reverse=True, key=sort_list_by_coolness)
	web_game_list.sort(reverse=True, key=sort_list_by_coolness)
	coolness_num = find_game_index(game_id, game_list)
	web_coolness_num = find_game_index(game_id, web_game_list)
	game_list.sort(reverse=True, key=sort_list_by_karma)
	web_game_list.sort(reverse=True, key=sort_list_by_karma)
	karma_num = find_game_index(game_id, game_list)
	web_karma_num = find_game_index(game_id, web_game_list)
	game_name = find_game_name(game_id, game_list)
	output = f"""Results for "{game_name}" - {game_id}:
=All - {game_count} total=
Popular rank: #{popular_num} - {round(popular_num / game_count * 100, round_to_digit)}%
Rating rank: #{ranking_num} - {round(ranking_num / game_count * 100, round_to_digit)}%
Coolness rank: #{coolness_num} - {round(coolness_num / game_count * 100, round_to_digit)}%
karma_num rank: #{karma_num} - {round(karma_num / game_count * 100, round_to_digit)}%

=Web - {web_game_count} total=
Popular rank: #{web_popular_num} - {round(web_popular_num / web_game_count * 100, round_to_digit)}%
Rating rank: #{web_ranking_num} - {round(web_ranking_num / web_game_count * 100, round_to_digit)}%
Coolness rank: #{web_coolness_num} - {round(web_coolness_num / web_game_count * 100, round_to_digit)}%
karma_num rank: #{web_karma_num} - {round(web_karma_num / web_game_count * 100, round_to_digit)}%
""".strip()
	return output

if __name__ == "__main__":
	jam_id = str(sys.argv[1])
	game_id = int(sys.argv[2])
	output = run_data(jam_id=jam_id, game_id=game_id)
	print(output)
