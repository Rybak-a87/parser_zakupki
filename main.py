# ----------------------------
# Parser zakupki.gov.ru
# version: 1.2
# ----------------------------
# author: Rybak A.A.
#
# ----------------------------


from ParserSection import ParserSection as PS
from WorkWithExcel import *
from config import *


def start():
    print("Wait...")
    row = 2
    save_by = 30    # по сколько записей сохранять
    save_count = 1    # сколько сохранений прошло

    par = PS(WEBSITE)
    par.set_list_pages(amount_pagers, website_section)

    excel_file = ToExcel(file_name)
    excel_file.write_to_excel_name_col_list(title_list)

    for url in par.get_pages():
        par.pagers(url)
        link = par.selects("div.registry-entry__header-mid__number a")
        par.set_list_cards(link)

        for card in par.get_cards():
            par.pagers(card)
            keys = par.selects("section.blockInfo__section span.section__title")
            values = par.selects("section.blockInfo__section span.section__info")
            par.set_dict(keys, values)

            if par.selects("tr.tableBlock__row th.tableBlock__col_header"):
                k = par.selects("tr.tableBlock__row th.tableBlock__col_header")
                v = par.selects("tr.tableBlock__row td.tableBlock__col")
                par.add_to_dict(k, v)
            temp_dict = dict()
            temp_dict["ссылка на карточку"] = card

            excel_file.write_to_excel_value(title_list, par.get_dict() | temp_dict, row)
            row += 1

            if row % save_by == 0:
                excel_file.save_excel()
                print("-"*30, f"|--Обработано {save_by*save_count} карточек--|", sep="\n")
                save_count += 1

    excel_file.save_excel()

        
if __name__ == '__main__':
    demo(20201101)
    start()
print("\nCompleted!!!")
