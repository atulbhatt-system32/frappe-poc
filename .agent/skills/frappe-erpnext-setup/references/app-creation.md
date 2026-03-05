# Frappe App Creation & Management

This guide covers the end-to-end process of creating, configuring, and managing custom Frappe applications.

## 1. Creating a New App

Use the Bench CLI to scaffold a new application. Always run this from your bench directory.

```bash
bench new-app <app_name>
```

**Prompts during creation:**
- **App Title**: Human-readable name (e.g., "Library Management")
- **App Description**: Short summary of what the app does.
- **App Publisher**: Your name or company.
- **App Email**: Contact email.
- **App Icon**: (Optional) Default icon from Octicons or FontAwesome.
- **App License**: (Default: MIT)

### App Directory Structure

A newly created app (e.g., `my_custom_app`) follows this structure:

```
apps/my_custom_app/
├── my_custom_app/          ← Python Package
│   ├── __init__.py
│   ├── hooks.py            ← Lifecycle hooks, event handlers, and desk config
│   ├── modules.txt         ← List of modules defined in this app
│   ├── patches.txt         ← Database migration patches
│   ├── templates/          ← HTML templates for web views
│   ├── public/             ← JS, CSS, and Image assets
│   └── www/                ← Web pages (portal/website)
├── MANIFEST.in
├── README.md
├── requirements.txt
└── setup.py
```

---

## 2. Installing the App on a Site

 Scaffolding an app doesn't automatically install it. You must explicitly install it on your target site.

```bash
bench --site <site_name> install-app <app_name>
```

Verify the installation:
```bash
bench --site <site_name> list-apps
```

---

## 3. Developer Mode

If you are creating new DocTypes or modifying existing ones, you **MUST** enable `developer_mode`. Without it, DocType changes are only saved in the database and not written to your app's source code.

```bash
bench set-config -g developer_mode 1
```

---

## 4. Key Configuration: hooks.py

`hooks.py` is the most important file in your app. It defines how your app interacts with the Frappe Framework.

Commonly used hooks:
- `app_include_js`: Include global JS files.
- `app_include_css`: Include global CSS files.
- `doctype_js`: Inject JS into specific DocTypes.
- `doc_events`: Server-side triggers (e.g., `before_insert`, `on_update`).
- `scheduler_events`: Cron-like tasks.
- `fixtures`: Export data (like Custom Fields, Custom Scripts) to JSON for version control.

---

## 5. Fixtures: Managing Custom Data

Fixtures allow you to export data stored in the database (which isn't tracked by Git) into files in your app.

**Defining fixtures in `hooks.py`:**
```python
fixtures = [
    {"dt": "Custom Field", "filters": [["module", "=", "My Module"]]},
    {"dt": "Property Setter", "filters": [["module", "=", "My Module"]]}
]
```

**Exporting fixtures:**
```bash
bench --site <site_name> export-fixtures
```
This writes data to `apps/<app_name>/<app_name>/fixtures/`.

---

## 6. Best Practices

1. **Naming**: Use snake_case for the app name (`my_custom_app`).
2. **Modules**: Group related DocTypes into a single module for better organization.
3. **Avoid monkey-patching**: Use `hooks.py` and `Override Class` instead of modifying core Frappe/ERPNext files.
4. **Localization**: Use `_("Text")` in Python and `__("Text")` in JS for all user-facing strings to support translations.
5. **Testing**: Create unit tests in the `tests/` directory within your module.
