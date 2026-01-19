# ============================================================================
# app/api/v1/practice.py
# ============================================================================
"""Practice problem endpoints."""

from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel, Field

from app.api.deps import get_db, get_current_user
from app.models.user import User
from app.crud.practice_problem import practice_problem_crud, PracticeProblemCreate, PracticeProblemUpdate
from app.crud.doc_section import CRUDDocSection
from app.models.doc_section import DocSection
from app.schemas.response import SuccessResponse
from app.core.logging import logger

router = APIRouter()

doc_section_crud = CRUDDocSection(DocSection)


# ============================================================================
# Schemas
# ============================================================================

class PracticeProblemResponse(BaseModel):
    """Practice problem response schema."""
    id: UUID
    doc_section_id: UUID
    title: str
    platform: str
    difficulty: str
    problem_url: str
    description: Optional[str]
    tags: Optional[List[str]]
    order_index: int
    
    class Config:
        from_attributes = True


class ProblemRecommendation(BaseModel):
    """Recommended practice problem."""
    title: str
    platform: str
    difficulty: str
    url: str
    tags: List[str]
    relevance_score: float


# ============================================================================
# Endpoints
# ============================================================================

@router.get("/sections/{section_id}", response_model=List[PracticeProblemResponse])
async def get_section_problems(
    section_id: UUID,
    difficulty: Optional[str] = Query(None, pattern="^(easy|medium|hard)$"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get practice problems for a documentation section.
    
    Optional filter by difficulty: easy, medium, hard
    """
    # Verify section exists
    section = await doc_section_crud.get(db, id=section_id)
    if not section:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Section not found"
        )
    
    problems = await practice_problem_crud.get_by_section(
        db,
        section_id=section_id,
        difficulty=difficulty
    )
    
    return [PracticeProblemResponse.model_validate(p) for p in problems]


@router.get("/languages/{language_id}", response_model=List[PracticeProblemResponse])
async def get_language_problems(
    language_id: UUID,
    difficulty: Optional[str] = Query(None, pattern="^(easy|medium|hard)$"),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=50),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get all practice problems for a programming language.
    
    Returns problems across all sections of the language.
    Optional filter by difficulty.
    """
    from app.crud.language import CRUDLanguage
    from app.models.language import Language
    
    language_crud = CRUDLanguage(Language)
    
    # Verify language exists
    language = await language_crud.get(db, id=language_id)
    if not language:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Language not found"
        )
    
    problems = await practice_problem_crud.get_by_language(
        db,
        language_id=language_id,
        difficulty=difficulty,
        skip=skip,
        limit=limit
    )
    
    return [PracticeProblemResponse.model_validate(p) for p in problems]


@router.post("/sections/{section_id}", response_model=PracticeProblemResponse, status_code=status.HTTP_201_CREATED)
async def add_problem_to_section(
    section_id: UUID,
    problem_data: PracticeProblemCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Add a practice problem to a section.
    
    **Admin/Contributor feature** - Add authorization check as needed.
    """
    # TODO: Add admin/contributor check
    # if not current_user.is_admin and not current_user.is_contributor:
    #     raise HTTPException(status_code=403, detail="Insufficient permissions")
    
    # Verify section exists
    section = await doc_section_crud.get(db, id=section_id)
    if not section:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Section not found"
        )
    
    # Override section_id
    problem_data.doc_section_id = section_id
    
    # Create problem
    problem = await practice_problem_crud.create(db, obj_in=problem_data)
    await db.commit()
    await db.refresh(problem)
    
    logger.info(f"User {current_user.id} added problem {problem.id} to section {section_id}")
    
    return PracticeProblemResponse.model_validate(problem)


@router.put("/{problem_id}", response_model=PracticeProblemResponse)
async def update_problem(
    problem_id: UUID,
    update_data: PracticeProblemUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update a practice problem. Admin/Contributor feature."""
    # TODO: Add admin/contributor check
    
    problem = await practice_problem_crud.get(db, id=problem_id)
    if not problem:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Problem not found"
        )
    
    updated_problem = await practice_problem_crud.update(db, db_obj=problem, obj_in=update_data)
    await db.commit()
    await db.refresh(updated_problem)
    
    logger.info(f"Problem {problem_id} updated by user {current_user.id}")
    
    return PracticeProblemResponse.model_validate(updated_problem)


@router.delete("/{problem_id}", response_model=SuccessResponse)
async def delete_problem(
    problem_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete a practice problem. Admin/Contributor feature."""
    # TODO: Add admin/contributor check
    
    problem = await practice_problem_crud.get(db, id=problem_id)
    if not problem:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Problem not found"
        )
    
    await practice_problem_crud.delete(db, id=problem_id)
    await db.commit()
    
    logger.info(f"Problem {problem_id} deleted by user {current_user.id}")
    
    return SuccessResponse(
        message="Problem deleted successfully",
        data={"problem_id": str(problem_id)}
    )


@router.get("/recommendations", response_model=List[ProblemRecommendation])
async def get_problem_recommendations(
    language_slug: str = Query(..., description="Programming language slug"),
    skill_level: str = Query("beginner", pattern="^(beginner|intermediate|advanced)$"),
    topic: Optional[str] = Query(None, description="Specific topic (e.g., 'arrays', 'recursion')"),
    max_results: int = Query(10, ge=1, le=20),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get AI-powered practice problem recommendations.
    
    **Premium feature** - Personalized problem suggestions based on:
    - User's skill level
    - Programming language
    - Specific topics/concepts
    - User's learning history
    
    Returns problems from LeetCode, HackerRank, Codeforces, etc.
    """
    # TODO: Implement AI recommendation logic
    # For now, return mock data
    
    logger.info(
        f"User {current_user.id} requested recommendations: "
        f"{language_slug}, {skill_level}, topic={topic}"
    )
    
    # Mock recommendations
    mock_recommendations = [
        ProblemRecommendation(
            title="Two Sum",
            platform="LeetCode",
            difficulty="easy" if skill_level == "beginner" else "medium",
            url="https://leetcode.com/problems/two-sum/",
            tags=["array", "hash-table"],
            relevance_score=0.95
        ),
        ProblemRecommendation(
            title="Valid Parentheses",
            platform="LeetCode",
            difficulty="easy",
            url="https://leetcode.com/problems/valid-parentheses/",
            tags=["string", "stack"],
            relevance_score=0.89
        ),
        ProblemRecommendation(
            title="Binary Search",
            platform="HackerRank",
            difficulty="easy" if skill_level != "advanced" else "medium",
            url="https://www.hackerrank.com/challenges/binary-search",
            tags=["binary-search", "algorithms"],
            relevance_score=0.87
        )
    ]
    
    return mock_recommendations[:max_results]
