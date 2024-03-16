from datetime import datetime, timedelta
import random

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils.timezone import make_aware
from faker import Faker

from core.models import Event, UserEventRegistration

class Command(BaseCommand):
    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting database population...'))

        faker = Faker()

        for i in range(10):
            first_name = faker.first_name()
            last_name = faker.last_name()
            User.objects.create_user(username=f'user{i}',
                                     email=f'user{i}@example.com',
                                     password='password',
                                     first_name=first_name,
                                     last_name=last_name)

        event_names = [
            'Django for Beginners',
            'Python Data Science Meetup',
            'React Native Workshop',
            'Machine Learning Basics',
            'Introduction to IoT',
            'Blockchain 101',
            'Advanced Django Techniques',
            'Full-stack Development with Python and JavaScript',
            'Mobile App Development Trends',
            'Cybersecurity Fundamentals',
        ]

        descriptions = [
            'Learn Django with hands-on examples.',
            'Explore data science techniques using Python.',
            'Build your first React Native app.',
            'An introduction to machine learning concepts.',
            'Getting started with the Internet of Things.',
            'Understanding blockchain technology.',
            'Deep dive into Django features.',
            'Learn full-stack development from front to back.',
            'What\'s new in mobile app development.',
            'Protect your digital assets with cybersecurity basics.',
        ]
        
        image_urls = [
          'https://circumeo.io/static/images/server-racks.png',
          'https://circumeo.io/static/images/typewriter.jpg',
          'https://circumeo.io/static/images/library.jpg',
          'https://circumeo.io/static/images/landscape.jpg',
          'https://circumeo.io/static/images/laptop.jpg',
          'https://circumeo.io/static/images/latte.jpg',
        ]

        for name, description in zip(event_names, descriptions):
            image_url = random.choice(image_urls)
            
            event_date = datetime.now() + timedelta(days=random.randint(1, 90))
            event_time = datetime.now().time()
            
            Event.objects.create(name=name, description=description, image_url=image_url, event_date=make_aware(event_date), event_time=event_time)

        users = list(User.objects.all())
        events = list(Event.objects.all())
        for user in users:
            for event in random.sample(events, k=random.randint(1, 5)):
                UserEventRegistration.objects.create(user=user, event=event)

        self.stdout.write(self.style.SUCCESS('Database population completed successfully!'))