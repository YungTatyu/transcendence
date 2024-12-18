#! /bin/bash

main() {
  ruff check || return 1
  ruff format --diff || return 1
  return 0
}

main "$@"
