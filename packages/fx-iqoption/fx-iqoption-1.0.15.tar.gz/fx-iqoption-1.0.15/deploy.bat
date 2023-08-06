del /S *.tar.gz
python setup.py sdist
twine upload dist/*
