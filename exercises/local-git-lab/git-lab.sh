#!/usr/bin/env bash
set -euo pipefail
# [Implementation 1] [Implementation 2]
case "${1:---help}" in -h|--help) echo "local-git-lab historical stage";; *) mkdir -p lab;; esac
