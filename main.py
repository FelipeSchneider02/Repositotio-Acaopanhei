import customtkinter as ctk
from create import Create
from petview import PetView
from ownerview import OwnerView
from services import pegar_id_pet, lista_pets_logado


class Main(ctk.CTkToplevel):
    def __init__(self, id_usuario_logado, *args, **kwargs):
        super().__init__(*args, **kwargs)  # inicializa tela Main
        self.id_usuario_logado = id_usuario_logado
        self.config_tela_main()  # carrega as config da tela main
        self.pegar_pets()  # função para pegar pets
        self.widgets_frame()  # carrega os widgtes do frame
        self.widgets_main()  # carrega os widgtes restantes

    def pegar_pets(self):
        lista_pets = lista_pets_logado(self.id_usuario_logado)

        if lista_pets is None:
            print("bateu aqui")
            self.voltar_tela()
        print(lista_pets)

        self.n = lista_pets  # carrega os pets pelo id do usuario logado
        print("bateu aqui1")

    def config_tela_main(self):
        self.title("Main")  # titulo que aparece na tela
        self.geometry("600x400")  # dimensoes x, y da tela
        self.resizable(False, False)  # nao permite usuario ajustar tela
        self.protocol("WM_DELETE_WINDOW", self.fechar_tudo)  # chama método ao fechar

    def widgets_frame(self):
        if not self.winfo_exists():
            return  # Cancela a função se a janela já não existe

        for widget in self.winfo_children():
            widget.destroy()  # Remove todos os widgets antes de recriar
        # ====================================criação de widgets========================================================
        # frame
        main_frame = ctk.CTkFrame(self, width=500, height=350, corner_radius=10)
        main_frame.pack(padx=20, pady=20)
        main_frame.grid_columnconfigure((0, 1), weight=1)

        # labels
        main_titulo_label = ctk.CTkLabel(main_frame, text="LISTA PETS", font=("Roboto", 18), width=150, height=30)

        # option box
        pet_var = ctk.StringVar(value="Pets cadastrados")
        self.pet_cadastrado_optionbox = ctk.CTkOptionMenu(main_frame, values=self.n, variable=pet_var,
                                                          font=("Roboto", 14), width=300, height=30)

        # buttons
        pet_criar_button = ctk.CTkButton(main_frame, text="Cadastrar pet", command=self.criar_pet, font=("Roboto", 14),
                                         width=300, height=30, fg_color="green")
        pet_view_button = ctk.CTkButton(main_frame, text="Visualizar", command=self.view_pet, font=("Roboto", 14),
                                        width=100, height=30, fg_color="orange")

        # ==============================================================================================================
        # ===================================definindo lugares dos widgets==============================================
        main_titulo_label.grid(row=0, column=0, pady=30, columnspan=2)
        self.pet_cadastrado_optionbox.grid(row=1, column=0, pady=30, columnspan=1)
        pet_view_button.grid(row=1, column=1, pady=30, columnspan=1)
        pet_criar_button.grid(row=2, column=0, pady=30, columnspan=2)

    def criar_pet(self):  # função para ir para tela de cadastrar novo pet
        self.withdraw()  # esconde a tela
        self.toplevel_window = Create(self, self.id_usuario_logado)

    def view_pet(self):  # função para ir para a tela de vizualizar um pet já criado
        # pega o pet através das opções do option box
        nome_pet_view = self.pet_cadastrado_optionbox.get()

        # verifica se tem algo no pets
        if nome_pet_view != "Pets cadastrados":
            self.id_pet_view = pegar_id_pet(nome_pet_view, self.id_usuario_logado)  # retornar o id pet
            self.withdraw()
            self.toplevel_window = PetView(self, self.id_pet_view)

        else:
            return

    def widgets_main(self):
        # ====================================criação de widgets========================================================
        # definindo botao voltar
        voltar_button = ctk.CTkButton(self, text="Voltar para login", command=self.voltar_tela,
                                      font=("Roboto", 14), width=150, height=30)

        editar_button = ctk.CTkButton(self, text="Visualizar responsável", command=self.visualizar_responsavel,
                                      font=("Roboto", 14), width=150, height=30, fg_color="orange")

        # ==============================================================================================================
        # ===================================definindo lugares dos widgets==============================================
        voltar_button.place(x=350, y=360)
        editar_button.place(x=100, y=360)

    def visualizar_responsavel(self):  # função para ir para a tela de visualizar dados responsavel
        self.withdraw()
        self.toplevel_window = OwnerView(self, self.id_usuario_logado)

    def atualizar_dados(self):
        # atualiza os dados quando for editado
        self.pegar_pets()  # Recarrega os dados do banco
        self.widgets_frame()  # Recria os widgets com os novos dados
        self.widgets_main()  # Recria os widgets

    def voltar_tela(self):
        if self.master:
            self.master.deiconify()
        self.destroy()

    def fechar_tudo(self):
        self.quit()  # Encerra a aplicação
