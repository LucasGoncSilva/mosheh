from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


def index(r: HttpRequest) -> HttpResponse:
    free_plan: list[str] = [
        'Store up to 5 Credentials',
        'Store up to 5 Payment Cards',
        'Store up to 5 Security Notes',
    ]

    free_plan_disabled: list[str] = [
        'No Temporary Sharing',
        'No access to Organizations',
        'No local exporting',
    ]

    monthly_plan: list[str] = [
        'Unlimited Credentials',
        'Unlimited Payment Cards',
        'Unlimited Security Notes',
        'Temporary Sharing',
        'Access to Organizations',
        'Local exporting via JSON file',
    ]

    annual_plan: list[str] = [
        'Everything from Monthly Plan',
        '16% cheaper',
        'No worries for renewal soon',
    ]

    return render(
        r,
        'plans/index.html',
        {
            'free': free_plan,
            'free_disabled': free_plan_disabled,
            'monthly': monthly_plan,
            'annual': annual_plan,
        },
    )
