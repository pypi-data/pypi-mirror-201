from __future__ import annotations
from datetime import datetime
from datetime import date


class Filing:
    """
    The filing class contains all the metadata of a filing.
    It is used to store the filings metadata in a uniform format.
    """

    def __init__(self,
                 accession_number: str = None,
                 ticker_symbol: str = None,
                 cik: str = None,
                 filing_date: date = None,
                 report_date: date = None,
                 acceptance_date_time: datetime = None,
                 act: str = None,
                 form: str = None,
                 file_number: str = None,
                 film_number: str = None,
                 items: str = None,
                 size: int = None,
                 is_xbrl: bool = None,
                 is_inline_xbrl: bool = None,
                 primary_document: str = None,
                 primary_doc_description: str = None):
        """
        :param accession_number: the accession number of the filing
        :param filing_date: the date the filing was submitted
        :param report_date: the date the filing is reporting
        :param acceptance_date_time: the date and time the filing was accepted
        :param act: the act of the filing
        :param form: the form of the filing
        :param file_number: the file number of the filing
        :param film_number: the film number of the filing
        :param items: the items of the filing
        :param size: the size of the filing
        :param is_xbrl: if the filing is xbrl
        :param is_inline_xbrl: if the filing is inline xbrl
        :param primary_document: the primary document of the filing
        :param primary_doc_description: the primary document description of the filing
        """
        self._accession_number: str = accession_number
        self._ticker_symbol: str = ticker_symbol
        self._cik: str = cik
        self._filing_date: date = filing_date
        self._report_date: date = report_date
        self._acceptance_date_time: datetime = acceptance_date_time
        self._act: str = act
        self._form: str = form
        self._file_number: str = file_number
        self._film_number: str = film_number
        self._items: str = items
        self._size: int = size
        self._is_xbrl: bool = is_xbrl
        self._is_inline_xbrl: bool = is_inline_xbrl
        self._primary_document: str = primary_document
        self._primary_doc_description: str = primary_doc_description

    @staticmethod
    def from_dict(filing_dict: dict) -> Filing:
        """
        Creates a filing object from the json that is returned by the web request to the sec server.
        The values are converted to appropriate python types.
        """
        accession_number: str = filing_dict.get('accessionNumber')
        filing_date: date = datetime.strptime(filing_dict.get("filingDate"), '%Y-%m-%d').date()
        report_date: date = datetime.strptime(filing_dict.get("reportDate"), '%Y-%m-%d').date()
        ticker_symbol: str = filing_dict.get('tickerSymbol')
        cik: str = filing_dict.get('cik')

        datetime_str = filing_dict.get("acceptanceDateTime")
        datetime_str = datetime_str.replace("T", " ")
        datetime_str = datetime_str.replace(".000Z", "")
        acceptance_date_time: datetime = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M:%S")

        act: str = filing_dict.get('act')
        form: str = filing_dict.get('form')
        file_number: str = filing_dict.get('fileNumber')
        film_number: str = filing_dict.get('filmNumber')
        items: str = filing_dict.get('items')
        size: int = filing_dict.get('size')

        is_xbrl: bool = bool(filing_dict.get('isXBRL'))
        is_inline_xbrl: bool = bool(filing_dict.get('isInlineXBRL'))

        primary_document: str = filing_dict.get('primaryDocument')
        primary_doc_description: str = filing_dict.get('primaryDocDescription')

        return Filing(accession_number=accession_number,
                      ticker_symbol=ticker_symbol,
                      cik=cik,
                      filing_date=filing_date,
                      report_date=report_date,
                      acceptance_date_time=acceptance_date_time,
                      act=act,
                      form=form,
                      file_number=file_number,
                      film_number=film_number,
                      items=items,
                      size=size,
                      is_xbrl=is_xbrl,
                      is_inline_xbrl=is_inline_xbrl,
                      primary_document=primary_document,
                      primary_doc_description=primary_doc_description)

    @property
    def accession_number(self) -> str:
        return self._accession_number

    @property
    def ticker_symbol(self) -> str:
        return self._ticker_symbol

    @property
    def cik(self) -> str:
        return self._cik

    @property
    def filing_date(self) -> date:
        return self._filing_date

    @property
    def report_date(self) -> date:
        return self._report_date

    @property
    def acceptance_date_time(self) -> datetime:
        return self._acceptance_date_time

    @property
    def act(self) -> str:
        return self._act

    @property
    def form(self) -> str:
        return self._form

    @property
    def file_number(self) -> str:
        return self._file_number

    @property
    def film_number(self) -> str:
        return self._film_number

    @property
    def items(self) -> str:
        return self._items

    @property
    def size(self) -> int:
        return self._size

    @property
    def is_xbrl(self) -> bool:
        return self._is_xbrl

    @property
    def is_inline_xbrl(self) -> bool:
        return self._is_inline_xbrl

    @property
    def primary_document(self) -> str:
        return self._primary_document

    @property
    def primary_doc_description(self) -> str:
        return self._primary_doc_description
