from flask import Flask, render_template, request, redirect
import os
import psycopg2

app = Flask(__name__)


def criar_banco():
    conexao = psycopg2.connect(
        host="localhost",
        database="biblioteca",
        user="postgres",
        password=os.environ["DB_PASSWORD"],
        port="5432"
    )

    cursor = conexao.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS livros (
            id SERIAL PRIMARY KEY,
            titulo TEXT NOT NULL,
            autor TEXT NOT NULL
        )
    """)

    conexao.commit()
    conexao.close()


@app.route("/")
def inicio():
    conexao = psycopg2.connect(
        host="localhost",
        database="biblioteca",
        user="postgres",
        password=os.environ["DB_PASSWORD"],
        port="5432"
    )

    cursor = conexao.cursor()

    cursor.execute("SELECT * FROM livros")
    livros = cursor.fetchall()

    conexao.close()

    return render_template("index.html", livros=livros)

@app.route("/cadastrar", methods=["POST"])
def cadastrar():
    titulo = request.form["titulo"]
    autor = request.form["autor"]

    conexao = psycopg2.connect(
        host="localhost",
        database="biblioteca",
        user="postgres",
        password=os.environ["DB_PASSWORD"],
        port="5432"
    )

    cursor = conexao.cursor()

    cursor.execute(
        "INSERT INTO livros (titulo, autor) VALUES (%s, %s)",
        (titulo, autor)
    )

    conexao.commit()
    conexao.close()

    return redirect("/")


if __name__ == "__main__":
    criar_banco()
    app.run(debug=True)