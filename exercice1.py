import re
import json

# Fonction pour parser les lignes de log et compter les codes de retour par adresse IP
def parse_log_file(log_file):
    logs = {}

    for line in log_file.split("\n"):
        log_entry = parse_log_line(line)

        if log_entry:
            ip = log_entry['ip']
            status_code = log_entry['status_code']

            if ip not in logs:
                logs[ip] = {}

            if status_code not in logs[ip]:
                logs[ip][status_code] = 0

            logs[ip][status_code] += 1

    return logs

# Fonction pour parser les lignes de log
def parse_log_line(line):
    # Définir le pattern regex pour parser les différentes parties du log
    pattern = r'^(\S+) (\S+) (\S+) \[(.*?)\] "(.*?)" (\d+) (\d+) "(.*?)" "(.*?)"$'
    match = re.match(pattern, line)

    if match:
        # Extraire les différentes parties du log
        ip = match.group(1)
        ident = match.group(2)
        user = match.group(3)
        timestamp = match.group(4)
        request = match.group(5)
        status_code = int(match.group(6))
        response_size = int(match.group(7))
        referer = match.group(8)
        user_agent = match.group(9)

        # Créer un dictionnaire avec les informations extraites
        log_entry = {
            'ip': ip,
            'ident': ident,
            'user': user,
            'timestamp': timestamp,
            'request': request,
            'status_code': status_code,
            'response_size': response_size,
            'referer': referer,
            'user_agent': user_agent
        }

        return log_entry
    else:
        return None

# Fonction pour écrire les données dans un fichier JSON
def write_data_to_json(data, output_file):
    with open(output_file, 'w') as file:
        json.dump(data, file)

# Exemple d'utilisation du script
log_data = """
81.249.97.13 - - [27/Apr/2022:06:58:22 +0000] "GET /list?ts=1651042697585 HTTP/1.1" 200 35 "http://localhost:3000/" "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:99.0) Gecko/20100101 Firefox/99.0"
176.139.4.215 - - [27/Apr/2022:06:58:26 +0000] "GET /list?ts=1651042702724 HTTP/1.1" 200 35 "http://localhost:3000/" "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:99.0) Gecko/20100101 Firefox/99.0"
176.139.4.215 - - [27/Apr/2022:06:58:26 +0000] "POST /send HTTP/1.1" 400 57 "http://localhost:3000/" "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:99.0) Gecko/20100101 Firefox/99.0"
176.139.4.215 - - [27/Apr/2022:06:58:27 +0000] "GET /list?ts=1651042706180 HTTP/1.1" 200 35 "http://localhost:3000/" "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:99.0) Gecko/20100101 Firefox/99.0"
81.249.97.13 - - [27/Apr/2022:06:58:28 +0000] "GET /list?ts=1651042702842 HTTP/1.1" 200 35 "http://localhost:3000/" "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:99.0) Gecko/20100101 Firefox/99.0"
176.139.4.215 - - [27/Apr/2022:06:58:31 +0000] "GET /list?ts=1651042707725 HTTP/1.1" 200 35 "http://localhost:3000/" "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:99.0) Gecko/20100101 Firefox/99.0"
"""

parsed_data = parse_log_file(log_data)
write_data_to_json(parsed_data, 'parsed_data.json')
