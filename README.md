# CJTF

Website of the Central Jersey Transportation Forum, at <https://centraljerseytf.org>.

Django settings are contained in config/settings.py. This file is excluded from source control, as it contains secrets. In production, it is created by Ansible (see <https://github.com/dvrpc/cloud-ansible/tree/main/roles/cjtf>).

## Development

Features, enhancements, bugs, questions, and similar are tracked in [issues](https://github.com/dvrpc/cjtf/issues). These are then distilled into [milestones](https://github.com/dvrpc/cjtf/milestones).

To run the website locally:

  1. Clone this repo.
  2. An example Django configuration file is provided at config/settings.py.example. Create a copy of this and rename it as settings.py.
  3. Create a Postgresql user named "cjtf_dev" with the password "cjtf_dev", and a corresponding database named "cjtf_dev". (This is what the example settings file is configured to use, but of course can be changed.) (Postgres is required - the code will not work with other types of databases as is.)
  4. Create a directory for Django to store database migrations, at web/migrations. (Migrations are not included in source control.)
  5. Create and activate a Python virtual environment with dependencies installed:
  ```shell
  python3 -m venv ve
  . ve/bin/activate  # for Bash shell. Other shells available too, e.g. ve/bin/activate.fish
  pip install -r requirements.txt
  ```
  6. Create the tables in the database with Django's migration tool:
  ```shell
  python manage.py makemigrations
  python manage.py makemigrations web
  python manage.py migrate
  ```
  7. Run the development server with `python manage.py runserver`

The site will be available at <http://127.0.0.1:8000/> and the admin site at <http://127.0.0.1:8000/admin>. See <https://docs.djangoproject.com/en/3.2/ref/contrib/admin/> for using the Django admin site.

