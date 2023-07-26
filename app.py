from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'


def create_table():
    connection = sqlite3.connect('notes.db')
    cursor = connection.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS notes
                      (id INTEGER PRIMARY KEY AUTOINCREMENT,
                      title TEXT NOT NULL,
                      content TEXT NOT NULL)''')
    connection.commit()
    connection.close()


def get_notes():
    connection = sqlite3.connect('notes.db')
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM notes")
    notes = cursor.fetchall()
    connection.close()
    return notes


def add_note(title, content):
    connection = sqlite3.connect('notes.db')
    cursor = connection.cursor()
    cursor.execute("INSERT INTO notes (title, content) VALUES (?, ?)", (title, content))
    connection.commit()
    connection.close()


def update_note_in_db(note_id, title, content):
    connection = sqlite3.connect('notes.db')
    cursor = connection.cursor()
    cursor.execute("UPDATE notes SET title=?, content=? WHERE id=?", (title, content, note_id))
    connection.commit()
    connection.close()


def get_note_by_id(note_id):
    connection = sqlite3.connect('notes.db')
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM notes WHERE id=?", (note_id,))
    note = cursor.fetchone()
    connection.close()
    return note


def delete_note_by_id(note_id):
    connection = sqlite3.connect('notes.db')
    cursor = connection.cursor()
    cursor.execute("DELETE FROM notes WHERE id=?", (note_id,))
    connection.commit()
    connection.close()


@app.route('/')
def index():
    notes = get_notes()
    return render_template('index.html', notes=notes)


@app.route('/create', methods=['GET', 'POST'])
def create_note():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        add_note(title, content)
        return redirect(url_for('index'))
    return render_template('create_note.html')


@app.route('/note/<int:note_id>', methods=['GET', 'POST'])
def view_note(note_id):
    note = get_note_by_id(note_id)
    if request.method == 'POST':
        delete_note_by_id(note_id)
        return redirect(url_for('index'))
    return render_template('view_note.html', note=note)


@app.route('/edit/<int:note_id>', methods=['GET', 'POST'])
def edit_note(note_id):
    note = get_note_by_id(note_id)
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        update_note_in_db(note_id, title, content)
        return redirect(url_for('view_note', note_id=note_id))
    return render_template('edit_note.html', note=note)


@app.route('/delete/<int:note_id>', methods=['GET', 'POST'])
def delete_note(note_id):
    if request.method == 'POST' or request.method == 'GET':
        delete_note_by_id(note_id)
        return redirect(url_for('index'))
    return redirect(url_for('index'))


@app.route('/update/<int:note_id>', methods=['POST'])
def update_note(note_id):
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        update_note_in_db(note_id, title, content)
        return redirect(url_for('view_note', note_id=note_id))
    return redirect(url_for('index'))


if __name__ == '__main__':
    create_table()
    app.run(debug=True)
