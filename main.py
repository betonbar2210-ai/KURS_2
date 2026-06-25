from src.airplane import Airplane
from src.api_client import APIAdapter
from src.utils import JSONSaver


def user_interaction():
    api_client = APIAdapter()
    json_saver = JSONSaver()

    print("\n=== Система мониторинга самолётов ===")

    while True:
        country = input("Введите название страны (на английском) для получения данных: ").strip()
        if not country:
            print("Страна не может быть пустой.")
            continue

        airplanes = []

        try:
            print(f"Ищем координаты для {country}...")
            coords = api_client.get_country_coordinates(country)
            print(f"Координаты найдены: {coords}")

            print("Получаем данные о самолётах...")
            airplanes_data = api_client.get_airplanes_in_area(**coords)
            print(airplanes_data)
            airplanes = Airplane.cast_to_object_list(airplanes_data)

            for airplane in airplanes:
                json_saver.add_airplane(airplane)

            print(f"\nПолучено и сохранено {len(airplanes)} самолётов")

        except Exception as e:
            print(f"Ошибка при получении данных: {e}")
            continue

        while True:
            print("\nКакая информация вас интересует?")
            print("1. Топ N самолётов по высоте")
            print("2. Самолёты по стране регистрации")
            print("3. Узнать количество самолётов в небе")
            print("4. Выйти")
            print("5. Запросить данные по другой стране")

            choice = input("Выберите действие цифрой: ").strip()

            if choice == '1':
                try:
                    top_n_input = input("Введите количество самолётов для топа: ").strip()
                    top_n = int(top_n_input)
                    if top_n <= 0:
                        print("Число должно быть положительным.")
                        continue
                except ValueError:
                    print("Ошибка: введите целое положительное число.")
                    continue

                if not airplanes:
                    print("Данные о самолётах не получены.")
                    continue

                sorted_airplanes = sorted(
                    airplanes,
                    key=lambda a: a.altitude,
                    reverse=True
                )

                print(f"\nТоп-{top_n} самолётов по высоте:")
                for idx, airplane in enumerate(sorted_airplanes[:top_n], 1):
                    print(f"{idx}. {airplane.callsign} ({airplane.origin_country}): "
                          f"{airplane.altitude} м")

            elif choice == '2':
                country_filter = input("Введите страну регистрации (на английском): ").strip()
                if not country_filter:
                    print("Страна не может быть пустой.")
                    continue

                filtered = [a for a in airplanes if a.origin_country.lower() == country_filter.lower()]

                if not filtered:
                    print("Самолёты не найдены.")
                else:
                    print(f"\nСамолёты из {country_filter}:")
                    for airplane in filtered:
                        print(f"   - {airplane.callsign}: "
                              f"{airplane.altitude} м, {airplane.velocity} км/ч")

            elif choice == '3':
                in_flight = [a for a in airplanes if not a.on_ground]
                print(f"В небе сейчас зафиксировано: {len(in_flight)} самолётов")

            elif choice == '4':
                print("До свидания!")
                return

            elif choice == '5':
                break

            else:
                print("Неверный выбор. Попробуйте снова.")


if __name__ == "__main__":
    try:
        user_interaction()
    except KeyboardInterrupt:
        print("\nПрограмма прервана пользователем")
    except Exception as e:
        print(f"Критическая ошибка: {e}")
