gh run download --repo smeriwether/blog --name blog $(gh run list --repo smeriwether/blog --limit 1 --json databaseId --jq '.[0].databaseId')

. .venv/bin/activate

pip install blog-1.0.0-py2.py3-none-any.whl --force-reinstall

pip install waitress

kill -9 $(pgrep waitress)

waitress-serve --call 'blog:create_app' &

