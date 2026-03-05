import frappe

def fix_workspace_crash():
    frappe.init(site="mysite.localhost")
    frappe.connect()

    email = "testlimited@example.com"
    user = frappe.get_doc("User", email)

    # 1. Clear blocked modules as they can brutally break Frappe v15+ routing natively depending on the module.
    # Security is already handled by Role Profiles / Document Permissions - because the user ONLY
    # has 'Strictly Limited Role', they will ONLY see what 'Strictly Limited Role' has access to (Test Entity).
    user.set("block_modules", [])
    
    # 2. Make sure the 'Limited Workspace' is explicitly set as the Home Page
    user.home_page = "workspace/Limited Workspace"
    
    user.save(ignore_permissions=True)
    
    frappe.db.commit()
    print("User block_modules cleared and home_page set.")

if __name__ == "__main__":
    fix_workspace_crash()
