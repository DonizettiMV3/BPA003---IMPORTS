import mysql.connector
from database.connection import create_connection

def Post_updateDuplicate(hora):

    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute(f"""
                UPDATE tbl_input_processos tip
                INNER JOIN tbl_dados_processos tdp 
                ON
                    tip.numero_precatorio = tdp.processo_comunicacao 
                SET 
                    tip.status = 'Não importado',
                    tip.execucao_syspax= 'Existente fila Syspax',
                    tip.data_importacao = '{hora}'
                    WHERE 
                        tip.numero_processo = tdp.NUMERO_PROCESSO
                        AND tip.nome_requerente = tdp.REQUERENTE
                        AND tip.numero_precatorio = tdp.processo_comunicacao
                        AND tip.documento_requerente = tdp.DOCUMENTO
                        AND tip.valor_espelho_principal = tdp.valor_solicitado;
                """)
        
    cursor.close()
    conn.close()

def Post_InsertDadosProcessos(hora, id_arquivo, nome_arquivo):

    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute(f"""
                INSERT INTO tbl_dados_processos (
                    processo_comunicacao,
                    procedimento,
                    numero,
                    numero_cnj,
                    data_protocolo_trf,
                    juizo_de_origem,
                    processos_originarios,
                    requerido,
                    requerentes,
                    advogado,
                    data_da_conta_de_liquidacao,
                    valor_solicitado,
                    tentativas_busca_trf3,
                    status,
                    descricao_status,
                    horario_execucao,
                    agent_trf3,
                    NUMERO_PROCESSO,
                    ASSUNTO,
                    REQUERENTE,
                    DOCUMENTO,
                    PARTICIPANTES,
                    DATA_PROCESSAMENTO,
                    STATUS_PROCESSAMENTO,
                    DRSCRICAO_STATUS_PROCESSAMENTO
                    )
                SELECT
                    tipt.numero_precatorio,
                    tipt.tipo_processo,
                    '-',
                    '-',
                    tipt.data_autuacao,
                    tipt.sigla_tribunal,
                    tipt.processos_originarios,
                    tipt.nome_requerido,
                    tipt.nome_requerente,
                    '-',
                    tipt.data_base_valor_espelho_principal,
                    tipt.valor_espelho_principal,
                    '0',
                    'IMPORTADO - Syspax',
                    'Processo enviado pelo usuário via Syspax',
                    '{hora}',
                    'Syspax - Importação',
                    tipt.numero_processo,
                    tipt.assunto,
                    tipt.nome_requerente,
                    tipt.documento_requerente,
                    advogados,
                    '{hora}',
                    'IMPORTADO - Syspax',
                    '-'
                FROM tbl_input_processos tipt
                INNER JOIN tbl_input_arquivos tia 
                ON
                    tia.nome_arquivo = tipt.nome_arquivo_importacao 
                LEFT JOIN tbl_dados_processos tip
                ON 
                    tip.processo_comunicacao = tipt.numero_precatorio
                WHERE 
                    (tia.id='{id_arquivo}' AND tia.nome_arquivo ='{nome_arquivo}') AND tipt.id  NOT IN (SELECT tipt.id   
							        FROM tbl_dados_processos tdp 
                                        WHERE tdp.processo_comunicacao  = tipt.numero_precatorio  
                                        AND tdp.REQUERENTE   = tipt.nome_requerente 
                                        AND tdp.valor_solicitado = tipt.valor_espelho_principal
                                        AND tdp.DOCUMENTO = tipt.documento_requerente );
                """)
        
    cursor.close()
    conn.close()


def Post_SelectDados(nome_arquivo):

    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute(f"""
                SELECT COUNT(tdp.id) FROM tbl_dados_processos tdp 
                INNER JOIN tbl_input_processos tip 
                ON 
                   tdp.processo_comunicacao = tip.numero_precatorio 
                WHERE
                    tdp.REQUERENTE = tip.nome_requerente 
                AND
                    tdp.data_protocolo_trf = tip.data_autuacao 
                AND 
                   tdp.valor_solicitado = tip.valor_espelho_principal 
                AND 
                   tdp.NUMERO_PROCESSO = tip.numero_processo 
                AND 
                   tip.nome_arquivo_importacao ='{nome_arquivo}'
                """)
    
    data = cursor.fetchall()
    
    cursor.close()
    conn.close()


    return data