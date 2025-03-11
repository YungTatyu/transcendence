#! /bin/bash

readonly PYTHON="py"
readonly JS="js"

lint() {
  local option="$1"
  if [[ ${option} != ${PYTHON} ]]; then
    biome lint --write --error-on-warnings
  fi
  if [[ ${option} != ${JS} ]]; then
    ruff check --fix
  fi
  return 0
}

fmt() {
  local option="$1"
  if [[ ${option} != ${PYTHON} ]]; then
    biome format --write --error-on-warnings
  fi
  if [[ ${option} != ${JS} ]]; then
    ruff format
  fi
  return 0
}

main() {
  local cmd="$1"
  local option="$2"
  if [[ ${cmd} == "lint" ]]; then
    lint ${option}
    return 0
  fi
  if [[ ${cmd} == "fmt" ]]; then
    fmt ${option}
    return 0
  fi

  # jsのlinterとformatterを実行
  biome check --error-on-warnings || return 1

  # puthonのlinterとformatterを実行
  ruff check || return 1
  ruff format --diff || return 1
  return 0
}

main "$@"
