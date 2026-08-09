# bash completion for aether — source from ~/.bashrc:
#   source /path/to/mechanicall-os/scripts/aether-completion.bash
#
# Verbs are loaded live from `aether verbs` so AETHER_VERBS stays single source.

_aether_complete() {
    local cur verbs
    COMPREPLY=()
    cur="${COMP_WORDS[COMP_CWORD]}"
    if command -v aether >/dev/null 2>&1; then
        verbs="$(aether verbs 2>/dev/null)"
    else
        verbs="init onboard try panel shell app deinit status distill watch repair poke trust current preflight approve reject next demo brief drift probe event artifact seed spark session graph garden rival help version verbs"
    fi
    # shellcheck disable=SC2207
    COMPREPLY=( $(compgen -W "${verbs} --help --version -h -V --no-hooks" -- "$cur") )
    return 0
}

complete -F _aether_complete aether
