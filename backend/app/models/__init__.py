"""
Models package - Import all models for Alembic and SQLAlchemy.
"""

from app.models.base import Base
from app.models.user import User
from app.models.language import Language
from app.models.doc_section import DocSection
from app.models.code_example import CodeExample
# from app.models.learning_path import LearningPath
# from app.models.user_progress import UserProgress
# from app.models.practice_problem import PracticeProblem
# from app.models.video_resource import VideoResource
# from app.models.bookmark import Bookmark
# from app.models.user_note import UserNote
# from app.models.discussion import Discussion
# from app.models.discussion_comment import DiscussionComment

__all__ = [
    "Base",
    "User",
    "Language",
    "DocSection",
    "CodeExample",
    # "LearningPath",
    # "UserProgress",
    # "PracticeProblem",
    # "VideoResource",
    # "Bookmark",
    # "UserNote",
    # "Discussion",
    # "DiscussionComment",
]