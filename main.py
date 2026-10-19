import os
import csv
from datetime import datetime

from bird_model import analyze_bird
from database import (
    create_table,
    save_result,
    get_history,
    search_bird,
    delete_result
)
from bird_info import get_bird_info


CSV_FILE = "bird_analysis.csv"


def save_to_csv(
    image_name,
    predicted_species,
    confidence,
    description
):
    file_exists = os.path.exists(CSV_FILE)

    with open(
        CSV_FILE,
        "a",
        newline="",
        encoding="utf-8-sig"
    ) as file:

        writer = csv.writer(file)

        if not file_exists:
            writer.writerow([
                "image_name",
                "predicted_species",
                "confidence",
                "analysis_date",
                "description"
            ])

        writer.writerow([
            image_name,
            predicted_species,
            confidence,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            description
        ])


def analyze_image():
    image_path = input("Введіть шлях до фото: ")

    if not os.path.exists(image_path):
        print("Файл не знайдено.")
        return

    extension = os.path.splitext(image_path)[1].lower()

    if extension not in [".jpg", ".jpeg", ".png"]:
        print("Підтримуються тільки JPG, JPEG та PNG.")
        return

    print()
    print("Аналіз фотографії...")

    try:
        results = analyze_bird(image_path)

        print()
        print(" TOP 3 RESULTS ")

        for i, result in enumerate(results, start=1):
            print()
            print("Варіант", i)
            print("Bird:", result["label"])
            print(
                "Confidence:",
                round(result["score"] * 100, 2),
                "%"
            )

        best_result = results[0]

        species = best_result["label"]
        confidence = best_result["score"]

        info = get_bird_info(species)

        print()
        print(" BIRD INFO ")
        print("Species:", species)
        print("Description:", info["description"])
        print("Extra info:", info["extra_info"])

        image_name = os.path.basename(image_path)

        save_result(
            image_name,
            species,
            confidence,
            info["description"],
            info["extra_info"]
        )

        save_to_csv(
            image_name,
            species,
            confidence,
            info["description"]
        )

        print()
        print("Результат збережено в базу даних і CSV.")

    except Exception as error:
        print("Помилка аналізу:")
        print(error)


def show_history():
    rows = get_history()

    print()
    print(" ІСТОРІЯ ")

    if not rows:
        print("Історія порожня.")
        return

    for row in rows:
        print()
        print("ID:", row[0])
        print("Image:", row[1])
        print("Species:", row[2])
        print(
            "Confidence:",
            round(row[3] * 100, 2),
            "%"
        )
        print("Date:", row[4])
        print("------------------------")


def find_bird():
    name = input("Введіть назву птаха: ")

    rows = search_bird(name)

    if not rows:
        print("Птаха не знайдено.")
        return

    print()
    print(" РЕЗУЛЬТАТИ ПОШУКУ ")

    for row in rows:
        print()
        print("ID:", row[0])
        print("Image:", row[1])
        print("Species:", row[2])
        print(
            "Confidence:",
            round(row[3] * 100, 2),
            "%"
        )
        print("Date:", row[4])
        print("Description:", row[5])
        print("Extra info:", row[6])
        print("------------------------")


def remove_record():
    record_id = input("Введіть ID запису: ")

    if not record_id.isdigit():
        print("ID повинен бути числом.")
        return

    deleted = delete_result(int(record_id))

    if deleted > 0:
        print("Запис видалено.")
    else:
        print("Запис з таким ID не знайдено.")


def show_statistics():
    rows = get_history()

    if not rows:
        print("Даних для статистики немає.")
        return

    total = len(rows)

    species_count = {}

    highest = rows[0]
    lowest = rows[0]

    for row in rows:
        species = row[2]
        confidence = row[3]

        if species not in species_count:
            species_count[species] = 0

        species_count[species] += 1

        if confidence > highest[3]:
            highest = row

        if confidence < lowest[3]:
            lowest = row

    most_common_species = max(
        species_count,
        key=species_count.get
    )

    print()
    print(" STATISTICS ")

    print("Проаналізовано фото:", total)

    print(
        "Найчастіший вид:",
        most_common_species
    )

    print(
        "Кількість:",
        species_count[most_common_species]
    )

    print()
    print("Найвища впевненість:")
    print("Species:", highest[2])
    print(
        "Confidence:",
        round(highest[3] * 100, 2),
        "%"
    )

    print()
    print("Найнижча впевненість:")
    print("Species:", lowest[2])
    print(
        "Confidence:",
        round(lowest[3] * 100, 2),
        "%"
    )


def main():
    create_table()

    while True:
        print()

        print("          AI BIRD LAB")


        print("1. Аналіз фотографії")
        print("2. Історія аналізів")
        print("3. Пошук птаха")
        print("4. Видалити запис")
        print("5. Статистика")
        print("0. Вихід")

        choice = input("Оберіть пункт: ")

        if choice == "1":
            analyze_image()

        elif choice == "2":
            show_history()

        elif choice == "3":
            find_bird()

        elif choice == "4":
            remove_record()

        elif choice == "5":
            show_statistics()

        elif choice == "0":
            print("Програму завершено.")
            break

        else:
            print("Невірний пункт меню.")


main()