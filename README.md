# CJTF

Website of the Central Jersey Transportation Forum, at <https://centraljerseytf.org>.

## Development

Features, enhancements, bugs, questions, and similar are tracked in [issues](https://github.com/dvrpc/cjtf/issues). These are then distilled into [milestones](https://github.com/dvrpc/cjtf/milestones).

To run the website locally, create and activate a python virtual environment with the dependencies installed:

```bash
python3 -m venv ve
. ve/bin/activate
pip install -r requirements.txt
```

Then run Django's development server:

```bash
python manage.py runserver
```
