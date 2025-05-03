import customtkinter as ctk
from services import dados_owners, atualizar_owner


class EditOwnerView(ctk.CTkToplevel):
    def __init__(self, master, id_usuario_logado, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.master = master
        self.id_usuario_logado = id_usuario_logado
        self.config_tela()
        self.pegar_infos_owner()
        self.widgets_edit()

    def config_tela(self):
        self.title("Editar Responsável")
        self.geometry("600x400")
        self.resizable(False, False)
        self.protocol("WM_DELETE_WINDOW", self.fechar_tudo)

    def pegar_infos_owner(self):
        dados = dados_owners(self.id_usuario_logado)
        self.login = dados["login"]
        self.nome = dados["nome"]
        self.ddd = dados["ddd"]
        self.celular = dados["celular"]

    def widgets_edit(self):
        # ====================================criação de widgets========================================================
        # frame
        tela_frame = ctk.CTkScrollableFrame(self, width=400, height=350, corner_radius=10)
        tela_frame.pack(padx=20, pady=20)
        tela_frame.grid_columnconfigure((0, 1), weight=1)

        # labels
        owner_label = ctk.CTkLabel(tela_frame, text="DADOS DO RESPONSAVEL", font=("Roboto", 18), width=300, height=30)

        login_label = ctk.CTkLabel(tela_frame, text="Login", font=("Roboto", 14), fg_color="gray22",
                                   width=100, height=30)

        nome_label = ctk.CTkLabel(tela_frame, text="Nome", font=("Roboto", 14), fg_color="gray22", width=100, height=30)

        ddd_label = ctk.CTkLabel(tela_frame, text="ddd", font=("Roboto", 14), fg_color="gray22",
                                 width=100, height=30)

        celular_label = ctk.CTkLabel(tela_frame, text="celular", font=("Roboto", 14), fg_color="gray22",
                                     width=100, height=30)

        espaco_label = ctk.CTkLabel(tela_frame, text="", width=100, height=30)

        # entrys
        self.login_entry = ctk.CTkEntry(tela_frame, font=("Roboto", 14), width=200)
        self.login_entry.insert(0, self.login)

        self.nome_entry = ctk.CTkEntry(tela_frame, font=("Roboto", 14), width=200)
        self.nome_entry.insert(0, self.nome)

        self.ddd_entry = ctk.CTkEntry(tela_frame, font=("Roboto", 14), width=200)
        self.ddd_entry.insert(0, self.ddd)

        self.celular_entry = ctk.CTkEntry(tela_frame, font=("Roboto", 14), width=200)
        self.celular_entry.insert(0, self.celular)

        # buttons
        salvar_button = ctk.CTkButton(tela_frame, text="Salvar", command=self.salvar_owner, font=("Roboto", 14),
                                      fg_color="green4", width=130, height=30)

        voltar_button = ctk.CTkButton(tela_frame, text="Voltar", command=self.voltar_tela, font=("Roboto", 14),
                                      width=130, height=30)

        # ==============================================================================================================
        # ===================================definindo lugares dos widgets==============================================
        owner_label.grid(row=0, column=0, pady=20, columnspan=3)
        login_label.grid(row=1, column=0, pady=5, columnspan=1)
        self.login_entry.grid(row=1, column=1, pady=5, columnspan=1)
        nome_label.grid(row=2, column=0, pady=5, columnspan=1)
        self.nome_entry.grid(row=2, column=1, pady=5, columnspan=1)
        ddd_label.grid(row=3, column=0, pady=5, columnspan=1)
        self.ddd_entry.grid(row=3, column=1, pady=5, columnspan=1)
        celular_label.grid(row=4, column=0, pady=5, columnspan=1)
        self.celular_entry.grid(row=4, column=1, pady=5, columnspan=1)
        espaco_label.grid(row=5, column=0, pady=5)  # para deixar espaçado igual viewpet
        salvar_button.grid(row=6, column=0, pady=15, sticky="w", columnspan=3)
        voltar_button.grid(row=6, column=1, pady=15, sticky="e", columnspan=3)

    def salvar_owner(self):
        novo_login = self.login_entry.get()
        novo_nome = self.nome_entry.get()
        novo_ddd = self.ddd_entry.get()
        novo_celular = self.celular_entry.get()

        atualizar_owner(self.id_usuario_logado, novo_login, novo_nome, novo_ddd, novo_celular)
        self.voltar_tela()

    def voltar_tela(self):
        if self.master:
            self.master.atualizar_dados()  # Atualiza os dados antes de exibir a tela novamente
            self.master.deiconify()
        self.destroy()

    def fechar_tudo(self):
        self.quit()  # Encerra a aplicação
