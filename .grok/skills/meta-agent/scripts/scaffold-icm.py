#!/usr/bin/env python3
"""
ICM Workspace / Stages Scaffolder (meta-agent behaviour)
Creates a minimal numbered-stage folder structure + CONTEXT.md templates
following Interpretable Context Methodology (arXiv:2603.16021).

Usage:
  python .grok/skills/meta-agent/scripts/scaffold-icm.py my-task "Short description"
  # Creates ./my-task/ with 01_*/02_*/... and root CONTEXT.md

Or run from anywhere and give target dir:
  python .../scaffold-icm.py /path/to/task-dir "Description of the work"
"""

import sys
import os
from datetime import datetime

STAGE_TEMPLATES = [
    ("01_analyze", "Analyze / Research", "Gather facts, requirements, existing code, context. Produce structured analysis."),
    ("02_plan", "Plan / Design", "Create concrete plan, architecture sketch, file list, acceptance criteria."),
    ("03_implement", "Implement", "Write or modify code, scripts, docs. Use Python behaviours for mechanical steps."),
    ("04_verify", "Verify / Test", "Run tests, lint, manual checks. Fix issues. Produce verification report."),
    ("05_review", "Review & Polish", "Human-aligned final pass: clarity, style, docs, edge cases. Prepare deliverables."),
]

CONTEXT_MD_TEMPLATE = """## Inputs
- Layer 4 (working): {prev_output}
- Layer 3 (reference): ../../references/coding-style.md   # (create if missing; or link to project rules)
- Layer 3 (reference): ../../CORE_PRINCIPLES.md
- Layer 1: ../CONTEXT.md

## Process
You are the **{role}** stage.

Follow the Meta-Agent skill (this workspace's .grok/skills/meta-agent/SKILL.md) and all Layer 3 references.

{description}

- Load *only* the inputs listed above.
- Prefer calling Python behaviours (scripts/) for any non-intelligent work.
- Write clear, self-contained artifacts.
- Place all deliverables under this stage's `output/`.
- Stop after writing output for human review.

## Outputs
- {primary_artifact} -> output/
- summary.md -> output/
- (any other files the next stage or user will need)
"""

ROOT_CONTEXT = """# ICM Task Context (Layer 1 Routing)

This folder follows the Interpretable Context Methodology (arXiv:2603.16021).

Folder structure = the agent architecture.
Markdown files = skills, contracts, context.
Python = behaviours.
Single agent (Grok) orchestrates by reading the structure.

## Pipeline
{stages}

## How to run
1. Review / edit anything in 01_analyze/output/ after it completes.
2. Tell the agent "proceed to 02" (or the next stage) after review.
3. Human edits at output/ gates are the primary way to steer.

References (Layer 3) live in `references/` (create shared ones at top level or in project root).
Working outputs live in each stage's `output/`.

See .grok/skills/meta-agent/SKILL.md for the full protocol.
"""

STAGE_README = """This is stage {num} ({name}).

See CONTEXT.md for the exact contract.
Write outputs to ./output/
"""

def mkdir_p(path):
    os.makedirs(path, exist_ok=True)

def write_file(path, content):
    with open(path, "w") as f:
        f.write(content)
    print(f"  wrote {path}")

def main():
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)

    target = sys.argv[1]
    desc = " ".join(sys.argv[2:]) or "Development task"

    base = os.path.abspath(target)
    name = os.path.basename(base.rstrip("/"))

    print(f"Scaffolding ICM workspace for '{name}' at {base}")
    mkdir_p(base)

    # Root routing file
    stage_list = "\n".join(f"- {s[0]}: {s[1]}" for s in STAGE_TEMPLATES)
    write_file(os.path.join(base, "CONTEXT.md"), ROOT_CONTEXT.format(stages=stage_list))

    # Optional references dir
    refs = os.path.join(base, "references")
    mkdir_p(refs)
    write_file(os.path.join(refs, "README.md"), "# Layer 3 Reference Material\n\nAdd shared conventions, style, domain rules here.\n")

    prev = "user-provided input or ../00_init/output/ (adjust as needed)"
    for idx, (folder, role, description) in enumerate(STAGE_TEMPLATES):
        stage_dir = os.path.join(base, folder)
        mkdir_p(stage_dir)
        mkdir_p(os.path.join(stage_dir, "output"))
        mkdir_p(os.path.join(stage_dir, "references"))  # stage local refs if needed

        prev_out = prev if idx == 0 else f"../{STAGE_TEMPLATES[idx-1][0]}/output/"
        primary = "analysis.md" if "analyze" in folder else \
                  "plan.md" if "plan" in folder else \
                  "implementation.md" if "implement" in folder else \
                  "verification.md" if "verify" in folder else "final.md"

        ctx = CONTEXT_MD_TEMPLATE.format(
            prev_output=prev_out,
            role=role,
            description=description,
            primary_artifact=primary
        )
        write_file(os.path.join(stage_dir, "CONTEXT.md"), ctx)
        write_file(os.path.join(stage_dir, "README.md"), STAGE_README.format(num=folder[:2], name=role))

        prev = f"../{folder}/output/"

    # Tiny helper note
    write_file(os.path.join(base, "README.md"), f"""# {name}

ICM workspace created {datetime.now().isoformat(timespec='seconds')}

Description: {desc}

See CONTEXT.md and each stage's CONTEXT.md.
Run the meta-agent skill (/meta-agent) and point it at this folder.

Stages are sequential with review gates at each output/ directory.
""")

    print("\nDone. Next steps:")
    print(f"  cd {base}")
    print("  # Tell your agent: start the 01_analyze stage for this ICM task")
    print("  # Review files in 01_analyze/output/ then say 'proceed to 02_plan'")

if __name__ == "__main__":
    main()
