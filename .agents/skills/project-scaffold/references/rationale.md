# Why This Scaffold Structure

## Problem
Monorepos with 10k+ lines across multiple services are expensive for AI agents to explore. Agents either:
- Read too many files and burn context budget, or
- Skip files and miss critical context (auth, deployment quirks, hardcoded secrets).

## Solution
A 3-layer documentation scaffold that acts as a map:
- **Layer 0 (INDEX):** The table of contents. Agents decide which section matters.
- **Layer 1 (Section):** Overview of one service/area. Agents understand boundaries before opening files.
- **Layer 2 (Sub-section):** Deep dive into one component. Agents read this instead of 5+ source files.

## Maintenance Model
The scaffold is authored once during Phase 1 exploration, then kept in sync with code:
- After significant refactors, audit the affected section.
- After adding a new service, append to INDEX and create its layer-1 main.md.
- The `last audited` timestamp and commit SHA in each file make staleness visible.

## Inspiration
This structure is derived from the EdgeSDR-Nexus monorepo at `scaffold/`.
