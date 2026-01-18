<!-- Sync Impact Report:
Version change: N/A (initial version) → 1.0.0
Added sections: All principles and sections as specified
Removed sections: None
Templates requiring updates: N/A
Follow-up TODOs: None
-->
# AI/Spec-Driven Book Creation with Integrated RAG Chatbot Constitution


## Core Principles

### Spec-first development using Spec-Kit Plus as the single source of truth
All development follows a specification-first approach using Spec-Kit Plus as the authoritative source. All implementations must strictly adhere to the documented specifications.

### Technical accuracy verified against official documentation
All technical claims and implementations must be verified against official documentation and primary sources. No assumptions or internal knowledge should be used without external verification.

### Clarity for developers, students, and technical practitioners
All documentation, code examples, and explanations must be clear and accessible to developers, students, and technical practitioners at various skill levels.

### Reproducibility: every step, command, and architecture is traceable
Every step, command, and architectural decision must be reproducible and traceable. All processes must work in a clean environment with clear documentation.

### Modularity: book content, code, and chatbot components remain loosely coupled
Book content, code examples, and chatbot components must remain loosely coupled and modular. Changes to one component should not require changes to others unnecessarily.

### Human as Tool Strategy
When encountering ambiguous requirements, unforeseen dependencies, or architectural uncertainty, actively seek user input for clarification and decision-making.


## Key Standards

Book authored using Docusaurus (Markdown/MDX only)
Version-controlled via GitHub; deployed on GitHub Pages
All technical claims must reference official docs or authoritative sources
Code examples must be runnable and aligned with current SDK versions
RAG chatbot must:
  - Use OpenAI Agents/ChatKit SDKs
  - Be served via FastAPI
  - Store structured data in Neon Serverless Postgres
  - Use Qdrant Cloud (Free Tier) for vector search
  - Answer questions strictly from book content
  - Support responses limited to user-selected text only


## Constraints and Success Criteria

No proprietary or undocumented APIs
Free-tier compatible infrastructure only
Clear separation between content ingestion, embedding, retrieval, and generation
Deployment instructions must work on a clean environment
Book successfully builds and deploys on GitHub Pages
RAG chatbot is embedded and fully functional within the book UI
Chatbot answers are context-faithful with no hallucinations
Selected-text-only Q&A works as specified
Spec validation passes without deviation

## Governance

All implementations must follow the Spec-Kit Plus methodology
Amendments to the constitution require explicit documentation and approval
All code changes must reference the specification
Compliance reviews must verify adherence to all principles
Changes must maintain backward compatibility where possible

**Version**: 1.0.0 | **Ratified**: 2026-01-15 | **Last Amended**: 2026-01-15