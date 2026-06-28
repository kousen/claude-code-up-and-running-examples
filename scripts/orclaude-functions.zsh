# Source this file from zsh after putting scripts/orclaude on your PATH.
#
# Example:
#   source /path/to/claude-code-up-and-running-examples/scripts/orclaude-functions.zsh

orglm() {
  orclaude z-ai/glm-5.2 "$@"
}

orkimi() {
  orclaude moonshotai/kimi-k2.7-code "$@"
}
