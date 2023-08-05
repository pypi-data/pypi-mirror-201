from sixbox.backend.meta.resource import Resource
from sixbox.backend.models.compound.price import Price
from sixbox.backend.models.compound.billing.project_breakdown import (
    ProjectBreakdown
)
from sixbox.backend.meta.fields import (
    HrefField, CompoundListField, CompoundField
)


class BillingGroupBreakdown(Resource):
    """
    Central resource for managing billing group breakdowns.
    """
    _URL = {
        'get': '/billing/groups/{id}/breakdown'
    }

    href = HrefField(read_only=True)
    project_breakdown = CompoundListField(ProjectBreakdown, read_only=True)
    total_spending = CompoundField(Price, read_only=True)

    def __str__(self):
        return '<BillingGroupBreakdown>'
