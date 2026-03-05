import frappe

def finally_fix_permissions():
    frappe.init(site="mysite.localhost")
    frappe.connect()

    # We need to give `Desk User` read access to the 'Page' and 'Workspace' DocTypes OR
    # simply give the user back the `Strictly Limited Role` and ensure it has the docperms 
    # we added earlier.
    
    # I'll just give the testuser both Desk User, All, and Strictly Limited Role
    user = frappe.get_doc("User", "testlimited@example.com")
    
    current_roles = [r.role for r in user.get("roles")]
    required_roles = ["All", "Desk User", "Strictly Limited Role"]
    
    for req in required_roles:
        if req not in current_roles:
            user.append("roles", {"role": req})
    
    user.save(ignore_permissions=True)
    
    # Let's ensure 'Strictly Limited Role' has access to Page, Workspace, and Test Entity
    for dt in ["Page", "Workspace"]:
        filters = {"parent": dt, "role": "Strictly Limited Role"}
        if not frappe.db.exists("Custom DocPerm", filters):
            frappe.get_doc({
                "doctype": "Custom DocPerm",
                "parent": dt,
                "role": "Strictly Limited Role",
                "read": 1,
                "permlevel": 0
            }).insert(ignore_permissions=True)
            print(f"Added {dt} access to Strictly Limited Role")

    frappe.db.commit()
    print("Permissions properly adjusted.")

if __name__ == "__main__":
    finally_fix_permissions()
