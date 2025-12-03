from faker import Faker
import random
import pyodbc

from configs import build_odbc_conn_str  # usa configs.py

fake = Faker("pt_BR")


def main():
    conn_str = build_odbc_conn_str()
    conn = pyodbc.connect(conn_str)
    cur = conn.cursor()

    N = 100  # número de associados

    for _ in range(N):
        # ASSOCIADO
        nome = fake.first_name()
        sobrenome = fake.last_name()
        idade = random.randint(18, 75)
        email = fake.email()

        cur.execute("""
            INSERT INTO associado (nome, sobrenome, idade, email)
            OUTPUT INSERTED.id
            VALUES (?, ?, ?, ?);
        """, (nome, sobrenome, idade, email))
        id_associado = cur.fetchone()[0]

        # CONTA
        tipo = random.choice(["CORRENTE", "POUPANCA"])
        data_criacao = fake.date_time_between(start_date="-3y", end_date="now")

        cur.execute("""
            INSERT INTO conta (tipo, data_criacao, id_associado)
            OUTPUT INSERTED.id
            VALUES (?, ?, ?);
        """, (tipo, data_criacao, id_associado))
        id_conta = cur.fetchone()[0]

        # CARTAO
        num_cartao = fake.random_number(digits=16)
        nom_impresso = f"{nome} {sobrenome}".upper()

        cur.execute("""
            INSERT INTO cartao (num_cartao, nom_impresso, id_conta, id_associado)
            OUTPUT INSERTED.id
            VALUES (?, ?, ?, ?);
        """, (num_cartao, nom_impresso, id_conta, id_associado))
        id_cartao = cur.fetchone()[0]

        # MOVIMENTOS
        for _ in range(random.randint(3, 8)):
            valor = round(random.uniform(10, 1500), 2)
            descricao = random.choice([
                "Supermercado", "Restaurante",
                "Farmácia", "Combustível", "Online"
            ])
            data_movimento = fake.date_time_between(start_date="-1y", end_date="now")

            cur.execute("""
                INSERT INTO movimento (vlr_transacao, des_transacao, data_movimento, id_cartao)
                VALUES (?, ?, ?, ?);
            """, (valor, descricao, data_movimento, id_cartao))

    conn.commit()
    cur.close()
    conn.close()
    print("Dados gerados com sucesso!")


if __name__ == "__main__":
    main()
