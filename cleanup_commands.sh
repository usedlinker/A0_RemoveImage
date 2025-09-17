
#!/bin/bash
# cleanup_commands.sh - run locally in your repo clone
# WARNING: do NOT run these on a shared repo without understanding --force pushes.
# 1) Replace leaked string in all files (edit LEAKED_STRING variable first)
LEAKED_STRING="R9YTB01G4ZV"
if [ "$LEAKED_STRING" = "" ]; then
  echo "Set LEAKED_STRING inside this script before running."
  exit 1
fi

# Find occurrences (preview)
grep -nR "$LEAKED_STRING" || true

# Replace occurrences in all files (preview then commit)
# WARNING: this will modify files in-place
git grep -l "$LEAKED_STRING" | xargs -r sed -i "s/$LEAKED_STRING/REDACTED_BY_OWNER/g"

# Commit changes
git add -A
git commit -m "Sanitize leaked secret occurrences"

# For full history removal, use BFG (recommended)
echo "To remove from git history, use BFG repo-cleaner:"
echo "1) Install BFG: https://rtyley.github.io/bfg-repo-cleaner/"
echo "2) Create leak-words.txt with the leaked string on one line"
echo "3) Run: bfg --replace-text leak-words.txt --no-blob-protection"
echo "4) Then run: git reflog expire --expire=now --all && git gc --prune=now --aggressive && git push --force"
