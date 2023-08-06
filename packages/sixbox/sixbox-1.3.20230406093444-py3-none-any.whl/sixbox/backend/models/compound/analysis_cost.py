from sixbox.backend.meta.resource import Resource
from sixbox.backend.meta.fields import StringField, CompoundField
from sixbox.backend.models.compound.analysis_cost_breakdown import (
    AnalysisCostBreakdown
)


class AnalysisCost(Resource):
    """
    AnalysisCost resource contains an information regarding the currency, the
    monet value and breakdown of a analysis cost.
    """
    currency = StringField(read_only=True)
    amount = StringField(read_only=True)
    breakdown = CompoundField(AnalysisCostBreakdown, read_only=True)

    def __str__(self):
        return (
            f'<AnalysisCost: currency={self.currency}, '
            f'amount={self.amount}>'
        )
