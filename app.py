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


    cursor = conexao.cursor()

    busca = request.args.get("busca", "").strip()

    if busca:
        cursor.execute(
            """
            SELECT * FROM livros
            WHERE titulo ILIKE %s OR autor ILIKE %s
            ORDER BY id ASC
            """,
            (f"%{busca}%", f"%{busca}%")
        )
    else:
        cursor.execute("SELECT * FROM livros ORDER BY id ASC")

    livros = cursor.fetchall()

    conexao.close()

    return render_template("index.html", livros=livros, busca=busca)


    conexao.close()

    return render_template("index.html", livros=livros, busca=busca)

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

@app.route("/excluir/<int:id>", methods=["POST"])
def excluir(id):
    conexao = psycopg2.connect(
        host="localhost",
        database="biblioteca",
        user="postgres",
        password=os.environ["DB_PASSWORD"],
        port="5432"
    )

    cursor = conexao.cursor()

    cursor.execute(
        "DELETE FROM livros WHERE id = %s",
        (id,)
    )

    conexao.commit()
    conexao.close()

    return redirect("/")

@app.route("/editar/<int:id>")
def editar(id):
    conexao = psycopg2.connect(
        host="localhost",
        database="biblioteca",
        user="postgres",
        password=os.environ["DB_PASSWORD"],
        port="5432"
    )

    cursor = conexao.cursor()

    cursor.execute(
        "SELECT * FROM livros WHERE id = %s",
        (id,)
    )

    livro = cursor.fetchone()

    conexao.close()

    if livro is None:
        return redirect("/")

    return render_template("editar.html", livro=livro)


@app.route("/atualizar/<int:id>", methods=["POST"])
def atualizar(id):
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
        "UPDATE livros SET titulo = %s, autor = %s WHERE id = %s",
        (titulo, autor, id)
    )

    conexao.commit()
    conexao.close()

    return redirect("/")
    
if __name__ == "__main__":
    criar_banco()
    app.run(debug=True)
