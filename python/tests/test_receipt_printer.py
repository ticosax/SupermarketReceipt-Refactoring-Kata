from approvaltests import verify

from supermarket_receipt.receipt_printer import ReceiptPrinter


def test_receipt_printer_wo_discount(no_discount_receipt):
    printer = ReceiptPrinter()
    verify(printer.print_receipt(no_discount_receipt))


def test_receipt_printer_with_discount(percent_discount_receipt):
    printer = ReceiptPrinter()
    verify(printer.print_receipt(percent_discount_receipt))


def test_receipt_printer_with_bulk_discount(bulk_discount_receipt):
    printer = ReceiptPrinter()
    verify(printer.print_receipt(bulk_discount_receipt))
