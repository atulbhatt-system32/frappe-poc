import frappe

def setup_test_entity():
    frappe.init(site="mysite.localhost")
    frappe.connect()

    doctype_name = "Test Entity"
    
    # 1. Create the DocType
    if not frappe.db.exists("DocType", doctype_name):
        doc = frappe.get_doc({
            "doctype": "DocType",
            "name": doctype_name,
            "module": "Core",
            "custom": 1,  # Safe creation without editing core app files
            "autoname": "format:TEST-{#####}",
            "fields": [
                {"fieldname": "field_a", "label": "Field A", "fieldtype": "Int"},
                {"fieldname": "field_b", "label": "Field B", "fieldtype": "Currency"},
                {"fieldname": "field_c", "label": "Field C", "fieldtype": "Currency", "read_only": 1},
                {"fieldname": "reference", "label": "Reference", "fieldtype": "Link", "options": "Sales Order"}
            ],
            "permissions": [
                {"role": "System Manager", "read": 1, "write": 1, "create": 1, "delete": 1},
                {"role": "Strictly Limited Role", "read": 1, "write": 1, "create": 1, "delete": 1}
            ]
        })
        doc.insert(ignore_permissions=True)
        print(f"DocType '{doctype_name}' created.")
    else:
        print(f"DocType '{doctype_name}' already exists.")

    # 2. Create the Client Script for live UI updates
    script_name = f"{doctype_name} Calculations"
    if not frappe.db.exists("Client Script", script_name):
        frappe.get_doc({
            "doctype": "Client Script",
            "name": script_name,
            "dt": doctype_name,
            "script": """frappe.ui.form.on('Test Entity', {
    field_a: function(frm) {
        frm.set_value('field_c', flt(frm.doc.field_a) * flt(frm.doc.field_b));
    },
    field_b: function(frm) {
        frm.set_value('field_c', flt(frm.doc.field_a) * flt(frm.doc.field_b));
    }
});""",
            "enabled": 1
        }).insert(ignore_permissions=True)
        print("Client Script created.")

    # 3. Create 5 dummy records
    existing_count = frappe.db.count(doctype_name)
    if existing_count < 5:
        for i in range(1, 6):
            new_doc = frappe.get_doc({
                "doctype": doctype_name,
                "field_a": i,
                "field_b": 150.00 * i,
                "field_c": i * (150.00 * i)
            })
            new_doc.insert(ignore_permissions=True)
        print("Inserted 5 records successfully.")

    # 4. Make it visible in Workspace
    workspace_name = "Limited Workspace"
    if frappe.db.exists("Workspace", workspace_name):
        ws = frappe.get_doc("Workspace", workspace_name)
        
        # Check if shortcut already exists
        exists = any(s.link_to == doctype_name for s in ws.get("shortcuts", []))
        if not exists:
            ws.append("shortcuts", {
                "type": "DocType",
                "label": doctype_name,
                "link_to": doctype_name
            })
            ws.save(ignore_permissions=True)
            print(f"Added {doctype_name} shortcut to '{workspace_name}' Workspace.")

    frappe.db.commit()

if __name__ == "__main__":
    setup_test_entity()
