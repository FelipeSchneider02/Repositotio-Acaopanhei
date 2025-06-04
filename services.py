import databaser


def autenticar_usuario(login, password):
    # Verifica se o usuário existe e retorna o ID
    databaser.cur.execute("""
            SELECT id_usuario FROM Usuarios
            WHERE login = ? AND password = ?
        """, (login, password))
    resultado = databaser.cur.fetchone()
    if resultado:
        id_usuario = resultado[0]
        return id_usuario
    return None


def lista_pets_logado(id_usuario):
    # se sim retorna os pets cadastrados
    databaser.cur.execute("""
                SELECT nome_pet FROM Pets
                WHERE id_responsavel = ?
        """, (id_usuario,))
    lista_pets = [tupla[0] for tupla in databaser.cur.fetchall()]
    print(id_usuario)
    return lista_pets


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

    if not dados_pet:
        return None  # Retorna None caso o pet não seja encontrado

    return {
        "nome": dados_pet[0],
        "raca": dados_pet[1],
        "sexo": dados_pet[2],
        "observacao": dados_pet[3] if dados_pet[3] is not None else "Sem observação"
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

    if not dados_owner:
        return None

    celular_formatado = "+55" + dados_owner[1] + dados_owner[2]

    return {
        "nome": dados_owner[0],
        "ddd": dados_owner[1],
        "celular": dados_owner[2],
        "login": dados_owner[3],
        "celular_formatado": celular_formatado,
    }


def atualizar_owner(id_usuario_logado, novo_login, novo_nome, novo_ddd, novo_celular):
    # pega o id e atualiza os dados do responsável
    databaser.cur.execute("""
        UPDATE Responsaveis SET nome_responsavel = ?, ddd = ?, celular = ? WHERE id_usuario = ?
    """, (novo_nome, novo_ddd, novo_celular, id_usuario_logado))

    # pega o id e atualiza o login
    databaser.cur.execute("""
        UPDATE Usuarios SET login = ? WHERE id_usuario = ?
    """, (novo_login, id_usuario_logado))

    # salva o banco de dados
    databaser.conn.commit()


def atualizar_pet(id_pet_view, novo_nome, novo_raca, novo_sexo, novo_obs):
    # pega o id e atualiza os dados do pet
    databaser.cur.execute("""
        UPDATE Pets SET nome_pet = ?, raca_pet = ?, sexo_pet = ? WHERE id_pet = ?
    """, (novo_nome, novo_raca, novo_sexo, id_pet_view))

    # pega o id e atualiza observação
    databaser.cur.execute("""
        UPDATE Observacoes SET observacao = ? WHERE id_pet = ?
    """, (novo_obs, id_pet_view))

    # salva o banco de dados
    databaser.conn.commit()


def apagar_pet(id_pet_delete):
    databaser.cur.execute("DELETE FROM Observacoes WHERE id_pet = ?", (id_pet_delete,))
    databaser.conn.commit()

    databaser.cur.execute("DELETE FROM Pets WHERE id_pet = ?", (id_pet_delete, ))
    databaser.conn.commit()


def apagar_owner(id_owner_delete):
    databaser.cur.execute("SELECT id_responsavel FROM Responsaveis WHERE id_usuario = ?", (id_owner_delete, ))
    id_responsavel = databaser.cur.fetchone()[0]

    databaser.cur.execute("DELETE FROM Pets WHERE id_responsavel = ?", (id_responsavel, ))
    databaser.conn.commit()

    databaser.cur.execute("DELETE FROM Responsaveis WHERE id_usuario = ?", (id_owner_delete, ))
    databaser.conn.commit()

    databaser.cur.execute("DELETE FROM Usuarios WHERE id_usuario = ?", (id_owner_delete, ))
    databaser.conn.commit()
