from config import config
from src.DBManager import DBManager
from src.utils import __get_employee_data, __get_vacancies_data, create_database, save_data_to_database_emp, \
    save_data_to_database_vac


def main():
    """
    Функция для запуска программы.
    :return:
    """
    user_name = input('Введите ваше имя:\n')
    print(f"Здравствуйте, {user_name}. Ваши возможные действия:\n"
          "1 - Посмотреть список всех компаний и количество вакансий у каждой компании\n"
          "2 - Посмотреть список всех вакансий с указанием названия компании, названия вакансии, зарплаты"
          "и ссылки на вакансию\n"
          "3 - Узнать среднюю зарплату по вакансиям\n"
          "4 - Посмотреть список всех вакансий, у которых зарплата выше средней по всем вакансиям\n"
          "5 - Посмотреть список всех вакансий, в названии которых содержатся запрашиваемое слово\n"
          "0 - Выход из программы\n")

    params = config()

    data_emp = __get_employee_data()
    data_vac = __get_vacancies_data()
    create_database('hh', params)
    save_data_to_database_emp(data_emp, 'hh', params)
    save_data_to_database_vac(data_vac, 'hh', params)
    db_manager = DBManager(params)


    while True:
        user_input = input('Введите номер запроса:\n')
        if user_input == "1":
            companies_and_vacancies_count = db_manager.get_companies_and_vacancies_count()
            print(f"Список всех компаний и количество вакансий у каждой компании:\n{companies_and_vacancies_count}\n")

        elif user_input == "2":
            all_vacancies = db_manager.get_all_vacancies()
            print(
                f"Cписок всех вакансий с указанием названия компании, названия вакансии, зарплаты и ссылки на вакансию:\n{all_vacancies}\n")

        elif user_input == '3':
            avg_salary = db_manager.get_avg_salary()
            print(f"Средняя зарплата по вакансиям:\n{avg_salary}\n")

        elif user_input == "4":
            vacancies_with_higher_salary = db_manager.get_vacancies_with_higher_salary()
            print(
                f"Список всех вакансий, у которых зарплата выше средней по всем вакансиям:\n{vacancies_with_higher_salary}\n")

        elif user_input == "5":
            user_input = input('Введите ключевое слово ')
            vacancies_with_keyword = db_manager.get_vacancies_with_keyword(user_input)
            print(f"Список всех вакансий, в названии которых содержатся запрашиваемое слово:\n{vacancies_with_keyword}")

        elif user_input == '0':
            break


if __name__ == '__main__':
    main()
