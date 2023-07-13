import warnings

import pandas as pd
from importer import import_data
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier


def classifier(user, password, host, port, database):

    # Wyłączenie wyświetlania ostrzeżeń
    warnings.filterwarnings('ignore')

    # Import danych
    (df, challenges) = import_data(user, password, host, port, database)

    # Podział zbioru na zmienne niezależne i zmienną zależną
    X = df[['time_dict', 'hobby_dict', 'knowledge_dict']]
    y = df['challenge_type']

    # Podział na zbiór treningowy i testowy i trening zbioru
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

    clf = DecisionTreeClassifier().fit(X_train, y_train)

    # Deklaracja zmiennych binarnych, dzięki którym po wpisaniu nieprawidłowej wartości program nie wyrzuci błędu
    verifier_time = verifier_hobby = verifier_knowledge = verifier_n = False

    # Zbieranie preferencji - docelowo zastąpione przez listę dropdown. W nawiasie dostępne opcje
    while not verifier_time:
        time = input("Podaj preferowaną porę dnia (Rano, W południe, Wieczór, Noc): ")
        if time in ['Rano', 'W południe', 'Wieczór', 'Noc']:
            # Znajdowanie wartości słownikowej dla podanej preferencji - potrzebna jest wartość liczbowa
            time_dict = df.loc[df['time'] == time, 'time_dict'].iloc[0]
            verifier_time = True
        else:
            print("Podaj właściwą porę")

    while not verifier_hobby:
        hobby = input("Podaj hobby (Jedzenie, Moda, Modelarstwo, Motoryzacja, RTV, Sport, Turystyka, Wędkarstwo): ")
        if hobby in ['Jedzenie', 'Moda', 'Modelarstwo', 'Motoryzacja', 'RTV', 'Sport', 'Turystyka', 'Wędkarstwo']:
            hobby_dict = df.loc[df['hobby'] == hobby, 'hobby_dict'].iloc[0]
            verifier_hobby = True
        else:
            print("Podaj właściwe hobby")

    while not verifier_knowledge:
        knowledge = input("Podaj swój poziom wiedzy (Ekspert, Początkujący, Średniozaawansowany, Zaawansowany): ")
        if knowledge in ['Ekspert', 'Początkujący', 'Średniozaawansowany', 'Zaawansowany']:
            knowledge_dict = df.loc[df['knowledge'] == knowledge, 'knowledge_dict'].iloc[0]
            verifier_knowledge = True
        else:
            print("Podaj właściwy poziom wiedzy")

    # Ustawianie liczby otrzymywanych wyników
    while not verifier_n:
        n = input("Podaj liczbę zwracanych wyników: ")
        try:
            n = int(n)
            verifier_n = True
        except TypeError:
            print("Nieprawidłowa liczba")

    # Stworzenie profilu na podstawie podanych preferencji
    X_profile = [[time_dict, hobby_dict, knowledge_dict]]

    # Wyliczenie prawdopodobieństwa dla danego typu zadania
    y_profile = clf.predict_proba(X_profile)

    # Dołączenie prawdopodobieństwa do tabeli z listą zadań
    percentage = challenges.merge(pd.DataFrame(list(zip(clf.classes_[1:7], y_profile[0]))
                                              , columns=['challenge_type', 'probability']), on='challenge_type', how='left')

    # Konwersja prawdopodobieństwa na wartość procentową
    percentage['percent'] = percentage['probability'].transform(lambda x: "{:.2%}".format(x))

    # Sortowanie danych
    percentage_sorted = percentage.sort_values(by=['probability'], ascending=False).head(n)

    # Wyświetlenie wyników - trzeba było zrobić w dwóch krokach, ponieważ program nie potrafił posortować po procentach
    print(percentage_sorted.drop(['probability'], axis=1))
