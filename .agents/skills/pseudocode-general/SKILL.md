---
name: pseudocode-general
description: "Trigger: pseudocode-general, high-level flow, code overview, step-by-step description, program outline, code sketch. Describe complete code behavior in language-agnostic, high-level steps."
license: Apache-2.0
metadata:
  author: gentleman-programming
  version: "1.0"
---

## Activation Contract

Use this skill when:
- a user asks for a high-level overview of what code does;
- a program flow needs to be described without language-specific syntax;
- documenting a pipeline, workflow, or sequence of operations;
- drafting a prompt that describes desired code behavior;
- summarizing complex code into readable steps.

Do not use for:
- detailed algorithm design with exact control flow (use `pseudocode-specific`);
- teaching pseudocode syntax and conventions (use `pseudocode-specific`);
- production code in a specific language (use language-specific skills).

## Hard Rules

- Describe each step as a single imperative statement: `VERB noun (details)`.
- Use UPPERCASE for action verbs: IMPORT, LOAD, SEND, FILTER, TRANSFORM, SAVE, PLOT, etc.
- Parameters go in parentheses: `(sample rate 4096, channels 2)`.
- Variables use `name = ACTION (...)` when a step produces a value.
- Keep steps sequential; add arrows `→` only for parallel or branching flows.
- Omit language-specific syntax: no semicolons, braces, type annotations, or imports.
- One step per line. Group related steps under a label if needed.

## Decision Gates

| Need | Action |
| --- | --- |
| Quick code overview | Use this skill: high-level steps, no syntax |
| Detailed algorithm with loops/conditions | Use `pseudocode-specific` instead |
| Describing a prompt or spec for code | Use this skill: describe intent, not implementation |
| Teaching actual pseudocode syntax | Use `pseudocode-specific` |

## Execution Steps

1. Identify the overall goal of the code or flow.
2. Break it into discrete steps: input → process → output.
3. For each step, write one line: `ACTION noun (parameters)`.
4. When a step produces a value, use `name = ACTION (...)`.
5. Optionally label sections: `## Input`, `## Processing`, `## Output`.

## Output Contract

Return:
- A numbered or bulleted list of high-level steps;
- Each step is a single line describing one operation;
- Variables introduced are named clearly but language-agnostic.

## Examples

**Data pipeline:**
```
1. IMPORT LIBRARIES (pandas, numpy, matplotlib)
2. data = LOAD CSV (path="data/sales.csv")
3. FILTER rows WHERE (amount > 1000)
4. AGGREGATE BY (region) → compute (mean, std)
5. PLOT bar chart (x=region, y=mean)
6. SAVE figure ("output/region_stats.png")
```

**IQ signal flow:**
```
1. IMPORT LIBRARIES (json, cv2, numpy)
2. iq = GENERATE DUMMY DATA IQ (sample rate 4096, length 1024)
3. req = REQUEST DATA SERVER (https://example.com/api)
4. req.send(iq)
5. response = RECEIVE RESPONSE (json)
6. PLOT time domain (iq, title="Raw IQ")
```

**Image processing:**
```
1. IMPORT LIBRARIES (cv2, numpy)
2. img = LOAD IMAGE ("input/photo.jpg")
3. gray = CONVERT color space (img → grayscale)
4. edges = APPLY CANNY (gray, low=100, high=200)
5. SAVE result ("output/edges.png")
```

## References

- `pseudocode-specific` — for detailed algorithm design with exact control flow syntax.
