import frappe

def regenerate_keys():
    frappe.init(site="mysite.localhost")
    frappe.connect()

    user_email = "testlimited@example.com"
    user = frappe.get_doc("User", user_email)
    
    # generate_keys() is a method on User that returns the secret
    # It sets api_key and api_secret (encrypted) in the DB
    api_secret = frappe.generate_hash(length=15)
    user.api_key = frappe.generate_hash(length=15)
    user.api_secret = api_secret # This gets encrypted automatically on save
    
    user.save(ignore_permissions=True)
    frappe.db.commit()
    
    print(f"API_KEY: {user.api_key}")
    print(f"API_SECRET: {api_secret}")

if __name__ == "__main__":
    regenerate_keys()
