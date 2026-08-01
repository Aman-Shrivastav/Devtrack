from django.core.management.base import BaseCommand

from api.models import KBEntry


KB_ENTRIES = [
    ("What is select_related in Django ORM?", "select_related follows foreign-key relationships with a SQL JOIN so related objects can be read without extra queries.", "database"),
    ("When should I use prefetch_related?", "Use prefetch_related for many-to-many or reverse relations. Django performs separate queries and joins the results in Python.", "database"),
    ("How does transaction.atomic() work?", "transaction.atomic creates an all-or-nothing database transaction. An exception rolls back the work inside its block.", "database"),
    ("What is a JWT token?", "A JSON Web Token is a signed credential that lets an API verify an authenticated user on later requests.", "api"),
    ("When should I use Q objects?", "Use Q objects when a Django query needs OR conditions, negation, or dynamically composed filters.", "database"),
    ("What does a REST API do?", "A REST API exposes resources through HTTP methods and standard response codes.", "api"),
    ("How do database indexes help?", "Indexes speed up reads for indexed lookups, but add storage and write overhead.", "database"),
    ("What is container orchestration?", "Container orchestration automates deployment, scaling, and lifecycle management of containers across machines.", "cloud"),
    ("What is Django middleware?", "Django middleware is a framework of hooks that processes requests and responses globally.", "framework"),
    ("How should API errors be handled?", "Return a suitable HTTP status code and a stable, useful error payload that clients can handle predictably.", "general"),
]


class Command(BaseCommand):
    help = "Seed the TeamBoard knowledge base with sample Q&A entries."

    def handle(self, *args, **options):
        created_count = 0
        for question, answer, category in KB_ENTRIES:
            _, created = KBEntry.objects.get_or_create(
                question=question,
                defaults={"answer": answer, "category": category},
            )
            created_count += created

        self.stdout.write(self.style.SUCCESS(f"Knowledge base seeded: {created_count} entries created."))
