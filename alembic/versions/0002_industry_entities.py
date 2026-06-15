"""add industry entities and relationships

Revision ID: 0002_industry_entities
Revises: 0001_initial_schema
Create Date: 2026-06-12
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = "0002_industry_entities"
down_revision: Union[str, None] = "0001_initial_schema"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "companies",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=256), nullable=False),
        sa.Column("alias_names", sa.JSON(), nullable=True),
        sa.Column("company_type", sa.String(length=64), nullable=True),
        sa.Column("industry", sa.String(length=64), nullable=True),
        sa.Column("province", sa.String(length=64), nullable=True),
        sa.Column("city", sa.String(length=64), nullable=True),
        sa.Column("address", sa.String(length=512), nullable=True),
        sa.Column("website", sa.String(length=512), nullable=True),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("tags", sa.JSON(), nullable=True),
        sa.Column("source_url", sa.String(length=512), nullable=True),
        sa.Column("confidence_score", sa.Float(), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
    )
    op.create_index(op.f("ix_companies_id"), "companies", ["id"], unique=False)
    op.create_index(op.f("ix_companies_name"), "companies", ["name"], unique=True)
    op.create_index(op.f("ix_companies_company_type"), "companies", ["company_type"], unique=False)
    op.create_index(op.f("ix_companies_industry"), "companies", ["industry"], unique=False)
    op.create_index(op.f("ix_companies_province"), "companies", ["province"], unique=False)
    op.create_index(op.f("ix_companies_city"), "companies", ["city"], unique=False)
    op.create_index(op.f("ix_companies_status"), "companies", ["status"], unique=False)

    op.create_table(
        "products",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=256), nullable=False),
        sa.Column("model", sa.String(length=128), nullable=True),
        sa.Column("category", sa.String(length=64), nullable=True),
        sa.Column("industry", sa.String(length=64), nullable=True),
        sa.Column("company_id", sa.Integer(), nullable=True),
        sa.Column("manufacturer_name", sa.String(length=256), nullable=True),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("specifications", sa.JSON(), nullable=True),
        sa.Column("application_scenarios", sa.JSON(), nullable=True),
        sa.Column("tags", sa.JSON(), nullable=True),
        sa.Column("source_url", sa.String(length=512), nullable=True),
        sa.Column("confidence_score", sa.Float(), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["company_id"], ["companies.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_products_id"), "products", ["id"], unique=False)
    op.create_index(op.f("ix_products_name"), "products", ["name"], unique=False)
    op.create_index(op.f("ix_products_model"), "products", ["model"], unique=False)
    op.create_index(op.f("ix_products_category"), "products", ["category"], unique=False)
    op.create_index(op.f("ix_products_industry"), "products", ["industry"], unique=False)
    op.create_index(op.f("ix_products_company_id"), "products", ["company_id"], unique=False)
    op.create_index(op.f("ix_products_manufacturer_name"), "products", ["manufacturer_name"], unique=False)
    op.create_index(op.f("ix_products_status"), "products", ["status"], unique=False)

    op.create_table(
        "entity_relationships",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("source_type", sa.String(length=32), nullable=False),
        sa.Column("source_id", sa.Integer(), nullable=False),
        sa.Column("target_type", sa.String(length=32), nullable=False),
        sa.Column("target_id", sa.Integer(), nullable=False),
        sa.Column("relation_type", sa.String(length=64), nullable=False),
        sa.Column("evidence", sa.Text(), nullable=True),
        sa.Column("confidence_score", sa.Float(), nullable=False),
        sa.Column("source_url", sa.String(length=512), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("source_type", "source_id", "target_type", "target_id", "relation_type", name="uq_entity_relationship"),
    )
    op.create_index(op.f("ix_entity_relationships_id"), "entity_relationships", ["id"], unique=False)
    op.create_index(op.f("ix_entity_relationships_source_type"), "entity_relationships", ["source_type"], unique=False)
    op.create_index(op.f("ix_entity_relationships_source_id"), "entity_relationships", ["source_id"], unique=False)
    op.create_index(op.f("ix_entity_relationships_target_type"), "entity_relationships", ["target_type"], unique=False)
    op.create_index(op.f("ix_entity_relationships_target_id"), "entity_relationships", ["target_id"], unique=False)
    op.create_index(op.f("ix_entity_relationships_relation_type"), "entity_relationships", ["relation_type"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_entity_relationships_relation_type"), table_name="entity_relationships")
    op.drop_index(op.f("ix_entity_relationships_target_id"), table_name="entity_relationships")
    op.drop_index(op.f("ix_entity_relationships_target_type"), table_name="entity_relationships")
    op.drop_index(op.f("ix_entity_relationships_source_id"), table_name="entity_relationships")
    op.drop_index(op.f("ix_entity_relationships_source_type"), table_name="entity_relationships")
    op.drop_index(op.f("ix_entity_relationships_id"), table_name="entity_relationships")
    op.drop_table("entity_relationships")
    op.drop_index(op.f("ix_products_status"), table_name="products")
    op.drop_index(op.f("ix_products_manufacturer_name"), table_name="products")
    op.drop_index(op.f("ix_products_company_id"), table_name="products")
    op.drop_index(op.f("ix_products_industry"), table_name="products")
    op.drop_index(op.f("ix_products_category"), table_name="products")
    op.drop_index(op.f("ix_products_model"), table_name="products")
    op.drop_index(op.f("ix_products_name"), table_name="products")
    op.drop_index(op.f("ix_products_id"), table_name="products")
    op.drop_table("products")
    op.drop_index(op.f("ix_companies_status"), table_name="companies")
    op.drop_index(op.f("ix_companies_city"), table_name="companies")
    op.drop_index(op.f("ix_companies_province"), table_name="companies")
    op.drop_index(op.f("ix_companies_industry"), table_name="companies")
    op.drop_index(op.f("ix_companies_company_type"), table_name="companies")
    op.drop_index(op.f("ix_companies_name"), table_name="companies")
    op.drop_index(op.f("ix_companies_id"), table_name="companies")
    op.drop_table("companies")
