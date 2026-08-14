from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)


def criar_banco():
    conexao = sqlite3.connect("biblioteca.db")
    cursor = conexao.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS livros (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            autor TEXT NOT NULL
        )
    """)

    conexao.commit()
    conexao.close()


@app.route("/")
def inicio():
    conexao = sqlite3.connect("biblioteca.db")
    cursor = conexao.cursor()

    cursor.execute("SELECT * FROM livros")
    livros = cursor.fetchall()

    conexao.close()

    return render_template("index.html", livros=livros)

@app.route("/cadastrar", methods=["POST"])
def cadastrar():
    titulo = request.form["titulo"]
    autor = request.form["autor"]

    conexao = sqlite3.connect("biblioteca.db")
    cursor = conexao.cursor()

    cursor.execute(
        "INSERT INTO livros (titulo, autor) VALUES (?, ?)",
        (titulo, autor)
    )

    conexao.commit()
    conexao.close()

    return redirect("/")


if __name__ == "__main__":
    criar_banco()
    app.run(debug=True)