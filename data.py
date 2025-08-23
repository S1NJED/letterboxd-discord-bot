from typing import Literal
import json

class Base:

	def __repr__(self):
		return json.dumps(self.__dict__, indent=4)

class MovieDataBase:
	movie_name: str
	movie_formatted_name: str
	movie_url: str
	movie_poster_url: str
	# movie_release_date: str

class WatchedDataActivity(MovieDataBase, Base):
	user_rating: str
	user_comment: str | None

class RewatchedDataActivity(MovieDataBase, Base):
	user_rating: str
	user_comment: str | None

class RatedDataActivity(MovieDataBase, Base):
	user_rating: str
	user_comment: str | None

class FollowedDataActivity(Base):
	user_followed_name: str
	user_followed_pfp: str
	user_followed_profile_url: str

# Either review OR list
class LikedReviewDataActivity(MovieDataBase, Base):
	reviewer_username: str
	reviewer_profile_url: str
	reviewer_pfp: str
	reviewer_rating: str

class LikedListDataActivity(Base):
	list_owner_username: str
	list_owner_profile_url: str
	list_owner_pfp: str
	list_name: str
	list_url: str

class ListedDataActivity(Base):
	list_name: str
	list_url: str
	film_amount: int

