import requests
from bs4 import BeautifulSoup
from models import *
from datetime import datetime
from utils import *

HEADERS = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:129.0) Gecko/20100101 Firefox/129.0"
}
TYPES = [
    "rated",
    "watched",
    "rewatched",
    "added",
    "liked",
    "followed"
]


# movie-name
def getMoviePoster(movie_name: str) -> str | None:
    url = f"https://letterboxd.com/film/{movie_name}/poster/std/230"

    try:
        req = requests.get(url)
        data = req.json() # url, url2x, shouldObfuscate
        movie_poster = data['url']
        return movie_poster
    except:
        return None # TODO: return defaut image ou jsp


def getUserActivty(username: str) -> list[WatchedActivity | RewatchedActivity | RatedActivity | FollowedActivity | LikedReviewActivity | LikedListActivity | ListedDataActivity]:
    url = "https://letterboxd.com/ajax/activity-pagination/" + username
    print(url)
    req = requests.get(url, headers=HEADERS)

    soup = BeautifulSoup(req.text, features="html.parser")

    sections = soup.select("section[data-activity-id]")

    activities = []
    for section in sections:

        activity_id = section.attrs['data-activity-id']
        activity_date = convert_datetime(section.select_one("time").attrs.get("datetime"))

        if "-review" in section.attrs.get("class"):
            activity_name = section.select_one("div.body > div.attribution-detail").get_text().strip()
            activity_type = activity_name.split()[1]

        elif "-basic" in section.attrs.get("class"):
            activity_name = section.select_one("div > p").get_text().strip()
            activity_type = activity_name.split()[1]

        data = {}

        # TODO: if `liked` check if its for a review or a list
        if activity_type == "liked":
            if "/list/" in section.select_one("a:nth-of-type(2)").attrs.get("href"):
                activity_type = "liked_list"
            else:
                activity_type = "liked_review"

        # no review
        if activity_type in ["watched",  "rewatched"]:
            data: WatchedDataActivity | RewatchedActivity = WatchedDataActivity()

            if "-basic" in section.attrs.get("class"):
                data.movie_name = section.select_one("a:nth-of-type(2)").text.strip()
                data.movie_formatted_name = section.select_one("a:nth-of-type(2)").attrs.get("href").split('/')[2]
                data.movie_url = f"https://letterboxd.com/film/" + data.movie_formatted_name
                data.movie_poster_url = getMoviePoster(data.movie_formatted_name)
                data.user_rating = section.select_one("span.rating").text.strip()
                data.user_comment = None
            else:
                data.movie_name = section.select_one("div.body > header > span > h2 > a").text.strip()
                data.movie_formatted_name = section.select_one("div.body > header > span > h2 > a").attrs.get("href").split('/')[2]
                data.movie_url = f"https://letterboxd.com/film/" + data.movie_formatted_name
                data.movie_poster_url = getMoviePoster(data.movie_formatted_name)
                data.user_rating = section.select_one("span.rating").text.strip()
                data.user_comment = section.select_one("div.body > div.js-review > div > p").text

            if f"{activity_type} and rated" in data.movie_name:
                data.movie_name = data.movie_name.replace(f"{activity_type} and rated", "").strip()

        # if activity_type in ["watched", "rewatched", "rated", "liked_review"]:
            
        #     '''
        #     watched (review) X 
        #     watched and rated X
        #     rewatched (review)
        #     rewatched and rated
        #     rated
        #     '''
            
        #     data = {
        #         "movie"
        #     }


        activities.append({
            "id": activity_id,
            "type": activity_type,
            "date": activity_date,

            "data": data # depends on the type
        })

    return activities
