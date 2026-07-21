"""
Dragon Media Centre
Version Information

Central source for application name, version and build metadata.
"""

APP_NAME = "Dragon Media Centre"

APP_VERSION = "1.2"
BUILD_NUMBER = "003"

# Backward-compatible aliases used elsewhere in the project.
VERSION = APP_VERSION
BUILD = BUILD_NUMBER

VERSION_DISPLAY = f"Version {APP_VERSION} • Build {BUILD_NUMBER}"

CODENAME = "Dragon Command Center"

FOUNDER = "Peter Boulton"

DEVELOPMENT_PARTNER = "Dragon 🐉"

STATUS = "Development"

COPYRIGHT = "© 2026 Peter Boulton"

FULL_VERSION = f"{APP_NAME} {VERSION_DISPLAY}"

WINDOW_TITLE = f"{APP_NAME} - {VERSION_DISPLAY}"

ABOUT_TEXT = f"""
{APP_NAME}
{VERSION_DISPLAY}

Codename:
{CODENAME}

Founder:
{FOUNDER}

Development Partner:
{DEVELOPMENT_PARTNER}

Status:
{STATUS}

{COPYRIGHT}
"""
