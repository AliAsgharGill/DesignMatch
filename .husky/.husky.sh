# .husky/.husky.sh
if [ -z "$husky_skip_init" ]; then
  debug() {
    [ "$HUSKY_DEBUG" = "1" ] && echo "husky: $1"
  }

  readonly hook_name="$(basename "$0")"
  debug "starting $hook_name hook"
  if [ "$HUSKY" = "0" ]; then
    debug "HUSKY env variable is set to 0, skipping hook"
    exit 0
  fi

  if ! command -v dirname >/dev/null; then
    echo "husky: dirname command not found in PATH"
    exit 127
  fi

  ...
fi
