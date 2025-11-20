import tkinter as tk
from tkinter import ttk, scrolledtext
import threading
import httpx
from datetime import datetime

# Configurações
cliente_echat = "laboclin"
token_echat = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6IkFkbWluaXN0cmFkb3IiLCJwcm9maWxlIjoiYWRtaW4iLCJpZCI6MSwidG9rZW5WZXJzaW9uIjozLCJpYXQiOjE3NjI0NjE1ODQsImV4cCI6MTc2MjQ2Mzk4NH0.tCNc1EPmVkaBRLJsvBqsZ57xC2zYdGZirdPzTtK5Az4"
headers_echat = {"Authorization": f"Bearer {token_echat}"}

cliente_echat2 = "laboclinlab"
token_echat2 = "PHPSESSID=5vk8bf3blj77imv8bmbrau4nmg"
headers_echat2 = {"Cookie": f"{token_echat2}"}


class EchatMigrationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Migração eChat - Laboclin")
        self.root.geometry("900x700")
        self.root.configure(bg="#1e1e2e")
        
        self.is_running = False
        self.setup_ui()
    
    def setup_ui(self):
        # Título
        title_frame = tk.Frame(self.root, bg="#1e1e2e")
        title_frame.pack(pady=20)
        
        tk.Label(
            title_frame,
            text="🔄 Migração de Dados eChat",
            font=("Helvetica", 24, "bold"),
            bg="#1e1e2e",
            fg="#89b4fa"
        ).pack()
        
        tk.Label(
            title_frame,
            text=f"{cliente_echat} → {cliente_echat2}",
            font=("Helvetica", 12),
            bg="#1e1e2e",
            fg="#a6adc8"
        ).pack()
        
        # Frame de estatísticas
        stats_frame = tk.Frame(self.root, bg="#1e1e2e")
        stats_frame.pack(pady=10, padx=20, fill="x")
        
        self.create_stat_card(stats_frame, "Respostas Rápidas", "respostas", 0)
        self.create_stat_card(stats_frame, "Classificações", "classificacoes", 1)
        self.create_stat_card(stats_frame, "Sub-Classificações", "subclassificacoes", 2)
        
        # Progress bar
        progress_frame = tk.Frame(self.root, bg="#1e1e2e")
        progress_frame.pack(pady=10, padx=20, fill="x")
        
        self.progress = ttk.Progressbar(
            progress_frame,
            mode='indeterminate',
            length=400
        )
        self.progress.pack()
        
        # Botões
        button_frame = tk.Frame(self.root, bg="#1e1e2e")
        button_frame.pack(pady=15)
        
        self.btn_respostas = tk.Button(
            button_frame,
            text="▶ Migrar Respostas Rápidas",
            command=lambda: self.iniciar_migracao("respostas"),
            font=("Helvetica", 11, "bold"),
            bg="#89b4fa",
            fg="#1e1e2e",
            padx=20,
            pady=10,
            relief="flat",
            cursor="hand2"
        )
        self.btn_respostas.grid(row=0, column=0, padx=5)
        
        self.btn_classificacoes = tk.Button(
            button_frame,
            text="▶ Migrar Classificações",
            command=lambda: self.iniciar_migracao("classificacoes"),
            font=("Helvetica", 11, "bold"),
            bg="#f38ba8",
            fg="#1e1e2e",
            padx=20,
            pady=10,
            relief="flat",
            cursor="hand2"
        )
        self.btn_classificacoes.grid(row=0, column=1, padx=5)
        
        self.btn_tudo = tk.Button(
            button_frame,
            text="▶ Migrar Tudo",
            command=lambda: self.iniciar_migracao("tudo"),
            font=("Helvetica", 11, "bold"),
            bg="#a6e3a1",
            fg="#1e1e2e",
            padx=20,
            pady=10,
            relief="flat",
            cursor="hand2"
        )
        self.btn_tudo.grid(row=0, column=2, padx=5)
        
        # Log área
        log_frame = tk.Frame(self.root, bg="#1e1e2e")
        log_frame.pack(pady=10, padx=20, fill="both", expand=True)
        
        tk.Label(
            log_frame,
            text="📋 Logs de Execução",
            font=("Helvetica", 12, "bold"),
            bg="#1e1e2e",
            fg="#cdd6f4"
        ).pack(anchor="w")
        
        self.log_text = scrolledtext.ScrolledText(
            log_frame,
            height=15,
            font=("Courier", 10),
            bg="#313244",
            fg="#cdd6f4",
            insertbackground="#cdd6f4",
            relief="flat",
            padx=10,
            pady=10
        )
        self.log_text.pack(fill="both", expand=True)
        
        # Status bar
        self.status_label = tk.Label(
            self.root,
            text="Pronto para iniciar",
            font=("Helvetica", 10),
            bg="#313244",
            fg="#a6adc8",
            anchor="w",
            padx=10,
            pady=5
        )
        self.status_label.pack(side="bottom", fill="x")
    
    def create_stat_card(self, parent, title, key, col):
        card = tk.Frame(parent, bg="#313244", relief="flat")
        card.grid(row=0, column=col, padx=5, sticky="ew")
        parent.grid_columnconfigure(col, weight=1)
        
        tk.Label(
            card,
            text=title,
            font=("Helvetica", 10),
            bg="#313244",
            fg="#a6adc8"
        ).pack(pady=(10, 5))
        
        stat_label = tk.Label(
            card,
            text="0",
            font=("Helvetica", 24, "bold"),
            bg="#313244",
            fg="#89b4fa"
        )
        stat_label.pack(pady=(0, 10))
        
        setattr(self, f"stat_{key}", stat_label)
    
    def log(self, mensagem, tipo="info"):
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        cores = {
            "info": "#89b4fa",
            "sucesso": "#a6e3a1",
            "erro": "#f38ba8",
            "warning": "#f9e2af"
        }
        
        cor = cores.get(tipo, "#cdd6f4")
        
        self.log_text.insert("end", f"[{timestamp}] ", "timestamp")
        self.log_text.insert("end", f"{mensagem}\n", tipo)
        
        self.log_text.tag_config("timestamp", foreground="#a6adc8")
        self.log_text.tag_config(tipo, foreground=cor)
        self.log_text.see("end")
        self.root.update()
    
    def atualizar_status(self, mensagem):
        self.status_label.config(text=mensagem)
        self.root.update()
    
    def atualizar_estatistica(self, tipo, valor):
        stat_label = getattr(self, f"stat_{tipo}")
        stat_label.config(text=str(valor))
        self.root.update()
    
    def iniciar_migracao(self, tipo):
        if self.is_running:
            self.log("⚠ Já existe uma migração em andamento!", "warning")
            return
        
        self.is_running = True
        self.progress.start()
        self.desabilitar_botoes()
        
        thread = threading.Thread(target=self.executar_migracao, args=(tipo,))
        thread.daemon = True
        thread.start()
    
    def desabilitar_botoes(self):
        self.btn_respostas.config(state="disabled")
        self.btn_classificacoes.config(state="disabled")
        self.btn_tudo.config(state="disabled")
    
    def habilitar_botoes(self):
        self.btn_respostas.config(state="normal")
        self.btn_classificacoes.config(state="normal")
        self.btn_tudo.config(state="normal")
    
    def executar_migracao(self, tipo):
        try:
            if tipo in ["respostas", "tudo"]:
                self.migrar_respostas_rapidas()
            
            if tipo in ["classificacoes", "tudo"]:
                self.migrar_classificacoes()
            
            self.log("✅ Migração concluída com sucesso!", "sucesso")
            self.atualizar_status("Migração concluída")
            
        except Exception as e:
            self.log(f"❌ Erro na migração: {str(e)}", "erro")
            self.atualizar_status("Erro na migração")
        
        finally:
            self.progress.stop()
            self.is_running = False
            self.habilitar_botoes()
    
    def migrar_respostas_rapidas(self):
        self.log("🔍 Buscando respostas rápidas...", "info")
        self.atualizar_status("Buscando respostas rápidas...")
        
        page = 1
        resposta_rapida = []
        
        with httpx.Client(headers=headers_echat, timeout=30.0) as client:
            while True:
                try:
                    params = {"searchParam": "", "pageNumber": page}
                    response = client.get(
                        f"https://{cliente_echat}api.eassystems.com.br/quickAnswers/",
                        params=params,
                    )
                    response.raise_for_status()
                    data = response.json()
                    
                    for linha in data["quickAnswers"]:
                        resposta_rapida.append(
                            {"atalho": linha["shortcut"], "mensagem": linha["message"]}
                        )
                    
                    self.log(f"📄 Página {page}: {len(data['quickAnswers'])} respostas encontradas")
                    
                    if not data["hasMore"]:
                        break
                    
                    page += 1
                    
                except httpx.HTTPError as e:
                    self.log(f"❌ Erro na página {page}: {e}", "erro")
                    break
        
        total = len(resposta_rapida)
        self.log(f"📊 Total de respostas rápidas: {total}", "info")
        self.atualizar_estatistica("respostas", total)
        
        # Enviar para destino
        self.log("📤 Enviando respostas rápidas...", "info")
        self.atualizar_status(f"Enviando {total} respostas rápidas...")
        
        sucesso = 0
        with httpx.Client(headers=headers_echat2, timeout=30.0) as client:
            for idx, resposta in enumerate(resposta_rapida, 1):
                try:
                    client.post(
                        url=f"https://{cliente_echat2}.eassystems.com.br/respostasrapidas/addResRapida",
                        data={"nome": resposta["atalho"], "mensagem": resposta["mensagem"]},
                    )
                    sucesso += 1
                    if idx % 10 == 0:
                        self.log(f"✓ {idx}/{total} respostas enviadas")
                        self.atualizar_estatistica("respostas", sucesso)
                except httpx.HTTPError as e:
                    self.log(f"❌ Erro ao enviar resposta {idx}: {e}", "erro")
        
        self.log(f"✅ {sucesso}/{total} respostas rápidas migradas com sucesso!", "sucesso")
        self.atualizar_estatistica("respostas", sucesso)
    
    def migrar_classificacoes(self):
        self.log("🔍 Buscando classificações...", "info")
        self.atualizar_status("Buscando classificações...")
        
        page = 1
        classificacao = []
        
        with httpx.Client(headers=headers_echat, timeout=30.0) as client:
            while True:
                try:
                    params = {"searchParam": "", "pageNumber": page}
                    response = client.get(
                        f"https://{cliente_echat}api.eassystems.com.br/categoryCl/",
                        params=params,
                    )
                    response.raise_for_status()
                    data = response.json()
                    
                    for linha in data["categoryClassifications"]:
                        classificacao.append(linha["name"])
                    
                    self.log(f"📄 Página {page}: {len(data['categoryClassifications'])} classificações")
                    
                    if not data["hasMore"]:
                        break
                    
                    page += 1
                    
                except httpx.HTTPError as e:
                    self.log(f"❌ Erro na página {page}: {e}", "erro")
                    break
        
        self.atualizar_estatistica("classificacoes", len(classificacao))
        
        # Sub-classificações
        self.log("🔍 Buscando sub-classificações...", "info")
        page = 1
        sub_classificacao = []
        
        with httpx.Client(headers=headers_echat, timeout=30.0) as client:
            while True:
                try:
                    params = {"searchParam": "", "pageNumber": page}
                    response = client.get(
                        f"https://{cliente_echat}api.eassystems.com.br/subCategoryCl/",
                        params=params,
                    )
                    response.raise_for_status()
                    data = response.json()
                    
                    for linha in data["subCategoryClassifications"]:
                        sub_classificacao.append(linha["name"])
                    
                    self.log(f"📄 Página {page}: {len(data['subCategoryClassifications'])} sub-classificações")
                    
                    if not data["hasMore"]:
                        break
                    
                    page += 1
                    
                except httpx.HTTPError as e:
                    self.log(f"❌ Erro na página {page}: {e}", "erro")
                    break
        
        self.atualizar_estatistica("subclassificacoes", len(sub_classificacao))
        
        # Enviar classificações
        self.log("📤 Enviando classificações...", "info")
        sucesso_class = 0
        
        with httpx.Client(headers=headers_echat2, timeout=30.0) as client:
            for idx, linha in enumerate(classificacao, 1):
                try:
                    client.post(
                        url=f"https://{cliente_echat2}.eassystems.com.br/classificacao/addClassif",
                        data={"id_buscar_classif": "", "nome": linha},
                    )
                    sucesso_class += 1
                except httpx.HTTPError as e:
                    self.log(f"❌ Erro ao enviar classificação {idx}: {e}", "erro")
        
        # Enviar sub-classificações
        self.log("📤 Enviando sub-classificações...", "info")
        sucesso_sub = 0
        
        with httpx.Client(headers=headers_echat2, timeout=30.0) as client:
            for idx, linha in enumerate(sub_classificacao, 1):
                try:
                    client.post(
                        url=f"https://{cliente_echat2}.eassystems.com.br/classificacao/addSubClassif",
                        data={"id_buscar_subclassif": "", "nome_subclassif": linha},
                    )
                    sucesso_sub += 1
                except httpx.HTTPError as e:
                    self.log(f"❌ Erro ao enviar sub-classificação {idx}: {e}", "erro")
        
        self.log(f"✅ {sucesso_class} classificações migradas!", "sucesso")
        self.log(f"✅ {sucesso_sub} sub-classificações migradas!", "sucesso")
        self.atualizar_estatistica("classificacoes", sucesso_class)
        self.atualizar_estatistica("subclassificacoes", sucesso_sub)


