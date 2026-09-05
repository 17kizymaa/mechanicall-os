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
let ids = [
    "B1-bind-first",
    "B2-plan-readable",
    "B3-plan-manual-edit",
    "B4-draft-is-workshop",
    "B5-propose-not-current",
    "B6-decide-only-yes",
    "B7-gate-instrument",
    "B8-receipt-tomorrow",
    "B9-window-honest",
    "B10-bind-not-repo",
];
let jobs = [];
let i = 0;
for id in ids {
    let p = "";
    p += "Read-only app reviewer. Never edit files. Never aether approve. Never tap Confirm. ";
    p += "Read dev/36_actual-app-verification/01_contract/output/BEHAVIOURS.md. ";
    p += "Score ONLY this id by reading the named source (SitRackView.kt, MainActivity.kt, ";
    p += "aether_pocket.py, AndroidManifest.xml as needed). Do not read SeatNav.kt — it is deleted: ";
    p += id;
    p += " Verdict PASS or FAIL with a file quote. Empty verdict is invalid.";
    jobs.push(#{
        prompt: p,
        label: "beh-" + i.to_string(),
        capability_mode: "read-only",
        agent_type: "explore",
        output_schema: row_schema,
    });
    i += 1;
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
log(n_ok.to_string() + "/10 behaviour reviewers returned evidence");

phase("Synthesize");
let sp = "";
sp += "Synthesize mechanical score plus these reviewer rows into one conclusion. ";
sp += "Do not rewrite CURRENT. Do not approve. Fail closed if B3 or B4 failed. ";
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
