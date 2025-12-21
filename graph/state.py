from typing import TypedDict, List, Dict, Optional

class NewsroomState(TypedDict):
    topic: str
    plan: Optional[Dict]
    research_data: Optional[List]
    analysis: Optional[Dict]
    draft: Optional[str]
    critique: Optional[Dict]
    final_article: Optional[str]
    revision_count: int  # Track loops to avoid infinite repetition