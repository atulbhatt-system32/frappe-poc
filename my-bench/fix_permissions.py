import frappe

def fix_user_permissions():
    frappe.init(site="mysite.localhost")
    frappe.connect()

    email = "testlimited@example.com"
    role_name = "Strictly Limited Role"

    user = frappe.get_doc("User", email)
    existing_roles = [r.role for r in user.get("roles")]

    # Every user needs the 'All' role to access basic frappe desk components like Pages
    if "All" not in existing_roles:
        user.append("roles", {
            "role": "All"
        })
        user.save(ignore_permissions=True)
        print("Added 'All' role back to the user.")

    # Explicitly grant read permission for Page and Workspace just in case
    for dt in ["Page", "Workspace"]:
        if not frappe.db.exists("Custom DocPerm", {"parent": dt, "role": role_name}):
            frappe.get_doc({
                "doctype": "Custom DocPerm",
                "parent": dt,
                "role": role_name,
                "read": 1,
                "permlevel": 0
            }).insert(ignore_permissions=True)
            print(f"Granted {role_name} read access to {dt}.")

    frappe.db.commit()
    print("Permissions patched successfully.")

if __name__ == "__main__":
    fix_user_permissions()
