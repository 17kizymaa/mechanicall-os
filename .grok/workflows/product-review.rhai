let meta = #{
    name: "product-review",
    description: "Parallel read-only Grok reviews to redefine the product; one REVIEW; never approve",
    when_to_use: "Redefine Mechanicall from simultaneous reviews, not multiple Nexts",
    phases: [
        #{ title: "Review", detail: "eight read-only dimensions" },
        #{ title: "Synthesize", detail: "one REVIEW.md; no CURRENT write" },
    ],
};

let dim_schema = #{
    "type": "object", "required": ["dimension", "score", "verdict", "evidence"],
    "properties": #{
        "dimension": #{ "type": "string" },
        "score": #{ "type": "integer" },
        "verdict": #{ "type": "string" },
        "evidence": #{ "type": "string" },
    },
};

let syn_schema = #{
    "type": "object", "required": ["summary", "score_total", "one_sentence"],
    "properties": #{
        "summary": #{ "type": "string" },
        "score_total": #{ "type": "integer" },
        "one_sentence": #{ "type": "string" },
    },
};

let dimensions = [
    "local-AI structured support",
    "selected directory",
    "chat-app framework",
    "workspace bridge",
    "protocol law CURRENT Yes silence",
    "ICM factory vs Rooms",
    "distribution honesty APK CLI Play Store",
    "skeptic refute that a redesign is needed",
];

phase("Review");
let jobs = [];
let i = 0;
for d in dimensions {
    let p = "";
    p += "You are a read-only reviewer for Mechanicall OS. Do not edit files. ";
    p += "Do not run aether approve, reject, or next. Opening is not Yes. ";
    p += "Use read_file and grep. Read CURRENT.md, PRODUCT.md, ";
    p += "dev/31_sequential-walk/04_gate-client/output/STORM.md, ";
    p += "dev/32_phase-close-agent-ci/01_phase-review/output/PHASE-REVIEW.md. ";
    p += "Score ONLY this dimension 0-5 with file evidence: ";
    p += d;
    p += " Empty score is invalid unless you read those files and still have no evidence.";
    jobs.push(#{
        prompt: p,
        label: "rev-" + i.to_string(),
        capability_mode: "read-only",
        agent_type: "explore",
        output_schema: dim_schema,
    });
    i += 1;
}
let results = parallel(jobs);

let packed = "";
let n_ok = 0;
for r in results {
    if r != () && r.success && r.output != () && r.output.verdict != () {
        n_ok += 1;
        packed += r.output.dimension + " | " + r.output.score.to_string() + " | " + r.output.verdict + " | " + r.output.evidence + "\n";
    }
}
log(n_ok.to_string() + "/" + dimensions.len().to_string() + " reviewers returned evidence");
if n_ok == 0 {
    complete(#{ summary: "No reviewer evidence. Fail closed. Not Yes.", score_total: 0, one_sentence: "Swarm produced no evidence." });
}

phase("Synthesize");
let sp = "";
sp += "Synthesize these read-only reviews into one product conclusion. ";
sp += "Do not edit CURRENT.md. Do not approve. ";
sp += "Command: write one paragraph plus score_total (sum of dimension scores if present). ";
sp += "Reviews:\n";
sp += packed;
let syn = agent(sp, #{
    label: "synthesize",
    capability_mode: "read-only",
    output_schema: syn_schema,
});

let report = "No synthesis.";
let total = 0;
let sentence = "Swarm did not synthesize.";
if syn.success && syn.output != () {
    if syn.output.summary != () { report = syn.output.summary; }
    if syn.output.score_total != () { total = syn.output.score_total; }
    if syn.output.one_sentence != () { sentence = syn.output.one_sentence; }
}
let path = write_scratch_file("REVIEW.md", report + "\n\n" + sentence + "\n");
complete(#{
    path: path,
    summary: report,
    score_total: total,
    one_sentence: sentence,
    reviewers_ok: n_ok,
});
