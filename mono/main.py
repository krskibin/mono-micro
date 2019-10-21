from mono import app, db
from mono.models import User, Task


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Task': Task}


@app.cli.command('create_db')
def create_db():
    db.drop_all()
    db.create_all()
    db.session.commit()


@app.cli.command('seed_db')
def seed_db():
    user = User(
        username="admin",
        email="admin@admin.pl"
    )
    user.set_password('admin')
    db.session.add(user)
    db.session.commit()

    task = Task(
        header="Hello",
        body="Task body",
        is_done=False,
        author=user
    )

    db.session.add(task)
    db.session.commit()
