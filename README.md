# IBATA - Internet Banking transactions analyzator
Author: Štěpán Severa (stepa0648)

## Basic info

**IBATA** is **I**nternet **BA**nking **T**ransactions **A**nalyzator.

This program downloads transaction from you Bank API (currently only Fio). Then it categorize it and print to output.

Output can be saved into various formats (TXT, JSON, CSV).

Plot showing amounts of transaction in different categories can be generated too.

All options can be showed by ``ibata --help``.

### App usage
```

    Usage: ibata [OPTIONS]

    A tool for analyzing bank transactions

    Options:
      --version                       Show the version and exit.
      -c, --config FILENAME           IBATA configuration file. [default:
                                      ibata.cfg]

      -f, --from DATE                 Date from which the transactions are being
                                      downloaded and parsed. Format is YYYY-MM-DD.
                                      [Required if -e flag is missing]

      -t, --to DATE                   Date to which the transactions are being
                                      downloaded and parsed. Format is YYYY-MM-DD.
                                      [Required if -e flag is missing]

      -m, --month DATE                Year and month from which the transactions
                                      are being downloaded and parsed. Format is
                                      YYYY-MM.[Required if -e, -f and -t flags are
                                      missing]

      -b, --bank ['FIO']              Bank from which will be transactions
                                      downloaded. Default: FIO

      -o, --output-format [SUMMARY|CATEGORIES|ALL|NONE]
                                      Verbosity level of the output. works only
                                      for output into console or into TXT file.
                                      [default: ALL]

      -p, --plot                      Should generate plot, show it, and save it
                                      in "{date_from}_{date_to}.png"

      -s, --save-as [TXT|JSON|CSV|NONE]
                                      In which format should be result saved. If
                                      not present result won't be saved.  If
                                      present, result would be saved into
                                      "{date_from}_{date_to}.{save-as}" file.
                                      [default: NONE]

      -e, --edit, --edit-categories   If present app enters editation mode for
                                      categories and other options are ignored.

  --help                          Show this message and exit.
```



### Config file


Config file should be::
```
[FIO]
token=XXXX

[Categories]
file=ibata/categories.json
```

Where [FIO] token is token for FIO bank API and [Categories] file is name of file, in which categories are described.
For basic functionality leave ``[Categories] file`` as in the example. In this project is provided ``categories.json`` with
some categories defined.

Default option for CLI app is config file named ``ibata.cfg`` in root folder of this directory.

### Categories file

Categories file is JSON file with a list of categories.

Basic Categories file is in this module ``ibata/categories.json``.

This file (defined in config file) can be edited via Categories editing mode (Can be found in :ref:`categories-editing`)


Example is
```json
 [
    {
        "name": "entertainment",
        "name_pretty": "Zábava",
        "data": [
            "netflix",
            "lasergame",
            "hry",
            "games"
        ]
    }
 ]
```
### Working modes
There are two working modes:

1. Categories editing
2. Transaction categorizing

#### Categories editing
This mode is enabled via ``-e``, ``--edit``, ``--edit-categories`` options.
If this option is enabled other options are ignored.

If this mode is selected program will list all categories, show every task user can perform and waits for input.
Every step is provided with options that user can select. At the end user can exit without saving and everything that
he has done is discarded, or he can save and exit and all changes will be saved into categories file provided
in Config file.

Here is state diagram of Category Manager states:

![Categories editing diagram](../ibata/images/categories_manager_states.png)

#### Transaction categorizing
If option ``-e`` is missing, app will start in this mode.

``-f, --from DATE`` and ``-t, --to DATE``
    In this mode options ``-f, --from DATE`` and ``-t, --to DATE`` are required.
    It defines date from and to which transaction should be downloaded.

``-b, --bank ['FIO']``
    Option ``-b, --bank ['FIO']`` defines from which Bank the transactions should be downloaded.
    Currently only FIO bank is supported.

``-o, --output-format [SUMMARY|CATEGORIES|ALL|NONE]``
    Option ``-o, --output-format [SUMMARY|CATEGORIES|ALL|NONE]`` defines the verbosity level of the output.
    It works only for output into console or into TXT file. Default is ALL.

``-p, --plot``
    Option ``-p, --plot`` defines whether plot should be generated plot. If so it will be generated, showed
    and saved in ``{date_from}_{date_to}.png``.

``-s, --save-as [TXT|JSON|CSV|NONE]``
    Option ``-s, --save-as [TXT|JSON|CSV|NONE]`` defines if the output should be saved and in which format it should be saved.
    Output will be saved into ``{date_from}_{date_to}.{save-as}`` file. Default is NONE.


### Adding new bank support
In directory ``ibata/downloaders`` create new file named
``{NEW_BANK_NAME}TransactionDownloader.py``. Create new class named same as the file and make sure that this class
inherits ``TransactionDownloader``. This class needs to implement method:

```python
def get_transactions(self, from_date, to_date):
```
and returns list of ``Transaction`` objects.

After this add your new class to ``TransactionDownloaderResolver`` into ``BANKS``
dict. Insert it there as ``"{NEW_BANK_NAME}": {NEW_BANK_NAME}TransactionDownloader``. Keys in this dict are used as CLI
option to select from which bank do you want to download transaction.

### Testing

#### Running tests

Install test requirements::

    pip install .[test]

and run tests::

    pytest tests

##### Using tox
Tests can be run via:

    tox

command.
Arguments can be passed for ``pytest`` using::

    tox -- {pytest args}

More info about tox can be found by::

    tox --help

Tests run by ``tox`` are defined in `tox.ini`  file in section ``testpaths``. Currently there are all tests
available in ``tests`` directory.

#### Tests preparation
Testing of HTTP communication is done by `betamax <https://betamax.readthedocs.io/en/latest/>`_
Communication is recorded onto cassettes in directory ``/tests/fixtures/cassettes``.

If you don't want to use these cassettes or you want to test functionality on your bank account you can rerecord these
cassettes.

If you want to rerecord betamax cassettes you need to delete them from ``tests/fixtures/cassetes`` directory.
Then you need to add following environment variables:

- `FIO_TOKEN`: your FIO Token for Fio Bank API
- `NAME`: your surname in uppercase e.g. Doe
- `ACCOUNTID`: number of your bank account
- `IBAN`: number of your IBAN
- `BIC`: number of your BIC
- `NAME_LC`: your surname starting with Uppercase letter and following with lowercase e.g. Doe

All of these variables are used for hiding confident information in cassettes.
Token is also used for downloading transaction from Fio API.

### Documentation
Documentation is in directory ``docs`` and can be generated by::

    make html

run from ``docs`` directory. Generated documentation can be then found in ``docs/_build/html`` and can be viewed
in browser by opening ``index.html`` file.