if __name__ == "__main__":
    root = tk.Tk()
    app = EchatMigrationApp(root)
    root.mainloop()


"""
EXPEDIENTE
https://zapmed.eassystems.com.br/hrexpediente/addExpediente
id
nome_expediente=Teste
mensagem=Mensagem de teste


https://zapmed.eassystems.com.br/hrexpediente/addHrFunc
id_buscar
expediente=2
dia=segunda-feira
horainicio=07:00
horafim=18:00
msg=Mensagem de teste




https://agnusdeiapi.eassystems.com.br/expedient/1

"""


def expediente():
    id = 1 #Mudar aqui de acordo com https://echatapi.eassystems.com.br/expedient/1
    dias = [
        "segunda-feira",
        "terça-feira",
        "quarta-feira",
        "quinta-feira",
        "sexta-feira",
    ]
    horainicio = "07:00"
    horafim = "18:00"
    data = {}

    with httpx.Client(headers=headers_echat, timeout=30.0) as client:
        try:
            response = client.get(
                f"https://{cliente_echat}api.eassystems.com.br/expedient/{id}"
            )
            response.raise_for_status()
            data = response.json()

        except httpx.HTTPError as e:
            print(f"ERROR ao pegar os horario \n {e}")

    with httpx.Client(headers=headers_echat2, timeout=30.0) as client:
        try:
            response = client.post(
                f"https://{cliente_echat2}.eassystems.com.br/hrexpediente/addExpediente",
                data={
                    "id": "",
                    "nome_expediente": data["name"],
                    "mensagem": data["message"],
                },
            )
            for dia in dias:
                response = client.post(
                    f"https://{cliente_echat2}.eassystems.com.br/hrexpediente/addHrFunc",
                    data={
                        "id_buscar": "",
                        "expediente": 1,
                        "dia": dia,
                        "horainicio": horainicio,
                        "horafim": horafim,
                        "msg": data["message"],
                    },
                )
                response.raise_for_status()
        except httpx.HTTPError as e:
            print(f"ERROR ao inserir os horario \n {e}")


