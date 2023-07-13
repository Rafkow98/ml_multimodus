import pandas as pd
from parser import parse_string


def import_data(user, password, host, port, database):
    credentials = f"mariadb://{user}:{password}@{host}:{port}/{database}"

    # Dane preferencji - zapytanie zwraca ID rekordu, ID użytkownika, ID wyzwania, typ wyzwania
    # oraz zmienne powstałe na podstawie kolumny value - zmienne z końcówką _dict zawierają wartość słownikową,
    # z kolei kolumny bez tej końcówki to nazwy preferencji
    df = pd.read_sql("""SELECT cap1.id, cap1.user_id, cap1.challenge_id, s1.SLO_NAZWA AS 'challenge_type'
    , cap2.value AS 'time_dict', cap3.value AS 'hobby_dict', cap4.value AS 'knowledge_dict'
    , s2.SLO_NAZWA AS 'time', s3.SLO_NAZWA AS 'hobby', s4.SLO_NAZWA AS 'knowledge'
    FROM lc_challenge_action_preference cap1
    LEFT JOIN lc_slownik s1 ON cap1.challenge_type = s1.SLO_ID 
    LEFT JOIN lc_challenge_action_preference cap2 ON cap1.id = cap2.id AND cap1.type = 30005040
    LEFT JOIN lc_slownik s2 ON cap2.value = s2.SLO_ID 
    LEFT JOIN lc_challenge_action_preference cap3 ON cap1.id = cap3.id AND cap1.type = 30005041
    LEFT JOIN lc_slownik s3 ON cap3.value = s3.SLO_ID 
    LEFT JOIN lc_challenge_action_preference cap4 ON cap1.id = cap4.id AND cap1.type = 30005042
    LEFT JOIN lc_slownik s4 ON cap4.value = s4.SLO_ID 
    WHERE cap1.challenge_id IS NOT NULL AND COALESCE(cap1.ssr_deleted, 0) = 0""", con=credentials)

    # Dane 10 losowych zadań
    challenge = pd.read_sql("""SELECT id, s.SLO_NAZWA AS 'challenge_type', c.name AS 'challenge_name' FROM lc_challenge c 
    LEFT JOIN lc_slownik s ON c.challenge_type = s.SLO_ID
    ORDER BY RAND() LIMIT 10""", con=credentials)

    # Zmiana ciągów tekstowych, które mogą się nieprawidłowo przekonwertować podczas ściągania i dodawania do dataframe
    parse_string(df)

    return df, challenge
