#!/usr/bin/env bash
set -euo pipefail

# Minimum seconds between fetches of the same checkout.
update_interval=300

repo_input=""
force_update=0

while [[ $# -gt 0 ]]; do
	case "$1" in
	--force-update)
		force_update=1
		;;
	-*)
		echo "error: unknown option: $1" >&2
		exit 2
		;;
	*)
		if [[ -n "$repo_input" ]]; then
			echo "error: unexpected argument: $1" >&2
			exit 2
		fi
		repo_input="$1"
		;;
	esac
	shift
done

if [[ -z "$repo_input" ]]; then
	echo "usage: checkout.sh <repo> [--force-update]" >&2
	exit 2
fi

trim_repo_input() {
	local s="$1"
	# Trim leading/trailing whitespace.
	s="${s#"${s%%[![:space:]]*}"}"
	s="${s%"${s##*[![:space:]]}"}"
	printf '%s' "$s"
}

# Sets host, org and repo from a repository reference.
parse_repo() {
	local input rest first path parts
	input="$(trim_repo_input "$1")"

	# Strip query/fragment for URL-like inputs.
	input="${input%%\?*}"
	input="${input%%#*}"

	# Scheme-ful forms first: a port in an ssh URL also looks scp-like.
	case "$input" in
	ssh://* | http://* | https://*)
		rest="${input#*://}"
		host="${rest%%/*}"
		path="${rest#*/}"
		;;
	*@*:*)
		host="${input%%:*}"
		path="${input#*:}"
		;;
	*/*)
		first="${input%%/*}"
		if [[ "$first" == *.* || "$first" == localhost ]]; then
			host="$first"
			path="${input#*/}"
		else
			host="github.com"
			path="$input"
		fi
		;;
	*)
		echo "error: unsupported repository format: $input" >&2
		return 1
		;;
	esac

	host="${host#*@}"
	path="${path#/}"
	path="${path%/}"

	# For GitHub-like deep links, use owner/repo only.
	IFS='/' read -r -a parts <<<"$path"
	if [[ ${#parts[@]} -ge 3 ]]; then
		case "${parts[2]}" in
		tree | blob | pull | issues | commit | actions | releases | compare | wiki)
			path="${parts[0]}/${parts[1]}"
			;;
		esac
	fi

	# Strip optional .git suffix.
	path="${path%.git}"

	if [[ "$path" != */* ]]; then
		echo "error: repository path must contain at least org/repo: $path" >&2
		return 1
	fi

	repo="${path##*/}"
	org="${path%/*}"

	if [[ -z "$host" || -z "$org" || -z "$repo" ]]; then
		echo "error: failed to parse repository: $input" >&2
		return 1
	fi
}

parse_repo "$repo_input" || exit 1

checkout_path="$HOME/.cache/checkouts/$host/$org/$repo"
origin_url="https://$host/$org/$repo.git"

if [[ ! -d "$checkout_path/.git" ]]; then
	git clone --filter=blob:none "$origin_url" "$checkout_path" >/dev/null
fi

last_fetch_file="$checkout_path/.git/librarian-last-fetch"
now_epoch="${EPOCHSECONDS:-$(date +%s)}"
needs_update=1

if ((force_update == 0)); then
	last_epoch=0
	# stderr is redirected first: a missing ledger must not report the failed read.
	read -r last_epoch 2>/dev/null <"$last_fetch_file" || last_epoch=0
	if [[ "$last_epoch" =~ ^[0-9]+$ ]] && ((now_epoch - last_epoch < update_interval)); then
		needs_update=0
	fi
fi

if ((needs_update == 1)); then
	# Normalize the remote to the canonical HTTPS URL. set-url fails when there
	# is no origin, which happens for a checkout this script did not create.
	if ! git -C "$checkout_path" remote set-url origin "$origin_url" 2>/dev/null; then
		git -C "$checkout_path" remote add origin "$origin_url"
	fi

	git -C "$checkout_path" fetch --prune --tags origin >/dev/null
	echo "$now_epoch" >"$last_fetch_file"

	# Only ever fast-forward: the cache is shared, so local state is never
	# discarded. Warn instead, since the caller is about to read stale source.
	upstream="$(git -C "$checkout_path" rev-parse --abbrev-ref --symbolic-full-name '@{u}' 2>/dev/null || true)"
	if [[ -n "$upstream" && -z "$(git -C "$checkout_path" status --porcelain --untracked-files=no)" ]]; then
		git -C "$checkout_path" merge --ff-only "$upstream" >/dev/null 2>&1 ||
			echo "warning: origin diverged, left at the current commit: $checkout_path" >&2
	else
		echo "warning: modified or has no upstream, not updated: $checkout_path" >&2
	fi
fi

printf '%s\n' "$checkout_path"
