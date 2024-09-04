import pdfkit
from .models import Usuario, AguaIngerida
from django.conf import settings
import os
from django_q.tasks import async_task # Para comunicação assincrona


def gerar_pdf_historico_usuario(usuario_id):
    try:
        usuario = Usuario.objects.get(id=usuario_id)
        historico = AguaIngerida.objects.filter(usuario=usuario)

        # Gerar o conteúdo do PDF com HTML e estilos básicos
        conteudo_pdf = f"""
        <!DOCTYPE html>
        <html lang="pt-br">
        <head>
            <meta charset="UTF-8">
            <meta http-equiv="X-UA-Compatible" content="IE=edge">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Histórico de Consumo de Água</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    margin: 20px;
                    padding: 20px;
                }}
                h1 {{
                    text-align: center;
                    color: #333;
                }}
                table {{
                    width: 100%;
                    border-collapse: collapse;
                    margin-top: 20px;
                }}
                th, td {{
                    padding: 10px;
                    border: 1px solid #ddd;
                    text-align: left;
                }}
                th {{
                    background-color: #f4f4f4;
                }}
            </style>
        </head>
        <body>
            <h1>Histórico de Consumo de Água do Usuário {usuario.nome}</h1>
            <table>
                <thead>
                    <tr>
                        <th>Data</th>
                        <th>Quantidade</th>
                    </tr>
                </thead>
                <tbody>
        """

        # Adicionar os dados de histórico ao conteúdo
        for registro in historico:
            conteudo_pdf += f"""
                <tr>
                    <td>{registro.data}</td>
                    <td>{registro.qtd_agua}ml</td>
                </tr>
            """

        conteudo_pdf += """
                </tbody>
            </table>
        </body>
        </html>
        """

        # Definir o caminho para salvar o PDF
        caminho_pdf = os.path.join(settings.BASE_DIR, f"historico_{usuario.id}.pdf")

        # Gerar o PDF com pdfkit
        pdfkit.from_string(conteudo_pdf, caminho_pdf)
        print("PDF gerado com sucesso!")

        return caminho_pdf
    except Usuario.DoesNotExist:
        return "Usuário não encontrado"
    except Exception as e:
        return str(e)

def tarefa_de_teste():
    print("Tarefa de teste executada!")
    return("Tarefa Concluída !!")



