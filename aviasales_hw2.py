# 1.	Доработать приложение по поиску авиабилетов, чтобы оно возвращало билеты
# по названию города, а не по IATA коду. (У aviasales есть для этого дополнительное API)
# Пункт отправления и пункт назначения должны передаваться в качестве параметров.
# Сделать форматированный вывод, который содержит в себе пункт отправления,
# пункт назначения, дату вылета,
# цену билета (можно добавить еще другие параметры по желанию)

import sys
import requests


def find_iata_cities(origin, destination):
    """
    описание
    :param origin:
    :param destination:
    :return:
    """

    cities_params = {'q': origin+' '+destination}

    req_cities = requests.get("https://www.travelpayouts.com/widgets_suggest_params",
                              params=cities_params)

    data_cities = req_cities.json()

    return data_cities


def find_ticket_date_cities(iata_origin, iata_destination, date_trip):
    """
    описание
    :param iata_origin: 
    :param iata_destination: 
    :param date_trip: 
    :return: 
    """
    flight_params = {
        'origin': iata_origin,
        'destination': iata_destination,
        'depart_date': date_trip

    }
    req_iata = requests.get("http://min-prices.aviasales.ru/calendar_preload",
                            params=flight_params)

    data_iata = req_iata.json()

    return sorted(data_iata['current_depart_date_prices'], key=lambda x: x['value'])


def print_results(cities, date, tickets):
    """
    описание
    :param cities:
    :param date:
    :param tickets:
    :return:
    """
    print(f"Пункт отправления: {cities['origin']['name']}")
    print(f"пункт назначения: {cities['destination']['name']}")
    print(f"дата: {date}")
    print()
    print(f"найдено {len(tickets)} лучших вариантов на эту дату:")
    for i, ticket in enumerate(tickets, start=1):
        print("==================================================")
        print(f"{i}. где купить: {ticket['gate']} количество пересадок: "
              f"{ticket['number_of_changes']} цена: {ticket['value']}")


# поиск кодов iata по названиям городов
iata_cities = find_iata_cities(sys.argv[1], sys.argv[2])
# pprint.pprint(iata_cities)

# поиск билетов по городам и дате
sort_tickets = find_ticket_date_cities(iata_cities['origin']['iata'],
                                       iata_cities['destination']['iata'], sys.argv[3])

# вывод результатов
print_results(iata_cities, sys.argv[3], sort_tickets)
