from sqlalchemy import (
    Column, Integer, String, Text, Boolean, Date,
    DateTime, ForeignKey, JSON, UniqueConstraint
)
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.sql import func

Base = declarative_base()


class ConceptSet(Base):
    __tablename__ = "concept_set"

    id               = Column(Integer, primary_key=True)
    concept_set_name = Column(String(255), nullable=False, unique=True)
    description      = Column(Text)
    domain_id        = Column(String(50))
    project_id       = Column(String(255))
    doi              = Column(String(255))
    created_by       = Column(String(255))
    created_at       = Column(DateTime, server_default=func.now())
    modified_at      = Column(DateTime, server_default=func.now(), onupdate=func.now())

    versions = relationship("ConceptSetVersion", back_populates="concept_set")


class ConceptSetVersion(Base):
    __tablename__ = "concept_set_version"

    version_id        = Column(Integer, primary_key=True)
    concept_set_id    = Column(Integer, ForeignKey("concept_set.id"), nullable=False)
    version_number    = Column(Integer, nullable=True)  # assigned at finalization only
    version_name      = Column(String(255), nullable=False)
    status            = Column(String(20), nullable=False, default="draft")  # draft / in_review / final
    parent_version_id = Column(Integer, ForeignKey("concept_set_version.version_id"), nullable=True)
    ohdsi_expression  = Column(JSON)
    rationale         = Column(Text)
    scope_notes       = Column(Text)
    author_name       = Column(String(255))
    research_study_id = Column(String(255))
    created_at        = Column(DateTime, server_default=func.now())
    modified_at       = Column(DateTime, server_default=func.now(), onupdate=func.now())

    concept_set    = relationship("ConceptSet", back_populates="versions")
    parent_version = relationship("ConceptSetVersion", remote_side="ConceptSetVersion.version_id")
    reviewers      = relationship("Reviewer", back_populates="version")
    members        = relationship("ConceptSetMember", back_populates="version")


class Reviewer(Base):
    __tablename__ = "reviewer"

    id         = Column(Integer, primary_key=True)
    version_id = Column(Integer, ForeignKey("concept_set_version.version_id"), nullable=False)
    name       = Column(String(255), nullable=False)
    email      = Column(String(255), nullable=False)
    role       = Column(String(100))       # SME / Informatician / Clinician / Domain Expert
    decision   = Column(String(20), default="pending")  # pending / approved / rejected
    notes      = Column(Text)
    decided_at = Column(DateTime)

    version = relationship("ConceptSetVersion", back_populates="reviewers")


class ConceptSetMember(Base):
    __tablename__ = "concept_set_member"

    id                  = Column(Integer, primary_key=True)
    version_id          = Column(Integer, ForeignKey("concept_set_version.version_id"), nullable=False)

    # OHDSI TAB spec fields (camelCase in JSON → snake_case in DB)
    # schema: https://raw.githubusercontent.com/ohdsi/tab/main/docs/schemas/concept-set-schema.json
    concept_id          = Column(Integer, nullable=False)
    concept_name        = Column(String(255))
    domain_id           = Column(String(20))
    vocabulary_id       = Column(String(20))
    concept_class_id    = Column(String(20))
    standard_concept    = Column(String(1))   # "S", "C", or null
    concept_code        = Column(String(50))
    valid_start_date    = Column(Date)
    valid_end_date      = Column(Date)
    invalid_reason      = Column(String(1))   # "D" (deleted), "U" (updated), or null

    # Required OHDSI expression flags
    is_excluded         = Column(Boolean, nullable=False, default=False)
    include_descendants = Column(Boolean, nullable=False, default=False)
    include_mapped      = Column(Boolean, nullable=False, default=False)

    # N3C / curation additions
    descendant_count    = Column(Integer)     # Phase 2: populated via WebAPI resolve
    review_status       = Column(String(50))
    review_comment      = Column(Text)
    created_by          = Column(String(255))
    created_at          = Column(DateTime, server_default=func.now())
    modified_at         = Column(DateTime, server_default=func.now(), onupdate=func.now())

    version = relationship("ConceptSetVersion", back_populates="members")
