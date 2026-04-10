'''
Retorna a seleção de fragmentos com base nos cenários apresentados

Diaut
04/2026
'''
import subprocess
import os


cenario = {
    "servico": {
        "nome": "Serviço",
        "opcoes": None,
        "selecao": "TPU"
    },
    "canal": {
        "nome": "Canal",
        "opcoes": [
            {"opcao":"1", "texto": "Todos exceto SEC"},
            {"opcao":"2", "texto": "SEC"},
        ],
        "selecao": None
    },
    "requerente": {
        "nome": "Requerente",
        "opcoes": [
            {"opcao":"1", "texto": "Titular"},
            {"opcao":"2", "texto": "Procurador"},
            {"opcao":"3", "texto": "RL"}
        ],
        "selecao": None
    },
    "motivo": {
        "nome": "Motivo",
        "opcoes": [
            {"opcao":"1", "texto": "Óbito"}
        ],
        "selecao": None
    },
    "precedido": {
        "nome": "Precedido",
        "opcoes": [
            {"opcao":"1", "texto": "Sim"},
            {"opcao":"2", "texto": "Não"}
        ],
        "selecao": None
    },
    "relacao": {
        "nome": "Relação",
        "opcoes": [
            {"opcao":"1", "texto": "Casado"},
            {"opcao":"2", "texto": "Companheiro"},
            {"opcao":"3", "texto": "Filho menor"},
            {"opcao":"4", "texto": "Filho maior com deficiência"},
            {"opcao":"5", "texto": "Filho maior com invalidez"},
            {"opcao":"6", "texto": "Pais"}
        ],
        "selecao": None
    },
    "situacao": {
        "nome": "Situação",
        "opcoes": [
            {"opcao":"1", "texto": "Há mais de 2 anos"},
            {"opcao":"2", "texto": "Há menos de 2 anos com UE anterior"},
            {"opcao":"3", "texto": "Há menos de 2 anos sem UE anterior"}
        ],
        "selecao": None
    },
    "outros_dependentes": {
        "nome": "Outros dependentes",
        "opcoes": [
            {"opcao":"1", "texto": "Sem"}
        ],
        "selecao": None
    },
    "acumula": {
        "nome": "Acumula",
        "opcoes": [
            {"opcao":"1", "texto": "Sim"},
            {"opcao":"2", "texto": "Não"},
            {"opcao":"3", "texto": "Sim/Não"}
        ],
        "selecao": None
    },
    "morte_por_acidente": {
        "nome": "Morte por acidente",
        "opcoes": [
            {"opcao":"1", "texto": "Sim"},
            {"opcao":"2", "texto": "Não"}
        ],
        "selecao": None
    },
    "anexos": {
        "nome": "Anexos",
        "opcoes": [
            {"opcao":"1", "texto": "Documentos titular"},
            {"opcao":"2", "texto": "Documentos RL"},
            {"opcao":"3", "texto": "Tutela/Curatela/Guarda"},
            {"opcao":"4", "texto": "Documentos procurador"},
            {"opcao":"5", "texto": "Documentos dependentes"},
            {"opcao":"6", "texto": "Certidão de óbito"},
            {"opcao":"7", "texto": "Certidão de casamento"},
            {"opcao":"8", "texto": "Autodeclaração"},
            {"opcao":"9", "texto": "Comprovantes de união estável"},
            {"opcao":"10", "texto": "Declaração acumulação RPPS"},
            {"opcao":"11", "texto": "CTPS"},
            {"opcao":"12", "texto": "Comprovante serviço público"},
            {"opcao":"14", "texto": ""},
            {"opcao":"13", "texto": "Carnês"},
            {"opcao":"15", "texto": "Outros documentos"},
            {"opcao":"1480", "texto": "Documentos interessado"},
            {"opcao":"1482", "texto": "Documentos grupo familiar"}
        ],
        "selecao": []
    }
}


# Monta o cenário conforme as seleções do usuário (input)
for chave, item in cenario.items():

    escolha = ""

    if item['nome'] == "Serviço":
        escolha = input(f"{item['nome']} (Enter para TPU): ")
        if escolha != "":
            item["selecao"] = escolha

    if item['nome'] != "Anexos" and item['nome'] != "Serviço":
        escolha = input(f"{item['nome']} ({' | '.join([f'{opcao['opcao']} - {opcao['texto']}' for opcao in item['opcoes']])}): ")
        item["selecao"] = None if escolha == "" else escolha

    if item['nome'] == "Anexos":
        print(f"{item['nome']}")
        print('\n'.join([f"{opcao['opcao']} - {opcao['texto']}" for opcao in item['opcoes']]))
        escolha = input(f"\nDigite os números dos anexos separados por vírgula (deixe em branco para nenhum):")
        #item["selecao"] = None if escolha == "" else int(escolha)
        item["selecao"] = [] if escolha == "" else [int(x.strip()) for x in escolha.split(",")]


