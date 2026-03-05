import frappe

def debug_permissions():
    frappe.init(site="mysite.localhost")
    frappe.connect()

    frappe.set_user("Administrator")
    
    # Let's see what roles testlimited has
    user = frappe.get_doc("User", "testlimited@example.com")
    print(f"Roles: {[r.role for r in user.roles]}")
    
    # See if they have access to Core module
    print(f"Blocked Modules: {[m.module for m in user.block_modules if m.module in ['Core', 'Desk']]}")
    
    # Check permissions on standard DocType 'Page'
    frappe.set_user("testlimited@example.com")
    try:
        has_perm = frappe.has_permission("Page", "read")
        print(f"Has permission for Page? {has_perm}")
    except Exception as e:
        print(f"Error checking permission: {e}")

if __name__ == "__main__":
    debug_permissions()
