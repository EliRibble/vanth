PROJECT=vanth
SCRIPTS="bin/vanth"
mkdir -p dist
if [ -z "$1" ]; then
    FILES="conftest.py setup.py $(find $PROJECT -maxdepth 3 -name "*.py" -not -path "*alembic/*" -print) $SCRIPTS $(find tests -maxdepth 3 -name "*.py" -print)"
else
    FILES="$1"
    echo "linting $FILES"
fi
pylint $FILES --reports=no | tee dist/pylint.log
