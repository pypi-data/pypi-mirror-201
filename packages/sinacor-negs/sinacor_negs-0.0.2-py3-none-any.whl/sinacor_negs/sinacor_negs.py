import pandas as pd
import numpy as np

from dataclasses import dataclass

from utils import drop_left_zeros_df

@dataclass
class Negs:
    header: pd.DataFrame()
    negs: pd.DataFrame()
    trailer: pd.DataFrame()
    account_more_than_seven_digits: bool

def read_negs_txt(path) -> Negs:

    _negs = Negs
    _negs.account_more_than_seven_digits = False

    file_txt = pd.read_csv(path)

    def get_header():
        header_txt = file_txt.columns[0]
        header = pd.DataFrame(index=[0])
        header['tipo_registro'] = header_txt[0:2]
        header['nome_arquivo'] = header_txt[2:10]
        header['codigo_arquivo'] = header_txt[2:6]
        header['codigo_usuario'] = header_txt[6:10]
        header['codigo_origem'] = header_txt[10:18]
        header['codigo_destino'] = header_txt[18:22]
        header['data_geracao'] = header_txt[22:30]
        header['data_pregao'] = header_txt[30:38]

        if header_txt[39:40] == 'S':
            _negs.account_more_than_seven_digits = True
            header['reserva'] = header_txt[39:200]
        else:
            _negs.account_more_than_seven_digits = False
            header['reserva'] = header_txt[38:200]

        header = drop_left_zeros_df(header)

        return header

    def get_negs():
        negs_txt = pd.Series(file_txt.iloc[:-1, 0])
        negs = pd.DataFrame(index=np.arange(len(negs_txt)))
        negs['tipo_registro'] = negs_txt.str[0:2]
        negs['numero_negocio_por_codigo_negociacao'] = negs_txt.str[2:9]
        negs['natureza_operacao'] = negs_txt.str[9:10]
        negs['codigo_negociacao'] = negs_txt.str[10:22]
        negs['tipo_mercado'] = negs_txt.str[22:25]
        negs['tipo_transacao'] = negs_txt.str[25:28]
        negs['nome_sociedade_emissora'] = negs_txt.str[28:40]
        negs['especificacao'] = negs_txt.str[40:50]
        negs['quantidade_negocio'] = negs_txt.str[50:61].str.lstrip("0").astype(int)
        negs['preco_negocio'] = negs_txt.str[61:72].str.lstrip("0").astype(float).div(100)
        negs['codigo_usuario_contraparte'] = negs_txt.str[72:77]
        negs['prazo_vencimento'] = negs_txt.str[77:80]
        negs['tipo_liquidacao'] = negs_txt.str[80:81]
        negs['hora_minuto_negocio'] = negs_txt.str[81:86]
        negs['situacao_negocio'] = negs_txt.str[86:87]
        negs['codigo_objeto_papel'] = negs_txt.str[87:99]
        negs['codigo_cliente'] = negs_txt.str[99:106]
        negs['digito_cliente'] = negs_txt.str[106:107]
        negs['codigo_isin'] = negs_txt.str[107:119]
        negs['distribuicao_isin'] = negs_txt.str[119:122]
        negs['fator_cotacao_negocio'] = negs_txt.str[122:129]
        negs['preco_exercicio_serie'] = negs_txt.str[129:140]
        negs['indicador_after_market'] = negs_txt.str[140:141]
        negs['reserva1'] = negs_txt.str[141:149]
        negs['prazo_vencimento_termo'] = negs_txt.str[149:154]
        negs['reserva2'] = negs_txt.str[154:167]
        negs['bolsa_movimento'] = negs_txt.str[167:168]
        negs['tipo_liquidacao'] = negs_txt.str[168:169]
        negs['prazo_liquidacao'] = negs_txt.str[169:172].str.lstrip("0").astype(int)
        negs['reserva3'] = negs_txt.str[172:198]
        negs['tipo_operacao_recompra'] = negs_txt.str[200:201]
        
        if _negs.account_more_than_seven_digits:
            negs['fase_grupo_instrumento'] = negs_txt.str[172:175]
            negs['fase_sessao_negociacao'] = negs_txt.str[175:176]
            negs['estado_instrumento'] = negs_txt.str[176:180]
            negs['codigo_bdi'] = negs_txt.str[180:184]
            negs['codigo_cliente'] = negs_txt.str[184:193]
            negs['reserva3'] = negs_txt.str[193:200]  

        negs = drop_left_zeros_df(negs)

        return negs

    def get_trailer():
        trailer_txt = file_txt.iloc[-1].values[0]
        trailer = pd.DataFrame(index=[0])
        trailer['tipo_registro'] = trailer_txt[0:2]
        trailer['nome_arquivo'] = trailer_txt[2:10]
        trailer['codigo_arquivo'] = trailer_txt[2:6]
        trailer['codigo_usuario'] = trailer_txt[6:10]
        trailer['codigo_origem'] = trailer_txt[10:18]
        trailer['codigo_destino'] = trailer_txt[18:22]
        trailer['data_geracao_arquivo'] = trailer_txt[22:30]
        trailer['total_registros_gerados'] = trailer_txt[30:39]
        trailer['reserva'] = trailer_txt[39:200]
        trailer = drop_left_zeros_df(trailer)
        return trailer

    _negs.header = get_header()
    _negs.negs = get_negs()
    _negs.trailer = get_trailer()

    return _negs