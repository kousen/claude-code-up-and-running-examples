export function register(on) {
  // The matcher limits this hook to Bash, so e.command is the shell command
  on('tool.call', { tool: 'Bash' }, async ($, e, next) => {
    if (/git push .*(--force|-f)\b/.test(e.command)) {
      // Returning without next() answers the event; the command never runs
      return { deny: 'No force pushes here. Push to a new branch instead.' }
    }
    return next(e)
  })
}
