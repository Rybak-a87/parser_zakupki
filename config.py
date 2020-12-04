from WorkWithExcel import FromExcel, now_day, now_month, now_year


WEBSITE = "https://zakupki.gov.ru"


# Ссылка на форму
FORM = FromExcel("form_to_start/FormToFill.xlsx")


# Чтение с формы
file_name = FORM.read_cell_str("G", 2)
title_list = FORM.read_col_in_list("B", 2)
title_list.append("Ссылка на карточку")
website_section = FORM.read_cell_str("G", 10)
amount_pagers = int(FORM.read_cell_str("G", 6))


def demo(n):
    """Настройка демо версии по дате"""
    now = int(f"{now_year}{now_month}{now_day}")
    if now > n:
        print("Stoped....")
        exit(0)
