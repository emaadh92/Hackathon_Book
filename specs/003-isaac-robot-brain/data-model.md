# Data Model: AI-Robot Brain Educational Content

## Overview
Data model for educational content about NVIDIA Isaac technologies, designed to support modular, reusable learning units.

## Core Entities

### LearningModule
- **Fields**:
  - id: string (unique identifier for the module)
  - title: string (module title)
  - description: string (brief overview of the module)
  - category: string (main topic area: "Simulation", "Perception", "Navigation", "Planning")
  - difficulty: enum (Beginner, Intermediate, Advanced)
  - estimatedTime: number (minutes to complete)
  - prerequisites: array of LearningModule ids
  - objectives: array of learning objectives
  - content: ContentBlock[]
  - assessments: Assessment[]
  - createdAt: timestamp
  - updatedAt: timestamp

### ContentBlock
- **Fields**:
  - id: string (unique identifier)
  - type: enum ("text", "diagram", "interactive", "video", "code", "quiz")
  - title: string (optional)
  - content: string (actual content - HTML, Markdown, or structured data)
  - metadata: object (additional data specific to content type)
  - order: number (position within the module)

### Assessment
- **Fields**:
  - id: string (unique identifier)
  - type: enum ("quiz", "practical", "reflection")
  - question: string (the assessment question)
  - options: array (for multiple choice)
  - correctAnswer: string or array (correct response)
  - explanation: string (why this is correct)
  - difficulty: enum (Beginner, Intermediate, Advanced)

### TopicConnection
- **Fields**:
  - id: string (unique identifier)
  - fromModuleId: string (source module)
  - toModuleId: string (target module)
  - relationshipType: enum ("prerequisite", "continuation", "related")
  - description: string (how these modules connect)

## Relationships
- LearningModule contains many ContentBlock entities
- LearningModule contains many Assessment entities
- TopicConnection connects LearningModule entities to show progression and relationships

## Validation Rules
- LearningModule.title must be 5-100 characters
- LearningModule.difficulty must be one of the defined enum values
- ContentBlock.order must be unique within a LearningModule
- ContentBlock.type must be one of the defined enum values
- Estimated time must be greater than 0

## State Transitions
- Draft → Review → Published → Archived (for modules)
- Pending → Submitted → Graded (for assessments)