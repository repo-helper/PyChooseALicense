#!/bin/bash
root_dir=$(git rev-parse --show-toplevel)
tmp_dir=$(mktemp -d -t pychoosealicense-XXXXXXXXXX)
cd
git clone https://github.com/github/choosealicense.com "$tmp_dir"
cp -r "$tmp_dir/_licenses" "$root_dir/pychoosealicense/" --verbose
cp "$tmp_dir/_data/rules.yml" "$root_dir/pychoosealicense/rules/rules.yml" --verbose

cat << EOF > "$root_dir/pychoosealicense/_licenses/__init__.py"
"""
License metadata used by \`\`pychoosealicense\`\`.
"""

CHOOSEALICENSE_COMMIT_INFO = """
$(git -C "$tmp_dir" log -1)
"""

CHOOSEALICENSE_COMMIT_HASH = "$(git -C "$tmp_dir" show --format="%H" --no-patch)"
CHOOSEALICENSE_COMMIT_SHORTHASH = "$(git -C "$tmp_dir" show --format="%h" --no-patch)"
EOF

rm -rf "$tmp_dir"
