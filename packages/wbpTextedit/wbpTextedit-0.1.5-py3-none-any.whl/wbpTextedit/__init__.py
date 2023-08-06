from .template import PlainTextTemplate
from .config import TextEditPreferences, PlainTextPreferences
from .template.python import PythonTextTemplate, PythonTextPreferences
from .template.xml import XMLTextTemplate, XMLTextPreferences
from .template.ini import IniTextTemplate, IniTextPreferences


__version__ = "0.1.5"

doctemplates = (PlainTextTemplate, PythonTextTemplate, XMLTextTemplate, IniTextTemplate)

preferencepages = (
    TextEditPreferences,
    PlainTextPreferences,
    PythonTextPreferences,
    XMLTextPreferences,
    IniTextPreferences,
)