"""
FILAS
https://agnusdeiapi.eassystems.com.br/queue
LISTA DE JSON{
	"0": {
		"id": 3,
		"name": "✅ CATU",
		"color": "#d0021b",
		"greetingMessage": "{{name}}, você escolheu a opção ................, aguarde por favor que já iremos atendê-lo...",
		"timeIdlenessGren": 2,
		"timeIdlenessYellow": 4,
		"timeIdlenessOrange": 6,
		"timeIdlenessRed": 20,
		"timeOpeningGren": 5,
		"timeOpeningYellow": 10,
		"timeOpeningOrange": 15,
		"timeOpeningRed": 60,
		"expedientId": 1,
		"createdAt": "2024-09-23T14:45:43.000Z",
		"updatedAt": "2024-09-23T14:45:43.000Z"
	}
}



https://zapmed.eassystems.com.br/filas/addFila
id
nome_fila=Teste
cor=#617A8A
id_expediente=1
id_conexao=1
tipo_atendimento=0
tempoaberturaverde=5
tempoaberturaazul=10
tempoaberturalaranja=15
tempoociosidadeverde=2
tempoociosidadeazul=4
tempoociosidadelaranja=6
mensagem=TESTE
"""


"""
USUARIOS
https://agnusdeiapi.eassystems.com.br/users/?searchParam=&pageNumber=1
LISTA DE USUARIO
{
	"0": {
		"userStatus": "online",
		"name": "Samara",
		"id": 44,
		"email": "samarasantos@agnusdei.com.br",
		"profile": "user", | admin
		"createdAt": "2025-07-30T12:18:12.000Z",
		"allowNoQueue": 1,
		"allowViewCloseTickets": "all",
		"classificationPermission": "disabled", | optional | required ou S se for os dois
		"lastPresence": "2025-10-16T20:17:19.000Z",
		"tokenVersion": 48,
		"enableSignature": true,
		"allowSignature": true,
		"whatsappId": null,
		"queues": [
			{
				"id": 1,
				"name": "✅ EXAMES",
				"color": "#417505",
				"UserQueue": {
					"userId": 44,
					"queueId": 1,
					"createdAt": "2025-07-30T13:53:28.000Z",
					"updatedAt": "2025-07-30T13:53:28.000Z"
				}
			},
			{
				"id": 2,
				"name": "✅ CONSULTAS",
				"color": "#4a90e2",
				"UserQueue": {
					"userId": 44,
					"queueId": 2,
					"createdAt": "2025-07-30T13:53:28.000Z",
					"updatedAt": "2025-07-30T13:53:28.000Z"
				}
			},
			{
				"id": 3,
				"name": "✅ CATU",
				"color": "#d0021b",
				"UserQueue": {
					"userId": 44,
					"queueId": 3,
					"createdAt": "2025-07-30T13:53:28.000Z",
					"updatedAt": "2025-07-30T13:53:28.000Z"
				}
			},
			{
				"id": 4,
				"name": "✅ POJUCA",
				"color": "#d400ff",
				"UserQueue": {
					"userId": 44,
					"queueId": 4,
					"createdAt": "2025-07-30T13:53:28.000Z",
					"updatedAt": "2025-07-30T13:53:28.000Z"
				}
			}
		],
		"whatsapp": null
	}
}
COUNT:64
hasMore:True



https://zapmed.eassystems.com.br/usuarios/addUsuarios

id_usuario
id_permissao=3
id_conexao=1
fila[]=1
fila[]=2
fila[]=3
fila[]=4
fila[]=7
nps=1
email=Teste@teste.com.br
senha=Teste@123
nome=Teste
permitir_assinatura=1
permitir_sem_fila=1
permitir_exibir_fechar_tickets=all
permitir_exibir_tickets_pendentes=1
permitir_exportacao_ticket=0
permissao_classificacao=required
habilitar_assinatura=1
"""
