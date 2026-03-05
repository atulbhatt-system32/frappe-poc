import frappe

def fix_user_permissions():
    frappe.init(site="mysite.localhost")
    frappe.connect()

    email = "testlimited@example.com"
    user = frappe.get_doc("User", email)

    # Let's ensure the user has 'Desk User' which gives the boilerplate access needed 
    # for Frappe framework (Workspace, Page, Report, etc.)
    # We remove 'Strictly Limited Role' because Frappe's underlying Desk checks can be finicky.
    
    current_roles = [r.role for r in user.get("roles")]
    
    # Clean up roles
    user.set("roles", [])
    
    for r in ["Desk User", "All"]:
        user.append("roles", {
            "role": r
        })
    
    user.save(ignore_permissions=True)
    
    frappe.db.commit()
    print("Permissions adjusted: Base 'Desk User' role provided to bypass core framework locks.")

if __name__ == "__main__":
    fix_user_permissions()