# Variáveis para facilitar o entendimento do código
canal = cenario["canal"]["selecao"]
requerente = cenario["requerente"]["selecao"]
motivo = cenario["motivo"]["selecao"]
precedido = cenario["precedido"]["selecao"]
relacao = cenario["relacao"]["selecao"]
situacao = cenario["situacao"]["selecao"]
outros_dependentes = cenario["outros_dependentes"]["selecao"]
acumula = cenario["acumula"]["selecao"]
anexos_cenario = cenario["anexos"]["selecao"]
morte_acidente = cenario["morte_por_acidente"]["selecao"]


# Formação do nome do cenário
nome_cenario = f"{cenario['servico']['selecao']}"
nome_cenario += " - "

for chave, item in cenario.items():

    if item['nome'] != "Anexos" and item['nome'] != "Serviço":
        if item['selecao']:
            # Traz o nome do item do cenário e o texto selecionado
            nome_cenario += f"{item['nome']} {next(op["texto"] for op in item["opcoes"] if op["opcao"] == item["selecao"])}"
            nome_cenario += " - "

    if item['nome'] == "Anexos":

        anexos = "0" if len(item['selecao']) == 0 else [an for an in item['selecao']]
        anexos = ', '.join(map(str, anexos))
        nome_cenario += f"{item['nome']} {anexos}"

fragmentos = []

# Mensagem inicial, sempre presente
fragmentos.append("INTROD_PADRAO")


##### Fragmentos intermediários, conforme os cenários #####

## Requerente ##
if requerente == 1:
    if relacao not in [3, 4, 5, 6] and 5 not in anexos_cenario:
        fragmentos.append("IDENT_INTER")
elif requerente == 2:
    fragmentos.append("PROCURACAO")
    fragmentos.append("IDENT_PROCUR")
    fragmentos.append("T_RESP_PROC")
    if relacao != 3 and 5 not in anexos_cenario:
        fragmentos.append("IDENT_INTER")
elif requerente == 3:
    fragmentos.append("IDENT_RL")
    fragmentos.append("REPRES_LEGAL")
    fragmentos.append("TERMO_RESPONS")
fragmentos.append("IDENT_INST_21")

## Motivo ##
if motivo == 1:
    if not 6 in anexos_cenario:
        fragmentos.append("FG_OBITO")

## Relação ##
if relacao == 1:
    if not 7 in anexos_cenario:
        fragmentos.append("CERT_CASAM_21")
elif relacao == 2:
    if not 9 in anexos_cenario:
        fragmentos.append("PROVA_UE_21")
elif relacao in [3, 4, 5]:
    fragmentos.append("IDENT_FILHOS")
elif relacao == 6:
    fragmentos.append("IDENT_PAIS_21")
    fragmentos.append("DEPEND_ECON_21")
    fragmentos.append("DECL_INEX_DEP")

## Situação ##
if situacao == 2:
    fragmentos.append("UE_ANTES_CAS_21")

## Precedido ##
if precedido == 2:
    fragmentos.append("CTPS_INSTIT_21")
    fragmentos.append("VINCULOS")

## Acumula ##
if acumula == 1 or acumula == 3:
    fragmentos.append("DECL_RPPS2")

## Morte por acidente ##
if morte_acidente == 1:
    fragmentos.append("OBITO_ACIDENTE")


# Mensagem final, sempre presente
fragmentos.append("CONC_PADRAO")


# Exibe a lista de fragmentos
counter = 1
output = ""

# Calcula o comprimento máximo do texto para alinhamento da tabulação
max_len = max(len(fragmento) for fragmento in fragmentos)

for fragmento in fragmentos:
    if fragmento != "":  # Pula as linhas vazias
        output += f"{fragmento:<{max_len}}\t{counter}\n"
        counter += 1
    else:
        output += "\n"

# Relaciona os nomes dos anexos selecionados
if len(cenario["anexos"]["selecao"]) > 0:
    output += f"\nAnexos:\n"
    for num_anexo in cenario["anexos"]["selecao"]:
        texto = next(
            (op["texto"] for op in cenario["anexos"]["opcoes"] if op["opcao"] == str(num_anexo)),
            "Anexo não encontrado"
        )
        output += f" • {texto}\n"
        
# Inclui o nome do cenário gerado
output += f"\nNome do cenário gerado:\n{nome_cenario}"

# Exibe o resultado no Notepad++
output_file = "fragmentos_output.txt"
with open(output_file, "w", encoding="utf-8") as f:
    f.write(output)

notepad_path = r"C:\Program Files\Notepad++\notepad++.exe"
if os.path.exists(notepad_path):
    subprocess.run([notepad_path, output_file])

print("Resultado exibido no Notepad++")

# Para exibição em tela (alternativa ao Notepad++)
# print("\n\nFragmentos:")
# print(output)
