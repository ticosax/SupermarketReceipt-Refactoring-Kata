from approvaltests import verify

from supermarket_receipt.receipt_printer import ReceiptPrinter


def test_receipt_printer_wo_discount_text(no_discount_receipt):
    printer = ReceiptPrinter()
    verify(printer.print_receipt(no_discount_receipt, mimetype="text/plain"))


def test_receipt_printer_with_discount_text(percent_discount_receipt):
    printer = ReceiptPrinter()
    verify(printer.print_receipt(percent_discount_receipt, mimetype="text/plain"))


def test_receipt_printer_with_bulk_discount_text(bulk_discount_receipt):
    printer = ReceiptPrinter()
    verify(printer.print_receipt(bulk_discount_receipt, mimetype="text/plain"))


def test_receipt_printer_wo_discount_html(no_discount_receipt):
    printer = ReceiptPrinter()
    verify(printer.print_receipt(no_discount_receipt, mimetype="text/html"))


def test_receipt_printer_with_discount_html(percent_discount_receipt):
    printer = ReceiptPrinter()
    verify(printer.print_receipt(percent_discount_receipt, mimetype="text/html"))


def test_receipt_printer_with_bulk_discount_html(bulk_discount_receipt):
    printer = ReceiptPrinter()
    verify(printer.print_receipt(bulk_discount_receipt, mimetype="text/html"))
