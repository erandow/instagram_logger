from django.core.management.base import BaseCommand
from accounts.tasks import long_running_task, my_scheduled_task


class Command(BaseCommand):
    help = 'Run Instagram tasks'

    def add_arguments(self, parser):
        parser.add_argument(
            '--async',
            action='store_true',
            help='Run the task asynchronously',
        )
        parser.add_argument(
            '--task',
            type=str,
            default='scheduled',
            choices=['long', 'scheduled'],
            help='Which task to run: "long" for long_running_task or "scheduled" for my_scheduled_task',
        )

    def handle(self, *args, **options):
        is_async = options.get('async', False)
        task_type = options.get('task', 'scheduled')
        
        if task_type == 'long':
            if is_async:
                self.stdout.write(self.style.SUCCESS('Starting long_running_task asynchronously...'))
                task = long_running_task.delay()
                self.stdout.write(self.style.SUCCESS(f'Task started with ID: {task.id}'))
            else:
                self.stdout.write(self.style.SUCCESS('Starting long_running_task synchronously...'))
                long_running_task()
                self.stdout.write(self.style.SUCCESS('Task completed'))
        else:  # scheduled
            if is_async:
                self.stdout.write(self.style.SUCCESS('Starting my_scheduled_task asynchronously...'))
                task = my_scheduled_task.delay()
                self.stdout.write(self.style.SUCCESS(f'Task started with ID: {task.id}'))
            else:
                self.stdout.write(self.style.SUCCESS('Starting my_scheduled_task synchronously...'))
                my_scheduled_task()
                self.stdout.write(self.style.SUCCESS('Task completed')) 