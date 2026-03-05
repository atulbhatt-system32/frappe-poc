import frappe
import json

def fix_limited_workspace():
    frappe.init(site="mysite.localhost")
    frappe.connect()

    ws_name = "Limited Workspace"
    if not frappe.db.exists("Workspace", ws_name):
        print("Workspace not found")
        return

    ws = frappe.get_doc("Workspace", ws_name)
    
    # Define the new content with the shortcut block
    content = [
        {
            "id": "header_1",
            "type": "header",
            "data": {
                "text": "Your Data",
                "level": 4,
                "col": 12
            }
        },
        {
            "id": "shortcut_test_entity",
            "type": "shortcut",
            "data": {
                "shortcut_name": "Test Entity",
                "col": 4
            }
        }
    ]
    
    ws.content = json.dumps(content)
    
    # Ensure roles are correct
    ws.set("roles", [])
    for role in ["Strictly Limited Role", "Desk User", "All"]:
        ws.append("roles", {"role": role})
    
    ws.save(ignore_permissions=True)
    frappe.db.commit()
    print("Limited Workspace content updated with shortcut block.")

if __name__ == "__main__":
    fix_limited_workspace()
