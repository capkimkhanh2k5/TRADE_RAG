# Copyright (c) 2026, Logistics Wizard and contributors
# For license information, please see license.txt

try:
    from frappe.model.document import Document
except ImportError:
    class Document:
        pass


class CustomsDeclarationItem(Document):
    pass
