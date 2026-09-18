from flask import Flask, render_template, request, redirect
from database import conectar

app = Flask(__name__)


@app.route("/")
def inicio():
    return render_template("index.html")


@app.route("/cadastrar", methods=["GET", "POST"])
def cadastrar():

    if request.method == "POST":

        estabelecimento = request.form["estabelecimento"]
        alimento = request.form["alimento"]
        quantidade = request.form["quantidade"]
        validade = request.form["validade"]
        endereco = request.form["endereco"]

        conexao = conectar()
        cursor = conexao.cursor()

        sql = """
        INSERT INTO doacoes
        (
            estabelecimento,
            alimento,
            quantidade,
            validade,
            endereco,
            status
        )
        VALUES (%s, %s, %s, %s, %s, %s)
        """

        valores = (
            estabelecimento,
            alimento,
            quantidade,
            validade,
            endereco,
            "Disponível"
        )

        cursor.execute(sql, valores)

        conexao.commit()

        cursor.close()
        conexao.close()

        return redirect("/doacoes")

    return render_template("cadastrar.html")


@app.route("/doacoes")
def doacoes():

    conexao = conectar()

    cursor = conexao.cursor(dictionary=True)

    cursor.execute("""
        SELECT *
        FROM doacoes
        ORDER BY id DESC
    """)

    lista_doacoes = cursor.fetchall()

    cursor.close()
    conexao.close()

    return render_template(
        "doacoes.html",
        doacoes=lista_doacoes
    )


@app.route("/reservar/<int:id>")
def reservar(id):

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute(
        """
        UPDATE doacoes
        SET status = 'Reservado'
        WHERE id = %s
        """,
        (id,)
    )

    conexao.commit()

    cursor.close()
    conexao.close()

    return redirect("/doacoes")


if __name__ == "__main__":
    app.run(debug=True)