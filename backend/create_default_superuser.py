from django.contrib.auth import get_user_model
User = get_user_model()

User.objects.filter(username="sa").exists() or User.objects.create_superuser("sa", "sa@sa.sa", "sa")
