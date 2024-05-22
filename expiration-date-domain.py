import whois
import datetime
import sys

dominios = ["youtube.cl", "youtube.com.br", "youtube.us", "youtube.uk", "youtube.co", "youtube.com", "youtube.me"]

def obter_data_expiracao(domain):
    try:
        w = whois.whois(domain)
        expiry_date = w.expiration_date
        if isinstance(expiry_date, list):
            expiry_date = expiry_date[0]
        return str(expiry_date)
    except Exception as e:
        print(f"Error fetching domain expiry for {domain}: {e}", file=sys.stderr)
        return None

# Função para verificar se a expiração está próxima
def expiracao_proxima(data_expiracao_str, dias_limite=90):
    if data_expiracao_str:
        try:
            # Converte a string de data em um objeto datetime
            data_expiracao = datetime.datetime.strptime(data_expiracao_str, '%Y-%m-%d')
        except ValueError:
            try:
                data_expiracao = datetime.datetime.strptime(data_expiracao_str, '%Y-%m-%d %H:%M:%S')
            except ValueError:
                print(f"Formato de data desconhecido: {data_expiracao_str}", file=sys.stderr)
                return False
        hoje = datetime.datetime.now()
        dias_para_expiracao = (data_expiracao - hoje).days
        return dias_para_expiracao <= dias_limite
    return False

# Loop para verificar cada domínio na lista
for dominio in dominios:
    data_expiracao_str = obter_data_expiracao(dominio).split(" ")[0]
    
    if data_expiracao_str:
        proxima = expiracao_proxima(data_expiracao_str)
        print(f"Domínio: {dominio}, Data de Expiração: {data_expiracao_str}, Expiração Próxima: {proxima}")
    else:
        print(f"Domínio: {dominio}, Data de Expiração: Não Disponível")
