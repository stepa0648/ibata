from ibata.cli_app import *


def test_save_as_none(runner, categories_summary):
    with runner.isolated_filesystem():
        save_as = "NONE"
        assert ResultSaver.save_result(save_as, categories_summary) is False
        save_as = None
        assert ResultSaver.save_result(save_as, categories_summary) is False


def test_save_as_txt(runner, categories_summary):
    text = """Přehled výdajů a příjmů

Od: 2020-01-01
Do: 2020-02-01

Příjmy:           0.00 Kč
Výdaje:       -1886.50 Kč
Cash-flow:    -1886.50 Kč

Hobby                   -1443.25 Kč
    2020-01-20 99512343             0300    -1443.25 CZK hobby           Platba převodem                John Doe                  Obi Regál do garáže 
Elektronika              -443.25 Kč
    2020-01-05                               -443.25 CZK electronics     Platba kartou                  John Doe                  Alza.cz Sluchátka v alze 
"""
    with runner.isolated_filesystem():
        save_as = "TXT"
        ResultSaver.save_result(save_as, categories_summary)
        with open(f"2020-01-01_2020-02-01.txt", 'r') as file:
            lines = file.read()
        assert lines == text


def test_save_as_json(runner, categories_summary):
    json_output = '''[{"name": "hobby", "name_pretty": "Hobby", "amount": -1443.25, "transactions": [{"date": "2020-01-20", "account": "99512343", "bank_code": "0300", "amount": -1443.25, "currency": "CZK", "message_for_payee": "Obi", "operation_type": "Platba převodem", "executor": "John Doe", "note": "Regál do garáže", "user_identification": null, "category": "hobby"}]}, {"name": "electronics", "name_pretty": "Elektronika", "amount": -443.25, "transactions": [{"date": "2020-01-05", "account": null, "bank_code": null, "amount": -443.25, "currency": "CZK", "message_for_payee": "Alza.cz", "operation_type": "Platba kartou", "executor": "John Doe", "note": "Sluchátka v alze", "user_identification": null, "category": "electronics"}]}]'''
    with runner.isolated_filesystem():
        save_as = "JSON"
        ResultSaver.save_result(save_as, categories_summary)
        with open(f"2020-01-01_2020-02-01.json", 'r') as file:
            lines = file.read()
        assert lines == json_output


def test_save_as_csv(runner, categories_summary):
    output = """Date,Account,Bank code,Amount,Currency,Category,Message for payee,Operation type,Executor,Note,User identification
2020-01-20,99512343,0300,-1443.25,CZK,hobby,Obi,Platba převodem,John Doe,Regál do garáže,
2020-01-05,,,-443.25,CZK,electronics,Alza.cz,Platba kartou,John Doe,Sluchátka v alze,
"""
    with runner.isolated_filesystem():
        save_as = "CSV"
        ResultSaver.save_result(save_as, categories_summary)
        with open(f"2020-01-01_2020-02-01.csv", 'r') as file:
            lines = file.read()
        print("##############")
        print(lines)
        print("##############")
        assert lines == output
