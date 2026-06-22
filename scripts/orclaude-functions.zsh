# Source this file from zsh after putting scripts/orclaude on your PATH.
#
# Example:
#   source /path/to/claude-code-up-and-running/scripts/orclaude-functions.zsh

orglm() {
  orclaude glm "$@"
}

orkimi() {
  orclaude kimi "$@"
}
