import databaser


def autenticar_usuario(login, password):
    # Verifica se o usuário existe e retorna o ID
    databaser.cur.execute("""
            SELECT id_usuario FROM Usuarios
            WHERE login = ? AND password = ?
        """, (login, password))
    resultado = databaser.cur.fetchone()

    # se sim retorna os pets cadastrados
    if resultado:
        id_usuario = resultado[0]
        databaser.cur.execute("""
                SELECT nome_pet FROM Pets
                WHERE id_responsavel = ?
            """, (id_usuario,))
        lista_pets = [tupla[0] for tupla in databaser.cur.fetchall()]
        return id_usuario, lista_pets
    return None, None


class RegisterService:
    @staticmethod
    def verificar_login_existente(login):
        # Verifica se um login já está cadastrado no banco de dados
        databaser.cur.execute("SELECT COUNT(*) FROM Usuarios WHERE login = ?", (login,))
        return databaser.cur.fetchone()[0] > 0

    @staticmethod
    def cadastrar_usuario(login, password, nome, ddd, celular):
        # Registra um novo usuário e retorna True se for bem-sucedido
        try:
            databaser.cur.execute("INSERT INTO Usuarios (login, password) VALUES (?, ?)", (login, password))
            databaser.conn.commit()

            # Obtém o ID do novo usuário cadastrado
            databaser.cur.execute("SELECT id_usuario FROM Usuarios ORDER BY id_usuario DESC LIMIT 1")
            id_usuario = databaser.cur.fetchone()[0]

            # Insere os dados na tabela Responsaveis
            databaser.cur.execute(
                "INSERT INTO Responsaveis (nome_responsavel, ddd, celular, id_usuario) VALUES (?, ?, ?, ?)",
                (nome, ddd, celular, id_usuario),
            )
            databaser.conn.commit()

            return True  # Cadastro bem-sucedido

        except Exception as e:
            print(f"Erro ao registrar usuário: {e}")
            return False


def cadastrar_pet(nome, raca, sexo, obs, id_responsavel):
    # registra um novo pet na Pets e retorna True se der certo
    try:
        databaser.cur.execute(
            "INSERT INTO Pets (nome_pet, raca_pet, sexo_pet, id_responsavel) VALUES (?, ?, ?, ?)",
            (nome, raca, sexo, id_responsavel)
        )
        databaser.conn.commit()

        # obtém o ID do novo pet cadastrado
        databaser.cur.execute("SELECT id_pet FROM Pets ORDER BY id_pet DESC LIMIT 1")
        id_pet = databaser.cur.fetchone()[0]

        # insere a obs
        databaser.cur.execute("INSERT INTO Observacoes (id_pet, observacao) VALUES (?, ?)", (id_pet, obs))
        databaser.conn.commit()

        return True

    except Exception as e:
        print(f"Erro ao registrar pet: {e}")
        return False


def pegar_id_pet(nome_pet_view, id_usuario):
    # pega o id do pet com base no nome do pet e do id_usuario
    databaser.cur.execute(
        "SELECT id_pet FROM Pets WHERE nome_pet = ? AND id_responsavel = ?", (nome_pet_view, id_usuario)
    )
    id_pet_view = databaser.cur.fetchone()[0]
    return id_pet_view


def dados_pets(id_pet_view):
    # pega o id do pet que está sendo visualizado e retorna as informações
    databaser.cur.execute("""
        SELECT p.nome_pet, p.raca_pet, p.sexo_pet, o.observacao
        FROM Pets p
        LEFT JOIN Observacoes o ON p.id_pet = o.id_pet
        WHERE p.id_pet = ?
        """, (id_pet_view, ))

    dados_pet = databaser.cur.fetchone()
    return {
        "nome": dados_pet[0],
        "raca": dados_pet[1],
        "sexo": dados_pet[2],
        "observacao": dados_pet[3]
    }


def dados_owners(id_usuario_logado):
    # pega o id do pet que está sendo visualizado e retorna as informações
    databaser.cur.execute("""
        SELECT r.nome_responsavel, r.ddd, r.celular, u.login
        FROM Responsaveis r
        JOIN Usuarios u ON r.id_usuario = u.id_usuario
        WHERE u.id_usuario = ?
        """, (id_usuario_logado, ))

    dados_owner = databaser.cur.fetchone()
    celular_formatado = "+55" + dados_owner[1] + dados_owner[2]

    return {
        "nome": dados_owner[0],
        "celular": celular_formatado,
        "login": dados_owner[3]
    }
