import customtkinter as ctk
from editpetview import EditPetView
from services import dados_pets


class PetView(ctk.CTkToplevel):
    def __init__(self, master, id_pet_view, *args, **kwargs):
        super().__init__(*args, **kwargs)  # inicializa tela Main
        self.master = master
        self.id_pet_view = id_pet_view
        self.config_tela_main()  # carrega as config da tela main
        self.pegar_infos_pet()
        self.widgets_view()  # carrega os widgtes do frame

    def config_tela_main(self):
        self.title("Petview")  # titulo que aparece na tela
        self.geometry("600x400")  # dimensoes x, y da tela
        self.resizable(False, False)  # nao permite usuario ajustar tela
        self.protocol("WM_DELETE_WINDOW", self.fechar_tudo)  # Chama método ao fechar

    def pegar_infos_pet(self):
        # retorna um dicionario usando a função dados_pets para pegar as informações do pet
        dados = dados_pets(self.id_pet_view)

        self.nome = dados["nome"]
        self.raca = dados["raca"]

        # pega o Char que vier e transforma em texto
        self.sexo = dados["sexo"]
        if self.sexo == "F":
            self.sexo = "Feminino"
        else:
            self.sexo = "Masculino"

        self.observacao = dados["observacao"]

    def widgets_view(self):
        for widget in self.winfo_children():
            widget.destroy()  # Remove todos os widgets antes de recriar
        # ====================================criação de widgets========================================================
        # frame
        tela_frame = ctk.CTkScrollableFrame(self, width=400, height=350, corner_radius=10)
        tela_frame.pack(padx=20, pady=20)
        tela_frame.grid_columnconfigure((0, 1), weight=1)

        # labels
        pet_label = ctk.CTkLabel(tela_frame, text="DADOS DO PET", font=("Roboto", 18), width=300, height=30)

        nome_label = ctk.CTkLabel(tela_frame, text="Nome", font=("Roboto", 14), fg_color="gray22", width=100, height=30)
        pet_nome_label = ctk.CTkLabel(tela_frame, text=self.nome, font=("Roboto", 14), anchor="w",
                                      width=200, height=30)

        raca_label = ctk.CTkLabel(tela_frame, text="Raça", font=("Roboto", 14), fg_color="gray22",
                                  width=100, height=30)
        pet_raca_label = ctk.CTkLabel(tela_frame, text=self.raca, font=("Roboto", 14), anchor="w",
                                      width=200, height=30)

        sexo_label = ctk.CTkLabel(tela_frame, text="Sexo", font=("Roboto", 14), fg_color="gray22",
                                  width=100, height=30)
        pet_sexo_label = ctk.CTkLabel(tela_frame, text=self.sexo, font=("Roboto", 14), anchor="w",
                                      width=200, height=30)

        observacao_label = ctk.CTkLabel(tela_frame, text="Observação", font=("Roboto", 14), fg_color="gray22",
                                        width=100, height=30)
        pet_observacao_label = ctk.CTkLabel(tela_frame, text=self.observacao, font=("Roboto", 14), anchor="w",
                                            width=200, height=30)

        # buttons
        editar_button = ctk.CTkButton(tela_frame, text="Editar", command=self.editar_pet, font=("Roboto", 14),
                                      fg_color="dark goldenrod", width=130, height=30)

        deletar_button = ctk.CTkButton(tela_frame, text="Deletar", command=self.deletar_pet, font=("Roboto", 14),
                                       fg_color="red", width=130, height=30)

        voltar_button = ctk.CTkButton(tela_frame, text="Voltar", command=self.voltar_tela, font=("Roboto", 14),
                                      width=130, height=30)

        # ==============================================================================================================
        # ===================================definindo lugares dos widgets==============================================
        pet_label.grid(row=0, column=0, pady=20, columnspan=3)
        nome_label.grid(row=1, column=0, pady=5, columnspan=1)
        pet_nome_label.grid(row=1, column=1, pady=5, columnspan=2)
        raca_label.grid(row=2, column=0, pady=5, columnspan=1)
        pet_raca_label.grid(row=2, column=1, pady=5, columnspan=2)
        sexo_label.grid(row=3, column=0, pady=5, columnspan=1)
        pet_sexo_label.grid(row=3, column=1, pady=5, columnspan=2)
        observacao_label.grid(row=4, column=0, pady=5, columnspan=1)
        pet_observacao_label.grid(row=4, column=1, pady=5, columnspan=2)
        editar_button.grid(row=5, column=0, pady=10, sticky="w", columnspan=3)
        deletar_button.grid(row=5, column=1, pady=10, sticky="e", columnspan=3)
        voltar_button.grid(row=6, column=0, pady=10, sticky="e", columnspan=3)

    def editar_pet(self):
        self.withdraw()
        self.toplevel_window = EditPetView(self, self.id_pet_view)

    def atualizar_dados(self):
        # atualiza os dados quando for editado
        self.pegar_infos_pet()  # Recarrega os dados do banco
        self.widgets_view()  # Recria os widgets com os novos dados

    def deletar_pet(self):
        ...

    def voltar_tela(self):
        if self.master:
            self.master.atualizar_dados()
            self.master.deiconify()
        self.destroy()

    def fechar_tudo(self):
        self.quit()  # Encerra a aplicação
