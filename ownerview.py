import customtkinter as ctk
from services import dados_owners


class OwnerView(ctk.CTkToplevel):
    def __init__(self, master, id_usuario_logado, *args, **kwargs):
        super().__init__(*args, **kwargs)  # inicializa tela Main
        self.master = master
        self.id_usuario_logado = id_usuario_logado
        self.config_tela_main()  # carrega as config da tela main
        self.pegar_infos_owner()
        self.widgets_view()  # carrega os widgtes do frame

    def config_tela_main(self):
        self.title("Owner view")  # titulo que aparece na tela
        self.geometry("600x400")  # dimensoes x, y da tela
        self.resizable(False, False)  # nao permite usuario ajustar tela
        self.protocol("WM_DELETE_WINDOW", self.fechar_tudo)  # Chama método ao fechar

    def pegar_infos_owner(self):
        # retorna um dicionario usando a função dados_owner para pegar as informações do responsável
        dados = dados_owners(self.id_usuario_logado)

        self.nome = dados["nome"]
        self.celular_formatado = dados["celular"]
        self.login = dados["login"]

    def widgets_view(self):
        # ====================================criação de widgets========================================================
        # frame
        tela_frame = ctk.CTkScrollableFrame(self, width=400, height=350, corner_radius=10)
        tela_frame.pack(padx=20, pady=20)
        tela_frame.grid_columnconfigure((0, 1), weight=1)

        # labels
        owner_label = ctk.CTkLabel(tela_frame, text="DADOS DO RESPONSAVEL", font=("Roboto", 18), width=300, height=30)

        login_label = ctk.CTkLabel(tela_frame, text="Login", font=("Roboto", 14), fg_color="gray22",
                                   width=100, height=30)
        owner_login_label = ctk.CTkLabel(tela_frame, text=self.nome, font=("Roboto", 14), anchor="w",
                                         width=200, height=30)

        nome_label = ctk.CTkLabel(tela_frame, text="Nome", font=("Roboto", 14), fg_color="gray22", width=100, height=30)
        owner_nome_label = ctk.CTkLabel(tela_frame, text=self.nome, font=("Roboto", 14), anchor="w",
                                        width=200, height=30)

        celular_label = ctk.CTkLabel(tela_frame, text="Celular", font=("Roboto", 14), fg_color="gray22",
                                     width=100, height=30)
        owner_celular_label = ctk.CTkLabel(tela_frame, text=self.celular_formatado, font=("Roboto", 14), anchor="w",
                                           width=200, height=30)

        espaco_label = ctk.CTkLabel(tela_frame, text="", width=100, height=30)

        # buttons
        editar_button = ctk.CTkButton(tela_frame, text="Editar", command=self.editar_owner, font=("Roboto", 14),
                                      fg_color="dark goldenrod", width=130, height=30)

        deletar_button = ctk.CTkButton(tela_frame, text="Deletar", command=self.deletar_owner, font=("Roboto", 14),
                                       fg_color="red", width=130, height=30)

        voltar_button = ctk.CTkButton(tela_frame, text="Voltar", command=self.voltar_tela, font=("Roboto", 14),
                                      width=130, height=30)

        # ==============================================================================================================
        # ===================================definindo lugares dos widgets==============================================
        owner_label.grid(row=0, column=0, pady=20, columnspan=3)
        login_label.grid(row=1, column=0, pady=5, columnspan=1)
        owner_login_label.grid(row=1, column=1, pady=5, columnspan=1)
        nome_label.grid(row=2, column=0, pady=5, columnspan=1)
        owner_nome_label.grid(row=2, column=1, pady=5, columnspan=2)
        celular_label.grid(row=3, column=0, pady=5, columnspan=1)
        owner_celular_label.grid(row=3, column=1, pady=5, columnspan=2)
        espaco_label.grid(row=4, column=0, pady=5)  # para deixar espaçado igual viewpet
        editar_button.grid(row=5, column=0, pady=10, sticky="w", columnspan=3)
        deletar_button.grid(row=5, column=1, pady=10, sticky="e", columnspan=3)
        voltar_button.grid(row=6, column=0, pady=10, sticky="e", columnspan=3)

    def editar_owner(self):
        ...

    def deletar_owner(self):
        ...

    def voltar_tela(self):
        if self.master:
            self.master.deiconify()
        self.destroy()

    def fechar_tudo(self):
        self.quit()  # Encerra a aplicação
