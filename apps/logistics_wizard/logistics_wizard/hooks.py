app_name = "logistics_wizard"
app_title = "Logistics"
app_publisher = "Khanh"
app_description = "Import-Export Workflow Widget and Shipment Tracking Management Hub"
app_email = "khanh@logistics.local"
app_license = "mit"

app_logo_url = "/assets/logistics_wizard/images/logistics-wizard-logo.svg"
app_home = "/desk/logistics-wizard/trade-case-overview"

add_to_apps_screen = [
    {
        "name": app_name,
        "logo": app_logo_url,
        "title": "Logistics",
        "route": app_home,
        "sequence_id": 2,
    }
]

app_include_js = [
    "leaflet.bundle.js",
    "smart_workflow_widget.bundle.js",
    "unified_logistics_hub.bundle.js"
]
app_include_css = [
    "leaflet.bundle.css",
    "smart_workflow_widget.bundle.css",
    "unified_logistics_hub.bundle.css"
]


doctype_js = {
    "Shipment Tracking": "public/js/shipment_tracking.js",
    "Trade Cost Sheet": "doctype/trade_cost_sheet/trade_cost_sheet.js"
}

doc_events = {
    "Trade Case": {
        "after_insert": "logistics_wizard.document_engine.api.on_trade_case_after_insert"
    },
    "Shipment Tracking": {
        "validate": "logistics_wizard.api.on_shipment_tracking_validate"
    },
    "Purchase Receipt": {
        "before_submit": "logistics_wizard.api.validate_purchase_receipt_shipment_status",
        "on_submit": "logistics_wizard.warehouse_engine.api.on_purchase_receipt_submit"
    },
    "Delivery Note": {
        "before_submit": "logistics_wizard.api.validate_delivery_note_shipment_status"
    }
}

scheduler_events = {
    "daily": [
        "logistics_wizard.document_engine.api.scheduled_check_expiring_documents",
        "logistics_wizard.customs_engine.api.scheduled_check_overdue_customs",
    ],
    "hourly": [
        "logistics_wizard.tracking_service.scheduled_scan_stale_shipments",
        "logistics_wizard.exception_engine.api.scheduled_evaluate_all_active_cases",
    ],
    "cron": {
        "0 */2 * * *": [
            "logistics_wizard.tracking_service.scheduled_sync_active_shipments",
        ],
    },
}

