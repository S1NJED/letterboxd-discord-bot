from pydantic import BaseModel
from typing import Literal, Union
from data import *

class BaseActivity(BaseModel):
	id: int
	type: str
	date: int

	
class WatchedActivity(BaseActivity):
	type: Literal["watched"]
	data: WatchedDataActivity

class RewatchedActivity(BaseActivity):
	type: Literal["rewatched"]
	data: RewatchedDataActivity

class RatedActivity(BaseActivity):
	type: Literal["rated"]
	data: RatedDataActivity

class FollowedActivity(BaseActivity):
	type: Literal["followed"]
	data: FollowedDataActivity

class LikedReviewActivity(BaseActivity):
	type: Literal["liked_review"]
	data: LikedReviewDataActivity

class LikedListActivity(BaseActivity):
	type: Literal["liked_list"]
	data: LikedListDataActivity

class ListedActivity(BaseActivity):
	type: Literal["listed"]
	data: ListedDataActivity

