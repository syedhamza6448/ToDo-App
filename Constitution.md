# Project Constitution: Spec-Driven Development

This project adheres to Spec-Driven Development (SDD) principles to ensure clarity, quality, and maintainability.

## Core Principles

1.  **Specs First**: No code is written without a corresponding specification. Changes to behavior must start with a change to the spec.
2.  **Single Source of Truth**: The `specs/` directory contains the authoritative definition of the system's behavior.
3.  **Atomic Updates**: Feature implementation involves:
    *   Creating/Updating a spec file in `specs/`.
    *   Reviewing the spec.
    *   Implementing the code to match the spec.
    *   Verifying implementation against the spec.
4.  **Living Documentation**: Specifications are not just planning documents; they are living documentation kept in sync with the codebase.
5.  **Test Alignment**: Tests should validate that the software adheres to the specifications.

## Workflow

1.  **Draft**: Create a Markdown file in `specs/` describing the feature, data models, and logic.
2.  **Refine**: Iterate on the spec until requirements are clear and unambiguous.
3.  **Implement**: Write code (`src/`) that fulfills the spec.
4.  **Verify**: Run tests and manual checks to ensure spec compliance.
