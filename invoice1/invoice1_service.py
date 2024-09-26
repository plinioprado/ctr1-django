""" invoice1 service with business logic """

# pylint: disable=broad-exception-caught

from typing import Optional
from invoice1.invoice1_model import Invoice1Model
import invoice1.invoice1_sqlite as dao

ResType = dict[str, Optional[str | int | dict[str, str | int | float] | list[dict[str, str | int | float]]]] # pylint: disable=line-too-long


class Invoice1Service:
    """ Receive Requests in a REST format and returns dicts to be converted into Responses """

    @classmethod
    def get(cls) -> ResType:
        """
        Get all Invoices

        Returns:
            dict with code, message, and list of invoices for the response,
            or for the error response
        """

        try:
            invoices: list[Invoice1Model] = dao.get()
            data: list[dict[str, str | int | float]] = [invoice.dict() for invoice in invoices]
            return {
                "code": 200,
                "message": "ok",
                "data": data
            }
        except Exception as err:
            return cls._handle_errors(err)


    @classmethod
    def get_by_num(cls, num: int) -> ResType:
        """
        Get the Invoice with a given number

        Args:
            num: number of the invoice

        Returns:
            dict with code, message, and invoice for the response, or for the error response
        """
        try:
            invoice: Invoice1Model | None = dao.get_by_num(int(num))
            data = {} if invoice is None else invoice.dict()
            return {
                "code": 200,
                "message": "ok",
                "data": data
            }
        except Exception as err:
            return cls._handle_errors(err)


    @classmethod
    def post(cls, req_data) -> ResType:
        """
        Create (post) an Invoice

        Args:
            req_data: dict with the data of the new invoice ('num' will be auto numbered)

        Returns:
            dict with code and message for the response, or for the error response
        """

        try:
            invoice: Invoice1Model = Invoice1Model(req_data)
            num: int = dao.post(invoice)["num"]
            return {
                "code": 200,
                "message": f"invoice {num} created"
            }
        except Exception as err:
            return cls._handle_errors(err)


    @classmethod
    def put(cls, req_data) -> ResType:
        """
        Delete (put) an Invoice

        Args:
            req_data: dict with the new data of the invoice whose number is the 'num' value

        Returns:
            dict with code and message for the response, or for the error response
        """

        try:
            invoice: Invoice1Model = Invoice1Model(req_data)
            num: int = dao.put(invoice)["num"]
            return {
                "code": 200,
                "message": f"invoice {num} updated"
            }
        except Exception as err:
            return cls._handle_errors(err)


    @classmethod
    def delete(cls, req_data) -> ResType:
        """
        Delete an Invoice

        Args:
            req_data: dict { 'num': <num>} where num is the invoice to be deleted

        Returns:
            dict with code and message for the response, or for the error response
        """

        try:
            if "num" not in req_data:
                raise ValueError("400|Missing num")

            if req_data["num"] == "reset":
                dao.reset()
                return {
                    "code": 200,
                    "message": "invoice deleted"
                }

            if not isinstance(req_data["num"], int):
                raise ValueError("400|Invalid num")

            num:int = dao.delete(req_data["num"])

            return {
                "code": 200,
                "message": f"invoice {num} deleted"
            }
        except Exception as err:
            return cls._handle_errors(err)


    @classmethod
    def reset(cls) -> ResType:
        """
        Reset the SQLite database

        Returns:
            dict with code and message for the response, or for the error response
        """

        try:
            dao.reset()
            return {
                "code": 200,
                "message": "invoice reset"
            }
        except Exception as err:
            return cls._handle_errors(err)


    @classmethod
    def _handle_errors(cls, err: Exception) -> ResType:
        """
        Handles errors

        Args:
            Exception classes

        Returns:
            dict for the erro response
        """
        error_parts = str(err).split("|")

        if len(error_parts) != 2:
            error_code = 500
            error_message: str = str(err)
        elif error_parts[0] == "400":
            error_code = 400
            error_message = error_parts[1]
        else:
            error_code = 500
            error_message = error_parts[1]

        return {"code": error_code, "message": error_message}
