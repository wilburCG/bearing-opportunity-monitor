"""initial schema

Revision ID: 0001_initial_schema
Revises:
Create Date: 2026-06-05
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = "0001_initial_schema"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "opportunities",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(length=512), nullable=False),
        sa.Column("summary", sa.Text(), nullable=True),
        sa.Column("opportunity_type", sa.String(length=64), nullable=True),
        sa.Column("industry", sa.String(length=64), nullable=True),
        sa.Column("company_name", sa.String(length=256), nullable=True),
        sa.Column("project_name", sa.String(length=256), nullable=True),
        sa.Column("province", sa.String(length=64), nullable=True),
        sa.Column("city", sa.String(length=64), nullable=True),
        sa.Column("district", sa.String(length=64), nullable=True),
        sa.Column("address", sa.String(length=512), nullable=True),
        sa.Column("latitude", sa.Float(), nullable=True),
        sa.Column("longitude", sa.Float(), nullable=True),
        sa.Column("bearing_types", sa.JSON(), nullable=True),
        sa.Column("bearing_models", sa.JSON(), nullable=True),
        sa.Column("equipment_types", sa.JSON(), nullable=True),
        sa.Column("estimated_quantity", sa.String(length=128), nullable=True),
        sa.Column("estimated_amount", sa.String(length=128), nullable=True),
        sa.Column("deadline_at", sa.DateTime(), nullable=True),
        sa.Column("volume_score", sa.Float(), nullable=False),
        sa.Column("urgency_score", sa.Float(), nullable=False),
        sa.Column("confidence_score", sa.Float(), nullable=False),
        sa.Column("fit_score", sa.Float(), nullable=False),
        sa.Column("total_score", sa.Float(), nullable=False),
        sa.Column("confidence_reason", sa.Text(), nullable=True),
        sa.Column("recommended_action", sa.Text(), nullable=True),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_opportunities_id"), "opportunities", ["id"], unique=False)
    op.create_index(op.f("ix_opportunities_title"), "opportunities", ["title"], unique=False)
    op.create_index(op.f("ix_opportunities_industry"), "opportunities", ["industry"], unique=False)
    op.create_index(op.f("ix_opportunities_company_name"), "opportunities", ["company_name"], unique=False)
    op.create_index(op.f("ix_opportunities_province"), "opportunities", ["province"], unique=False)
    op.create_index(op.f("ix_opportunities_city"), "opportunities", ["city"], unique=False)
    op.create_index(op.f("ix_opportunities_status"), "opportunities", ["status"], unique=False)
    op.create_index(op.f("ix_opportunities_total_score"), "opportunities", ["total_score"], unique=False)

    op.create_table(
        "sources",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("url", sa.String(length=512), nullable=False),
        sa.Column("title", sa.String(length=512), nullable=True),
        sa.Column("source_site", sa.String(length=128), nullable=True),
        sa.Column("source_type", sa.String(length=64), nullable=True),
        sa.Column("published_at", sa.DateTime(), nullable=True),
        sa.Column("fetched_at", sa.DateTime(), nullable=False),
        sa.Column("raw_text_hash", sa.String(length=64), nullable=True),
        sa.Column("content_text", sa.Text(), nullable=True),
        sa.Column("content_summary", sa.Text(), nullable=True),
        sa.Column("credibility_level", sa.String(length=32), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("url"),
    )
    op.create_index(op.f("ix_sources_id"), "sources", ["id"], unique=False)
    op.create_index(op.f("ix_sources_url"), "sources", ["url"], unique=True)
    op.create_index(op.f("ix_sources_source_site"), "sources", ["source_site"], unique=False)
    op.create_index(op.f("ix_sources_source_type"), "sources", ["source_type"], unique=False)
    op.create_index(op.f("ix_sources_raw_text_hash"), "sources", ["raw_text_hash"], unique=False)

    op.create_table(
        "search_tasks",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("task_type", sa.String(length=64), nullable=False),
        sa.Column("query", sa.String(length=512), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("started_at", sa.DateTime(), nullable=True),
        sa.Column("finished_at", sa.DateTime(), nullable=True),
        sa.Column("found_count", sa.Integer(), nullable=False),
        sa.Column("created_opportunity_count", sa.Integer(), nullable=False),
        sa.Column("error_message", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_search_tasks_id"), "search_tasks", ["id"], unique=False)
    op.create_index(op.f("ix_search_tasks_task_type"), "search_tasks", ["task_type"], unique=False)
    op.create_index(op.f("ix_search_tasks_query"), "search_tasks", ["query"], unique=False)
    op.create_index(op.f("ix_search_tasks_status"), "search_tasks", ["status"], unique=False)

    op.create_table(
        "opportunity_sources",
        sa.Column("opportunity_id", sa.Integer(), nullable=False),
        sa.Column("source_id", sa.Integer(), nullable=False),
        sa.Column("evidence_snippet", sa.Text(), nullable=True),
        sa.Column("extraction_confidence", sa.Float(), nullable=False),
        sa.ForeignKeyConstraint(["opportunity_id"], ["opportunities.id"]),
        sa.ForeignKeyConstraint(["source_id"], ["sources.id"]),
        sa.PrimaryKeyConstraint("opportunity_id", "source_id"),
    )

    op.create_table(
        "opportunity_notes",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("opportunity_id", sa.Integer(), nullable=False),
        sa.Column("note", sa.Text(), nullable=False),
        sa.Column("operator", sa.String(length=128), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["opportunity_id"], ["opportunities.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_opportunity_notes_id"), "opportunity_notes", ["id"], unique=False)
    op.create_index(op.f("ix_opportunity_notes_opportunity_id"), "opportunity_notes", ["opportunity_id"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_opportunity_notes_opportunity_id"), table_name="opportunity_notes")
    op.drop_index(op.f("ix_opportunity_notes_id"), table_name="opportunity_notes")
    op.drop_table("opportunity_notes")
    op.drop_table("opportunity_sources")
    op.drop_index(op.f("ix_search_tasks_status"), table_name="search_tasks")
    op.drop_index(op.f("ix_search_tasks_query"), table_name="search_tasks")
    op.drop_index(op.f("ix_search_tasks_task_type"), table_name="search_tasks")
    op.drop_index(op.f("ix_search_tasks_id"), table_name="search_tasks")
    op.drop_table("search_tasks")
    op.drop_index(op.f("ix_sources_raw_text_hash"), table_name="sources")
    op.drop_index(op.f("ix_sources_source_type"), table_name="sources")
    op.drop_index(op.f("ix_sources_source_site"), table_name="sources")
    op.drop_index(op.f("ix_sources_url"), table_name="sources")
    op.drop_index(op.f("ix_sources_id"), table_name="sources")
    op.drop_table("sources")
    op.drop_index(op.f("ix_opportunities_total_score"), table_name="opportunities")
    op.drop_index(op.f("ix_opportunities_status"), table_name="opportunities")
    op.drop_index(op.f("ix_opportunities_city"), table_name="opportunities")
    op.drop_index(op.f("ix_opportunities_province"), table_name="opportunities")
    op.drop_index(op.f("ix_opportunities_company_name"), table_name="opportunities")
    op.drop_index(op.f("ix_opportunities_industry"), table_name="opportunities")
    op.drop_index(op.f("ix_opportunities_title"), table_name="opportunities")
    op.drop_index(op.f("ix_opportunities_id"), table_name="opportunities")
    op.drop_table("opportunities")
