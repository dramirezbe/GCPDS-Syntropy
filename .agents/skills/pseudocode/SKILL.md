---
name: pseudocode
description: "Trigger: pseudocode, write pseudocode, algorithm design, sketch algorithm, pseudocode review, understand pseudocode. Create, interpret, and validate educational pseudocode across all common programming constructs."
license: Apache-2.0
metadata:
  author: gentleman-programming
  version: "1.0"
---

## Activation Contract

Use this skill when:
- a user asks to write, read, or explain pseudocode;
- an algorithm needs to be sketched before implementation;
- pseudocode must be translated to or from a real programming language;
- a user wants to learn or teach pseudocode syntax and conventions.

Do not use for:
- production code in a specific language (use language-specific skills instead);
- one-off explanations that do not need the full reference;
- runtime or performance analysis without algorithmic context.

## Hard Rules

- Use the convention `←` for assignment and `=` for equality/comparison.
- Prefer PascalCase for algorithm and type names, camelCase for variables.
- Always close blocks explicitly: `END IF`, `END FOR`, `END FUNCTION`, `END CLASS`, etc.
- Type declarations use `DECLARE name AS TYPE` or inferred `name := value`.
- Arrays are zero-indexed by default; document if one-indexed.
- Keep pseudocode language-agnostic; avoid language-specific idioms.
- Reference `assets/pseudocode-reference.md` for exhaustive examples.

## Decision Gates

| Need | Action |
| --- | --- |
| Full syntax lookup or teaching reference | Read `assets/pseudocode-reference.md` |
| Quick algorithm sketch | Use SKILL.md conventions + minimal syntax |
| Translate pseudocode to code | Ask target language, then map constructs 1:1 |
| Validate existing pseudocode | Check block closings, assignment vs equality, types |
| User asks for a specific construct | Reference the numbered section in assets |

## Execution Steps

1. Confirm scope: reading, writing, translating, or teaching pseudocode.
2. If writing: identify inputs, outputs, control flow, and data structures needed.
3. If translating: map each pseudocode construct to the target language equivalent.
4. If teaching: reference the numbered sections in `assets/pseudocode-reference.md`.
5. Validate: ensure all blocks are closed, assignments use `←`, comparisons use `=`.

## Output Contract

Return:
- The pseudocode block or translation produced;
- Any assumptions about indexing, types, or conventions used;
- Pointer to relevant sections in `assets/pseudocode-reference.md` if applicable.

## References

- `assets/pseudocode-reference.md` — comprehensive examples (99 topics).
