import requests
from bs4 import BeautifulSoup
from models import *
from utils import *
from time import sleep
from letterboxdpy.movie import Movie

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
# This one rise 429 error code
# def getMoviePoster(movie_name: str) -> str | None:
    
#     sleep(0.5)

#     url = f"https://letterboxd.com/film/{movie_name}/poster/std/230"
    
#     try:
#         req = requests.get(url)
#         print(req.text)
#         data = req.json() # url, url2x, shouldObfuscate
#         movie_poster = data['url']
#         return movie_poster
#     except Exception as err:
#         print(err)
#         return None # TODO: return defaut image ou jsp

def getMoviePoster(movie_name: str) -> str | None:
    return Movie(movie_name).poster

def getMovieJson(movie_name: str):
    url = f"https://letterboxd.com/film/{movie_name}/json/"

    try:
        req = requests.get(url)
        data = req.json()
        return (data) 
    except Exception as err:
        print(err)
        return None


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

        if activity_type in ["watched",  "rewatched"]:
            data: WatchedDataActivity | RewatchedActivity = WatchedDataActivity()

            # No review
            if "-basic" in section.attrs.get("class"):
                data.movie_name = section.select_one("a:nth-of-type(2)").text.strip()
                data.movie_formatted_name = section.select_one("a:nth-of-type(2)").attrs.get("href").split('/')[3]
                data.movie_url = f"https://letterboxd.com/film/" + data.movie_formatted_name
                data.movie_poster_url = getMoviePoster(data.movie_formatted_name)
                data.user_rating = section.select_one("span.rating").text.strip()
                data.user_comment = None
            # Review
            else:
                data.movie_name = section.select_one("div.body > header > span > h2 > a").text.strip()
                data.movie_formatted_name = section.select_one("div.body > header > span > h2 > a").attrs.get("href").split('/')[3]
                data.movie_url = f"https://letterboxd.com/film/" + data.movie_formatted_name
                data.movie_poster_url = getMoviePoster(data.movie_formatted_name)
                data.user_rating = section.select_one("span.rating").text.strip()
                data.user_comment = section.select_one("div.body > div.js-review > div > p").text

            if f"{activity_type} and rated" in data.movie_name:
                data.movie_name = data.movie_name.replace(f"{activity_type} and rated", "").strip()

        # TODO: handle:
        if activity_type == "rated":
            pass
        elif activity_type == "liked_list":
            pass
        elif activity_type == "liked_review":
            pass
        elif activity_type == "added":
            pass
        elif activity_type == "listed":
            pass

        activities.append({
            "id": activity_id,
            "type": activity_type,
            "date": activity_date,

            "data": data # depends on the type
        })

    return activities
