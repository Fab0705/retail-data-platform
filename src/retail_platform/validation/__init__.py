from .schema_validation import SchemaValidator
from .quality_checks import QualityValidator
from .business_validation import BusinessValidator

class DataValidator:
    """Fachada unificada para ejecutar validaciones modulares."""
    def __init__(self):
        self.schema = SchemaValidator()
        self.quality = QualityValidator()
        self.business = BusinessValidator()