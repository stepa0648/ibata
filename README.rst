=============================
NI-PYT Semestral work - IBATA
=============================

Author: Štěpán Severa (severste)

This semestral work will be console application that should work as transaction organizer of payment transactions. It will download transaction from bank API and then it will organize them into different categories. After that it will provide some charts of how many user spent in which category. User will be able to specify which time period he wants to download from API and get results from.

IBATA is Internet BAnking Transactions Analyzator.

*****************************************
Functional and nonfunctional requirements
*****************************************

Functional requirements
=======================
1. Application will provide CLI, where user can specify the time period of transactions that will be downloaded from bank API.
2. Application will provide downloading transactions from FIO bank API, but it will provide possibility to extend this downloader of another bank API.
3. Application will provide categorization transactions into different specified categories. User will be able to modify these categories and will be able to modify which transaction will be assigned into which category.
4. Application will provide charts, that will visualize spendings in given categories.
5. Application will provide saving results into a file in JSON and CSV format.

Nonfunctional requirements
==========================
1. Application will be CLI app.
2. Application will be expandable of possibilities to download from another bank API's.
3. Application will provide help, how to use it.
4. Application will be tested and documented.