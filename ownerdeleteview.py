import customtkinter as ctk
from services import dados_owners, apagar_owner


class OwnerDeleteView(ctk.CTkToplevel):
    def __init__(self, master, id_owner_delete, *args, **kwargs):
        super().__init__(*args, **kwargs)  # inicializa tela Main
        self.master = master
        self.id_owner_delete = id_owner_delete
        self.config_tela_delete()  # carrega as config da tela main
        self.pegar_infos()
        self.widgets_view()  # carrega os widgtes do frame

    def config_tela_delete(self):
        self.title("Deletar Pet")  # titulo que aparece na tela
        self.geometry("600x400")  # dimensoes x, y da tela
        self.resizable(False, False)  # nao permite usuario ajustar tela
        self.protocol("WM_DELETE_WINDOW", self.fechar_tudo)  # Chama método ao fechar

    def pegar_infos(self):
        # retorna um dicionario usando a função dados_pets para pegar as informações do pet
        dados = dados_owners(self.id_owner_delete)

        self.nome = dados["nome"]

    def widgets_view(self):
        # ====================================criação de widgets========================================================
        # frame
        tela_frame = ctk.CTkScrollableFrame(self, width=400, height=350, corner_radius=10)
        tela_frame.pack(padx=20, pady=20)
        tela_frame.grid_columnconfigure((0, 1), weight=1)

        # labels
        owner_label = ctk.CTkLabel(tela_frame, text="DADOS DO USÚARIO A SER DELETADO",
                                   font=("Roboto", 18), width=300, height=30)

        nome_label = ctk.CTkLabel(tela_frame, text="Nome", font=("Roboto", 14), fg_color="gray22", width=100, height=30)
        owner_nome_label = ctk.CTkLabel(tela_frame, text=self.nome, font=("Roboto", 14), anchor="w",
                                        width=200, height=30)

        info_label = ctk.CTkLabel(tela_frame, text="Tem certeza que deseja deletar o cadastro?",
                                  font=("Roboto", 16), width=100, height=30)

        # buttons
        deletar_button = ctk.CTkButton(tela_frame, text="Deletar", command=self.deletar_pet, font=("Roboto", 14),
                                       fg_color="red", width=130, height=30)

        voltar_button = ctk.CTkButton(tela_frame, text="Voltar", command=self.voltar_tela, font=("Roboto", 14),
                                      width=130, height=30)

        # ==============================================================================================================
        # ===================================definindo lugares dos widgets==============================================
        owner_label.grid(row=0, column=0, pady=20, columnspan=3)
        nome_label.grid(row=1, column=0, pady=5, columnspan=1)
        owner_nome_label.grid(row=1, column=1, pady=5, columnspan=2)
        info_label.grid(row=2, column=0, pady=80, columnspan=3)
        deletar_button.grid(row=6, column=1, pady=5, sticky="e", columnspan=3)
        voltar_button.grid(row=6, column=0, pady=5, sticky="w", columnspan=3)

    def deletar_pet(self):
        apagar_owner(self.id_owner_delete)

        # Se a janela do PetView ainda existir, atualiza os dados
        if self.master and self.master.winfo_exists():
            if self.master and self.master.winfo_exists():
                self.master.atualizar_dados()

        self.voltar_tela()

    def voltar_tela(self):
        if self.master and self.master.winfo_exists():
            self.master.atualizar_dados()
            self.master.deiconify()  # Reexibe a tela principal caso ainda exista
        self.destroy()

    def fechar_tudo(self):
        self.quit()  # Encerra a aplicação
