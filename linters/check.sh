#! /bin/bash

main() {
  biome check --error-on-warnings || return 1
  ruff check || return 1
  ruff format --diff || return 1
  return 0
}

main "$@"
