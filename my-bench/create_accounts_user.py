import frappe
from frappe.utils.password import update_password

def create_user():
    frappe.init(site="mysite.localhost")
    frappe.connect()

    email = "testaccounting@example.com"
    if not frappe.db.exists("User", email):
        user = frappe.get_doc({
            "doctype": "User",
            "email": email,
            "first_name": "Test",
            "last_name": "Accounting",
            "send_welcome_email": 0,
        })
        user.insert(ignore_permissions=True)
        
        # Add Accounts User role for limited accounting access
        user.set("roles", [])
        user.append("roles", {
            "role": "Accounts User"
        })
        user.save(ignore_permissions=True)
        
        update_password(email, "testpass123")
        frappe.db.commit()
        print(f"User created: {email} / testpass123")
    else:
        print(f"User already exists: {email}")

if __name__ == "__main__":
    create_user()
