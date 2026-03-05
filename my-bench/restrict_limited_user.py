import frappe

def enforce_strict_limited_user():
    frappe.init(site="mysite.localhost")
    frappe.connect()

    email = "testlimited@example.com"
    if not frappe.db.exists("User", email):
        print(f"User {email} not found.")
        return

    # 1. Ensure a specific Role exists that grants only Desk Access
    role_name = "Strictly Limited Role"
    if not frappe.db.exists("Role", role_name):
        frappe.get_doc({
            "doctype": "Role",
            "role_name": role_name,
            "desk_access": 1
        }).insert(ignore_permissions=True)

    user = frappe.get_doc("User", email)

    # Replace roles with ONLY the strictly limited role
    # This ensures they have ZERO permission entries by default!
    user.set("roles", [{"role": role_name}])

    # 2. Hide all non-required modules
    # Fetch all Module Definitions
    all_modules = frappe.get_all("Module Def", pluck="name")
    
    # We allow 'Core' and 'Desk' because they contain framework essentials
    allowed_modules = ["Core", "Desk"]
    
    user.set("block_modules", [])
    for module in all_modules:
        if module not in allowed_modules:
            user.append("block_modules", {
                "module": module
            })

    # 3. Create one dedicated workspace
    workspace_name = "Limited Workspace"
    if frappe.db.exists("Workspace", workspace_name):
        frappe.delete_doc("Workspace", workspace_name, force=1)
        
    workspace = frappe.get_doc({
        "doctype": "Workspace",
        "title": workspace_name,
        "label": workspace_name,
        "public": 1,
        "is_hidden": 0,
        "module": "Core",
        "roles": [{"role": role_name}],
        # Just putting a simple UI element so it's not a blank page
        "content": '[{"id":"header_shortcuts","type":"header","data":{"text":"Your Shortcuts","level":4}}]'
    })
    workspace.insert(ignore_permissions=True)

    # 4. Assign the workspace to the Limited User as their default
    user.default_workspace = workspace_name
    
    # Save the user with these extreme limitations applied
    user.save(ignore_permissions=True)
    frappe.db.commit()
    print("Strict limit constraints successfully applied to", email)

if __name__ == "__main__":
    enforce_strict_limited_user()
