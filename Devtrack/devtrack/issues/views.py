import json
import os

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .models import (
    Reporter,
    Issue,
    CriticalIssue,
    LowPriorityIssue
)


# -------------------------
# Helper Functions
# -------------------------

def read_json(filename):
    """
    Reads data from a JSON file.
    Returns an empty list if file does not exist.
    """
    if not os.path.exists(filename):
        return []

    with open(filename, "r") as file:
        try:
            return json.load(file)
        except json.JSONDecodeError:
            return []


def write_json(filename, data):
    """
    Writes data to a JSON file.
    """
    with open(filename, "w") as file:
        json.dump(data, file, indent=4)


# -------------------------
# Reporter APIs
# -------------------------

@csrf_exempt
def reporters(request):

    # -----------------
    # CREATE REPORTER
    # -----------------
    if request.method == "POST":

        try:
            data = json.loads(request.body)

            reporter = Reporter(
                id=data["id"],
                name=data["name"],
                email=data["email"],
                team=data["team"]
            )

            reporter.validate()

            reporters_data = read_json("reporters.json")

            reporters_data.append(
                reporter.to_dict()
            )

            write_json(
                "reporters.json",
                reporters_data
            )

            return JsonResponse(
                reporter.to_dict(),
                status=201
            )

        except ValueError as e:

            return JsonResponse(
                {"error": str(e)},
                status=400
            )

        except KeyError as e:

            return JsonResponse(
                {"error": f"Missing field: {e}"},
                status=400
            )

        except Exception as e:

            return JsonResponse(
                {"error": str(e)},
                status=400
            )

    # -----------------
    # GET REPORTERS
    # -----------------
    elif request.method == "GET":

        reporter_id = request.GET.get("id")

        reporters_data = read_json(
            "reporters.json"
        )

        # GET REPORTER BY ID
        if reporter_id:

            try:
                reporter_id = int(reporter_id)

                for reporter in reporters_data:

                    if reporter["id"] == reporter_id:

                        return JsonResponse(
                            reporter,
                            status=200
                        )

                return JsonResponse(
                    {"error": "Reporter not found"},
                    status=404
                )

            except ValueError:

                return JsonResponse(
                    {"error": "Invalid reporter id"},
                    status=400
                )

        # GET ALL REPORTERS
        return JsonResponse(
            reporters_data,
            safe=False,
            status=200
        )

    return JsonResponse(
        {"error": "Method not allowed"},
        status=405
    )


# -------------------------
# Issue APIs
# -------------------------

@csrf_exempt
def issues(request):

    # -----------------
    # CREATE ISSUE
    # -----------------
    if request.method == "POST":

        try:

            data = json.loads(request.body)

            priority = data["priority"]

            # Polymorphism / Inheritance
            if priority == "critical":

                issue = CriticalIssue(
                    id=data["id"],
                    title=data["title"],
                    description=data["description"],
                    status=data["status"],
                    priority=data["priority"],
                    reporter_id=data["reporter_id"]
                )

            elif priority == "low":

                issue = LowPriorityIssue(
                    id=data["id"],
                    title=data["title"],
                    description=data["description"],
                    status=data["status"],
                    priority=data["priority"],
                    reporter_id=data["reporter_id"]
                )

            else:

                issue = Issue(
                    id=data["id"],
                    title=data["title"],
                    description=data["description"],
                    status=data["status"],
                    priority=data["priority"],
                    reporter_id=data["reporter_id"]
                )

            issue.validate()

            issues_data = read_json(
                "issues.json"
            )

            issues_data.append(
                issue.to_dict()
            )

            write_json(
                "issues.json",
                issues_data
            )

            response_data = issue.to_dict()

            response_data["message"] = (
                issue.describe()
            )

            return JsonResponse(
                response_data,
                status=201
            )

        except ValueError as e:

            return JsonResponse(
                {"error": str(e)},
                status=400
            )

        except KeyError as e:

            return JsonResponse(
                {"error": f"Missing field: {e}"},
                status=400
            )

        except Exception as e:

            return JsonResponse(
                {"error": str(e)},
                status=400
            )

    # -----------------
    # GET ISSUES
    # -----------------
    elif request.method == "GET":

        issue_id = request.GET.get("id")
        status_filter = request.GET.get("status")

        issues_data = read_json(
            "issues.json"
        )

        # GET ISSUE BY ID
        if issue_id:

            try:

                issue_id = int(issue_id)

                for issue in issues_data:

                    if issue["id"] == issue_id:

                        return JsonResponse(
                            issue,
                            status=200
                        )

                return JsonResponse(
                    {"error": "Issue not found"},
                    status=404
                )

            except ValueError:

                return JsonResponse(
                    {"error": "Invalid issue id"},
                    status=400
                )

        # GET ISSUES BY STATUS
        if status_filter:

            filtered_issues = []

            for issue in issues_data:

                if issue["status"] == status_filter:

                    filtered_issues.append(
                        issue
                    )

            return JsonResponse(
                filtered_issues,
                safe=False,
                status=200
            )

        # GET ALL ISSUES
        return JsonResponse(
            issues_data,
            safe=False,
            status=200
        )

    return JsonResponse(
        {"error": "Method not allowed"},
        status=405
    )