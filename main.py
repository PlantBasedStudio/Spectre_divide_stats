import json


def load_data(file_name="player_stats.json"):
    try:
        with open(file_name, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {} 


def save_data(data, file_name="player_stats.json"):
    with open(file_name, "w") as file:
        json.dump(data, file, indent=4)


def add_game(data, map_name, sponsor, result, kills, deaths, assists):
    key = f"{map_name}-{sponsor}"
    if key not in data:
        data[key] = {"wins": 0, "games": 0, "kills": 0, "deaths": 0, "assists": 0}
    
    data[key]["games"] += 1
    if result == "win":
        data[key]["wins"] += 1
    data[key]["kills"] += kills
    data[key]["deaths"] += deaths
    data[key]["assists"] += assists


def calculate_stats(data):
    print("\nPerformance par map et sponsor :")
    for key, stats in data.items():
        winrate = (stats["wins"] / stats["games"]) * 100 if stats["games"] > 0 else 0
        kda = f"{stats['kills']}/{stats['deaths']}/{stats['assists']}"
        print(f"Map-Sponsor: {key}, Winrate: {winrate:.2f}%, KDA: {kda}, Parties jouées: {stats['games']}")


def calculate_global_kda(data):
    total_kills, total_deaths, total_assists, total_games = 0, 0, 0, 0

    for stats in data.values():
        total_kills += stats['kills']
        total_deaths += stats['deaths']
        total_assists += stats['assists']
        total_games += stats['games']

    if total_games > 0:
        avg_kills = total_kills / total_games
        avg_deaths = total_deaths / total_games
        avg_assists = total_assists / total_games
        print(f"\nRatio moyen sur toutes les parties (K/D/A) : {avg_kills:.2f}/{avg_deaths:.2f}/{avg_assists:.2f}")
    else:
        print("\nAucune partie enregistrée.")


def input_new_game():
    maps = ["mill", "commons", "metro", "skyway"]
    sponsors = ["Pinnacle", "morgen", "bloom", "ryke", "vector", "ghost", "muu", "umbra"]

    print("\nChoisissez une map :")
    for i, map_name in enumerate(maps, 1):
        print(f"{i}. {map_name}")
    map_choice = int(input("Entrez le numéro de la map : ")) - 1
    map_name = maps[map_choice]

    print("\nChoisissez un sponsor :")
    for i, sponsor_name in enumerate(sponsors, 1):
        print(f"{i}. {sponsor_name}")
    sponsor_choice = int(input("Entrez le numéro du sponsor : ")) - 1
    sponsor = sponsors[sponsor_choice]

    result = input("Résultat de la partie (win/lose) : ").strip().lower()
    while result not in ["win", "lose"]:
        result = input("Résultat invalide. Entrez 'win' ou 'lose' : ").strip().lower()

    kills = int(input("Nombre de kills : "))
    deaths = int(input("Nombre de deaths : "))
    assists = int(input("Nombre d'assists : "))

    return map_name, sponsor, result, kills, deaths, assists


def main():

    data = load_data()
    

    while True:
        print("\n1. Ajouter une nouvelle partie")
        print("2. Voir les statistiques actuelles (par map et sponsor)")
        print("3. Voir le ratio moyen sur toutes les parties")
        print("4. Quitter")
        choice = input("Entrez votre choix : ").strip()

        if choice == "1":
            map_name, sponsor, result, kills, deaths, assists = input_new_game()
            add_game(data, map_name, sponsor, result, kills, deaths, assists)
            save_data(data)
        elif choice == "2":
            calculate_stats(data)
        elif choice == "3":
            calculate_global_kda(data)
        elif choice == "4":
            save_data(data)
            print("Au revoir!")
            break
        else:
            print("Choix invalide, veuillez réessayer.")

if __name__ == "__main__":
    main()
