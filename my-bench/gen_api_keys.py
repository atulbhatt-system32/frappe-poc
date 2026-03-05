import frappe
from frappe.utils.password import update_password

def setup_api_credentials():
    frappe.init(site="mysite.localhost")
    frappe.connect()

    user_email = "testlimited@example.com"
    user = frappe.get_doc("User", user_email)
    
    # Generate API Key if not exists
    if not user.api_key:
        api_key = frappe.generate_hash(length=15)
        user.api_key = api_key
        user.save(ignore_permissions=True)
    else:
        api_key = user.api_key
        
    # Generate API Secret (this requires update_password or manual db set because api_secret is a Password field)
    api_secret = "secret123"
    frappe.db.set_value("User", user_email, "api_secret", api_secret)
    
    frappe.db.commit()
    print(f"API_KEY: {api_key}")
    print(f"API_SECRET: {api_secret}")

if __name__ == "__main__":
    setup_api_credentials()
