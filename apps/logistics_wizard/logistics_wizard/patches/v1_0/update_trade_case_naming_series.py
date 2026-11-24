# Copyright (c) 2026, Logistics Wizard and contributors
# For license information, please see license.txt

import frappe


def execute():
    """
    Remove legacy Property Setters that pinned Trade Case naming_series to TC-.YYYY.-.
    and reload Trade Case DocType so IMP-.YYYY.-.#### / EXP-.YYYY.-.#### / TC-.YYYY.-.
    take effect cleanly during bench migrate.
    """
    for ps_name in (
        "Trade Case-naming_series-default",
        "Trade Case-naming_series-options",
    ):
        if frappe.db.exists("Property Setter", ps_name):
            val = str(frappe.db.get_value("Property Setter", ps_name, "value") or "")
            if "IMP-.YYYY.-.####" not in val:
                frappe.delete_doc("Property Setter", ps_name, ignore_permissions=True, force=True)

    frappe.reload_doc("logistics_wizard", "doctype", "trade_case", force=True)
    frappe.clear_cache(doctype="Trade Case")
