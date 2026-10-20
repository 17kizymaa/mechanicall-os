let meta = #{
    name: "actual-app-verification",
    description: "Score the demo sit against BEHAVIOURS.md; parallel read-only reviewers; never approve",
    when_to_use: "ACTUAL-APP-VERIFICATION, app reviewer, behaviour score",
    phases: [
        #{ title: "Score", detail: "one agent runs python/app_verify.py" },
        #{ title: "Review", detail: "one read-only reviewer per behaviour" },
        #{ title: "Synthesize", detail: "one VERIFICATION; no CURRENT write" },
    ],
};

let row_schema = #{
    "type": "object",
    "required": ["id", "verdict", "evidence"],
    "properties": #{
        "id": #{ "type": "string" },
        "verdict": #{ "type": "string" },
        "evidence": #{ "type": "string" },
    },
};

let syn_schema = #{
    "type": "object",
    "required": ["summary", "failed", "next_gap"],
    "properties": #{
        "summary": #{ "type": "string" },
        "failed": #{ "type": "string" },
        "next_gap": #{ "type": "string" },
    },
};

phase("Score");
let score_p = "";
score_p += "Run: python3 python/app_verify.py from the mechanicall-os repo root. ";
score_p += "Read the printed table. Do not tap Confirm. Do not aether approve. ";
score_p += "Do not edit CURRENT.md. Return the ten ids with PASS/FAIL copied from the script.";
let scored = agent(score_p, #{
    label: "mechanical-score",
    capability_mode: "execute",
    agent_type: "general-purpose",
});

phase("Review");
let team = [
    #{ id: "approve-log", file: ".grok/personas/approve-log.toml" },
    #{ id: "reject-log", file: ".grok/personas/reject-log.toml" },
    #{ id: "preflight-log", file: ".grok/personas/preflight-log.toml" },
    #{ id: "next-selected-log", file: ".grok/personas/next-selected-log.toml" },
    #{ id: "before-current", file: ".grok/personas/before-current.toml" },
    #{ id: "decisions-log", file: ".grok/personas/decisions-log.toml" },
    #{ id: "proposals-log", file: ".grok/personas/proposals-log.toml" },
];
let jobs = [];
for member in team {
    let p = "";
    p += "You are the sidecar persona in the app-review loop. Read-only. ";
    p += "Never edit files. Never aether approve. Never tap Confirm. Never train. ";
    p += "Working directory is the mechanicall-os repo. ";
    p += "Read " + member.file + " and the instructions_file it names. Speak only from those rows. ";
    p += "Read dev/36_actual-app-verification/01_contract/output/BEHAVIOURS.md. ";
    p += "Comment on the mechanical score for this sit. Quote one row from your file. ";
    p += "id must be " + member.id + ". ";
    p += "verdict is PASS if your rows agree with the score, FAIL if a row contradicts it, SUGGEST if you only have a quote. ";
    p += "evidence is the quote plus the behaviour id it touches. Empty verdict is invalid.";
    jobs.push(#{
        prompt: p,
        label: member.id,
        capability_mode: "read-only",
        agent_type: "explore",
        output_schema: row_schema,
    });
}
let results = parallel(jobs);

let packed = "";
let n_ok = 0;
for r in results {
    if r != () && r.success && r.output != () && r.output.verdict != () {
        n_ok += 1;
        packed += r.output.id + " | " + r.output.verdict + " | " + r.output.evidence + "\n";
    }
}
log(n_ok.to_string() + "/7 sidecar reviewers returned evidence");

phase("Synthesize");
let sp = "";
sp += "Synthesize mechanical score plus these reviewer rows into one conclusion. ";
sp += "Do not rewrite CURRENT. Do not approve. The sidecar rows are suggestions. ";
sp += "A SUGGEST verdict is not a mechanical FAIL. Fail closed only if the score phase failed B3 or B4. ";
sp += "Rows:\n";
sp += packed;
sp += "\nName the single biggest gap (manual plan edit vs draft-as-chat).";
let syn = agent(sp, #{
    label: "synthesize",
    capability_mode: "read-only",
    output_schema: syn_schema,
});
if syn.success && syn.output != () {
    complete(syn.output);
}
complete(#{
    summary: "Reviewers incomplete. Fail closed. Not Yes.",
    failed: "unknown",
    next_gap: "Re-run /actual-app-verification",
});
