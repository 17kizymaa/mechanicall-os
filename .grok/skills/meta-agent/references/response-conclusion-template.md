# Response Conclusion Requirements (Layer 3 Reference - Factory Configuration)

This is stable reference material. Internalize as constraints for every response generated while the meta-agent skill is active.

## Mandatory Rule

**Every response, without exception, must end with a section titled exactly:**

```
Conclusion and Next-Stage Analysis (ICM Layered Review Gate)
```

The text **under this heading must exceed 40 lines** (counting all lines of substantive content in the final rendered response; aim for 45-70 lines for depth and reviewability).

Short or abrupt endings are forbidden. This implements the "human review gate" and "every output is an edit surface" principle.

## Why This Rule Exists (from ICM paper + CORE_PRINCIPLES)

The paper emphasizes that intermediate outputs must be complete, readable artifacts that a human can inspect and edit before the next stage. A weak conclusion leaves the "product" (your thinking + artifacts) without a clear handoff point.

This repo's CORE_PRINCIPLES demand "maximum inspectability" and that infrastructure must not disappear in a way that hides reasoning. A long, structured conclusion makes the agent's state, reasoning layers, and proposed paths fully visible and diffable.

## Required Content Elements (expand each into multiple paragraphs)

1. **Task Restatement in ICM Terms**
   - Explicitly identify which "stage" of the current conversation or task this response addressed.
   - Reference the user's exact query using Layer 0/1 context.

2. **Five-Layer Mapping**
   - Detail what was loaded from Layer 0 (identity files), Layer 1 (routing), Layer 2 (if any stage contracts), Layer 3 (references like this file and CORE_PRINCIPLES), Layer 4 (working files read or created).
   - Explain how context was deliberately scoped.

3. **Principles Reaffirmation**
   - One or two sentences for each of the eight non-negotiable principles, stating how this response embodied it.
   - Explicitly mention folders, markdown skills, Python behaviours, single-agent model, review gates, layered loading, filesystem truth, and factory/product separation.

4. **Filesystem Inspection Summary**
   - List the specific files and directories inspected for this response (use relative paths).
   - Note any sidecars (`.context.md`, `.aether/`, `.memory/`, `.grok/skills/meta-agent/`).
   - Highlight how the structure itself guided the answer (e.g., the presence of AGENTS.md forced the philosophy).

5. **Artifacts Produced or Modified**
   - Describe exactly what was written, edited, or proposed (paths, commands run, scripts).
   - Treat the main answer body as the "working artifact" for this turn.

6. **Philosophical Reflection**
   - Tie the work back to the arXiv:2603.16021 paper.
   - Connect to this repo's Mechanicall OS goals and awareness sidecars.
   - Discuss observability, human control, and why long conclusions improve model performance (scoped context, reviewability).

7. **Next Stage Proposals (as numbered folders)**
   - Propose at least three concrete follow-on directions, each formatted as a potential ICM stage:
     - 02_...
     - 03_...
     - 04_...
   - For each, give a one-sentence purpose, suggested Inputs, and example Outputs.
   - Ask the user which (if any) to activate by creating the folder + CONTEXT.md.

8. **Python Behaviours and Markdown Contracts Suggested**
   - Recommend or reference specific .py files (e.g. scaffold-icm.py) or new ones that could be written.
   - Suggest updates to existing markdown (AGENTS.md, this template, .context.md).

9. **Review Gate Explicit Hand-off**
   - Clearly state: "This concludes the current turn's output. Review and edit any proposed artifacts or the analysis above before instructing the next stage."
   - Invite direct edits to files or "proceed to X" instructions.
   - Remind that the user can reorder folders, change prompts in CONTEXT.md style files, or reject the direction.

10. **Alignment Check and Open Questions**
    - Self-audit against anti-patterns.
    - Surface any tensions with principles.
    - List 2-4 genuine open questions for the user.

## How to Generate the >40 Lines

- Never use filler. Expand each required element with specific references to files read, exact commands, paper concepts ("Layered context loading prevents lost in the middle"), and this workspace's actual structure (aether shell script, .context.md sidecar, the meta-agent skill dir we are editing).
- Quote short passages from loaded files.
- Use bullet lists and sub-bullets liberally.
- End the conclusion by repeating the user's agency: the filesystem + your edits are the control surface.
- Vary the wording across responses while always hitting the required elements and line count.

## Example Starter Block (expand this in every response)

Conclusion and Next-Stage Analysis (ICM Layered Review Gate)

[Start writing here and continue until well over 40 lines...]

The task just performed was a direct modification to the meta-agent skill definition itself...

[Continue with all 10 elements above in full paragraphs.]

## Enforcement

This template is Layer 3 reference material. It is configured once. Every response (the "product") must internalize it.

If a response would naturally be short, the conclusion section must still expand using reflection, proposals, and alignment checks.

Failure to produce >40 lines in the Conclusion section violates the skill contract and the review gate principle.

This file itself is an edit surface. The user may modify this template to tune the required elements or line target.

# End of Layer 3 Response Conclusion Requirements

Keep this file stable. Changes here affect the "factory" for all future responses.
