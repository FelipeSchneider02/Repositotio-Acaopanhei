import customtkinter as ctk
from services import dados_pets, atualizar_pet


class EditPetView(ctk.CTkToplevel):
    def __init__(self, master, id_pet_view, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.master = master
        self.id_pet_view = id_pet_view
        self.config_tela()
        self.pegar_infos_pet()
        self.widgets_edit()

    def config_tela(self):
        self.title("Editar Pet")
        self.geometry("600x400")
        self.resizable(False, False)
        self.protocol("WM_DELETE_WINDOW", self.fechar_tudo)

    def pegar_infos_pet(self):
        # retorna um dicionario usando a função dados_pets para pegar as informações do pet
        dados = dados_pets(self.id_pet_view)

        self.nome = dados["nome"]
        self.raca = dados["raca"]
        self.sexo = dados["sexo"]
        self.observacao = dados["observacao"]

    def widgets_edit(self):
        # ====================================criação de widgets========================================================
        # frame
        tela_frame = ctk.CTkScrollableFrame(self, width=400, height=350, corner_radius=10)
        tela_frame.pack(padx=20, pady=20)
        tela_frame.grid_columnconfigure((0, 1), weight=1)

        # labels
        pet_label = ctk.CTkLabel(tela_frame, text="DADOS DO PET", font=("Roboto", 18), width=300, height=30)

        nome_label = ctk.CTkLabel(tela_frame, text="Nome", font=("Roboto", 14), fg_color="gray22",
                                  width=100, height=30)

        raca_label = ctk.CTkLabel(tela_frame, text="Raça", font=("Roboto", 14), fg_color="gray22", width=100, height=30)

        sexo_label = ctk.CTkLabel(tela_frame, text="Sexo", font=("Roboto", 14), fg_color="gray22",
                                  width=100, height=30)

        observacao_label = ctk.CTkLabel(tela_frame, text="Observação", font=("Roboto", 14), fg_color="gray22",
                                        width=100, height=30)

        self.espaco_label = ctk.CTkLabel(tela_frame, text="", width=100, height=30)

        # entrys
        self.nome_entry = ctk.CTkEntry(tela_frame, font=("Roboto", 14), width=200)
        self.nome_entry.insert(0, self.nome)

        self.raca_entry = ctk.CTkEntry(tela_frame, font=("Roboto", 14), width=200)
        self.raca_entry.insert(0, self.raca)

        self.observacao_entry = ctk.CTkEntry(tela_frame, font=("Roboto", 14), width=200)
        self.observacao_entry.insert(0, self.observacao)

        # optionmenu
        sexo_var = ctk.StringVar(value=self.sexo)
        self.sexo_optionmenu = ctk.CTkOptionMenu(tela_frame, values=["M", "F"], variable=sexo_var, font=("Roboto", 14),
                                                 width=200, height=30)


        # buttons
        salvar_button = ctk.CTkButton(tela_frame, text="Salvar", command=self.salvar_petview, font=("Roboto", 14),
                                      fg_color="green4", width=130, height=30)

        voltar_button = ctk.CTkButton(tela_frame, text="Voltar", command=self.voltar_tela, font=("Roboto", 14),
                                      width=130, height=30)

        # ==============================================================================================================
        # ===================================definindo lugares dos widgets==============================================
        pet_label.grid(row=0, column=0, pady=20, columnspan=3)
        nome_label.grid(row=1, column=0, pady=5, columnspan=1)
        self.nome_entry.grid(row=1, column=1, pady=5, columnspan=1)
        raca_label.grid(row=2, column=0, pady=5, columnspan=1)
        self.raca_entry.grid(row=2, column=1, pady=5, columnspan=1)
        sexo_label.grid(row=3, column=0, pady=5, columnspan=1)
        self.sexo_optionmenu.grid(row=3, column=1, pady=5, columnspan=1)
        observacao_label.grid(row=4, column=0, pady=5, columnspan=1)
        self.observacao_entry.grid(row=4, column=1, pady=5, columnspan=1)
        self.espaco_label.grid(row=5, column=0, pady=5)  # para deixar espaçado igual viewpet
        salvar_button.grid(row=6, column=0, pady=15, sticky="w", columnspan=3)
        voltar_button.grid(row=6, column=1, pady=15, sticky="e", columnspan=3)

    def salvar_petview(self):
        # criar services
        novo_nome = self.nome_entry.get()
        novo_raca = self.raca_entry.get()
        novo_sexo = self.sexo_optionmenu.get()
        novo_obs = self.observacao_entry.get()

        # verifica se todos os campos estão ocupados
        if not all([novo_nome, novo_raca, novo_sexo, novo_obs]):
            self.espaco_label.configure(text="Preencha todos os campos")
            return

        atualizar_pet(self.id_pet_view, novo_nome, novo_raca, novo_sexo, novo_obs)

        self.voltar_tela()

    def voltar_tela(self):
        if self.master:
            self.master.atualizar_dados()  # Atualiza os dados antes de exibir a tela novamente /// criar
            self.master.deiconify()
        self.destroy()

    def fechar_tudo(self):
        self.quit()  # Encerra a aplicação
