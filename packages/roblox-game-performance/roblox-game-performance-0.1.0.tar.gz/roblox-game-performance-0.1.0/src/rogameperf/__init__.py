import requests
import json
import time
from lxml import html
from requests import Session
from datetime import datetime
from typing import Any, TypedDict

GAME_URL_PREFIX = "https://www.roblox.com/games/"

def dump_element(element) -> str:
	return (html.tostring(element)).decode('utf-8')

class AdIntValueData(TypedDict):
	Current: int
	Total: int

class AdFloatValueData(TypedDict):
	Current: float
	Total: float

class AdData(TypedDict):
	Title: str
	Id: str
	PlaceId: int
	Type: str
	IsRunning: bool
	Clicks: AdIntValueData
	CTR: AdFloatValueData
	Bid: AdIntValueData
	Impressions: AdIntValueData
	CPC: AdFloatValueData

class RatingData(TypedDict):
	Likes: int
	Dislikes: int

class GameData(TypedDict):
	Rating: RatingData
	Favorites: int
	Visits: int
	Concurrents: int

class RecordData(TypedDict):
	Timestamp: str
	PlaceId: int
	Advertisements: list[AdData]
	Game: GameData | None

class PerformanceTracker():
	session: Session
	place_id: int
	universe_id: int
	group_id: int
	
	def __init__(
		self,
		rbx_security_cookie: str,
		place_id: int,
		group_id: int
	):
		self.place_id = place_id
		self.group_id = group_id
		
		# get authorized session
		session = requests.Session()
		session.cookies.update({
			".ROBLOSECURITY": rbx_security_cookie
		})
		self.session = session

		# get universe id
		for place in json.loads(session.get(f"https://games.roblox.com/v1/games/multiget-place-details?placeIds={place_id}").text):
			self.universe_id = int(place["universeId"])

		assert self.universe_id, f"no universe id found for {place_id}"

	def read_ads(self) -> list[AdData]:

		response = self.session.get(f"https://www.roblox.com/develop/groups/{self.group_id}?Page=ads")
		tree = html.fromstring(response.text)

		ads = []

		try:
			for tabl in tree.xpath('//table[@data-ad-type]'):
				# get title
				ad_id = tabl.get("data-item-id")
				ad_type = tabl.get("data-ad-type")
				place_id: int
				ad_title: str
				for title in tabl.xpath('.//td[@colspan="6"]'):
				
					for span in title.xpath(".//span[not(@href) and @class='title']"):
						ad_title = span.text

					for a in title.xpath('.//a[@href]'):
						a_url = a.get("href")
						if GAME_URL_PREFIX in a_url:
							url_end = a_url.replace(GAME_URL_PREFIX, "")
							place_id = int(url_end.split("/")[0])

				# get stats
				clicks: int
				total_clicks: int
				ctr: float
				total_ctr: float
				bid: int
				total_bid: int
				impressions: int
				total_impressions: int
				is_running: bool = len(tabl.xpath("//*[text()='Not running']")) == 0
				for stats in tabl.xpath('.//td[@class="stats-col"]'):
					for div in stats.xpath(".//div[not(@title) and @class='totals-label']"):
						for span in div.xpath(".//span"):
							if "Clicks" in div.text:
								clicks = int(span.text)
							elif "Bid" in div.text:
								bid = int(span.text)
							elif "CTR" in div.text:
								ctr = float(span.text.replace("%", ""))/100
							elif "Impressions" in div.text:
								impressions = int(span.text)

					for div in stats.xpath(".//div[@title and @class='totals-label']"):
						for span in div.xpath(".//span"):
							if "Clicks" in div.text:
								total_clicks = int(span.text)
							elif "Bid" in div.text:
								total_bid = int(span.text)
							elif "CTR" in div.text:
								total_ctr = float(span.text.replace("%", ""))/100
							elif "Impr" in div.text:
								total_impressions = int(span.text)

				ad_data: AdData = {
					"Title": ad_title,
					"Id": ad_id,
					"PlaceId": place_id,
					"Type": ad_type,
					"IsRunning": is_running,
					"Clicks": {
						"Current": clicks,
						"Total": total_clicks,
					},
					"CTR": {
						"Current": ctr,
						"Total": total_ctr,
					},
					"Bid": {
						"Current": bid,
						"Total": total_bid,
					},
					"Impressions": {
						"Current": impressions,
						"Total": total_impressions,
					},
					"CPC": {
						"Current": float(bid)/float(max(clicks,1)),
						"Total": float(total_bid)/float(max(total_clicks,1)),
					},
				}
				if self.place_id == place_id:
					ads.append(ad_data)
		except:
			print("Recording ads failed")

		return ads

	def read_concurrents(self) -> int: 
		response = self.session.get(GAME_URL_PREFIX+str(self.place_id))
		tree = html.fromstring(response.text)
		
		try:
			for element in tree.xpath("//li[@class='game-stat game-stat-width-voice']"):
				for stat in element.xpath(".//p[@class='text-label text-overflow font-caption-header']"):
					if stat.text == "Active":
						for val in element.xpath(".//p[@class='text-lead font-caption-body wait-for-i18n-format-render invisible']"):
							return int(val.text.replace(",", ""))
		except:
			return 0

		return 0

	def get_game_data(self) -> GameData | None:

		try:
			# get like / dislike
			likes: int
			dislikes: int
			for entry in json.loads(self.session.get(f"https://games.roblox.com/v1/games/votes?universeIds={self.universe_id}").text)["data"]:
				if entry["id"] == self.universe_id:
					likes = entry["upVotes"]
					dislikes = entry["downVotes"]

			# get favorites
			favorites: int = json.loads(self.session.get(f"https://games.roblox.com/v1/games/{self.universe_id}/favorites/count").text)["favoritesCount"]
			
			# parse for concurrents and visits
			response = self.session.get(GAME_URL_PREFIX+str(self.place_id))
			tree = html.fromstring(response.text)

			# get visits
			visits: int
			for element in tree.xpath("//p[@id='game-visit-count']"):
				visits = int(element.get("title").replace(",", ""))

			concurrents = self.get_concurrents()

			game_data: GameData = {
				"Rating": {
					"Likes": likes,
					"Dislikes": dislikes,
				},
				"Favorites": favorites,
				"Visits": visits,
				"Concurrents": concurrents,
			}

			return game_data
		except:
			return None

	def dump(self) -> RecordData:

		data: RecordData = {
			"Timestamp": datetime.now().timestamp(),
			"PlaceId": self.place_id,
			"Advertisements": self.get_ads(),
			"Game": self.get_game_stats(),
		}