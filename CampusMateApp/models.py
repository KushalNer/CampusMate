from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


YEAR_CHOICES = [
    ('1st Year', '1st Year'),
    ('2nd Year', '2nd Year'),
    ('3rd Year', '3rd Year'),
    ('4th Year', '4th Year'),
]

SEM_CHOICES = [
    ('1st Sem', '1st Sem'),
    ('2nd Sem', '2nd Sem'),
    ('3rd Sem', '3rd Sem'),
    ('4th Sem', '4th Sem'),
    ('5th Sem', '5th Sem'),
    ('6th Sem', '6th Sem'),
]

class ClassList(models.Model):
    class_name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.class_name

class Slip(models.Model):
    class_name = models.ForeignKey(ClassList, on_delete=models.SET_NULL, null=True, blank=True)
    year = models.CharField(max_length=20, choices=YEAR_CHOICES)
    sem = models.CharField(max_length=20, choices=SEM_CHOICES, null=True, blank=True)
    title = models.CharField(max_length=100)
    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.title} ({self.class_name} - {self.year})"


class SlipQuestion(models.Model):
    slip = models.ForeignKey(Slip, on_delete=models.CASCADE, related_name='questions')
    subject = models.CharField(max_length=100)
    question_text = models.TextField()
    solution_text = models.TextField()
    explanation = models.TextField(blank=True, null=True)
    output = models.TextField(blank=True, null=True)
    marks = models.IntegerField(blank=True, null=True)
    verified = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.subject} - {self.question_text[:30]}"


CATEGORY_CHOICES = [
    ('Programming', 'Programming'),
    ('AI', 'AI'),
    ('Database', 'Database'),
    ('Cloud', 'Cloud'),
    ('Web Development', 'Web Development'), # Add existing topics to choices
    ('Data Science', 'Data Science'),
]


class ExploreTopic(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='explore_topics/', blank=True, null=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='Programming')
    link = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, default=timezone.now)
    updated_at = models.DateTimeField(blank=True)

    def __str__(self):
        return self.title

DEPARTMENT_CHOICES = [
    ('Computer Science', 'Computer Science'),
    ('Information Technology', 'Information Technology'),
    ('Electronics', 'Electronics'),
    ('Mechanical', 'Mechanical'),
    ('Civil', 'Civil'),
]

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    student_id = models.CharField(max_length=20, unique=True, blank=True, null=True)
    department = models.CharField(max_length=50, choices=DEPARTMENT_CHOICES, blank=True, null=True)
    year = models.CharField(max_length=20, choices=YEAR_CHOICES, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

    def __str__(self):
        return f'{self.user.username} Profile'


class CommunityThread(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='threads')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_solved = models.BooleanField(default=False)
    upvotes = models.PositiveIntegerField(default=0)
    views = models.PositiveIntegerField(default=0)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='Programming')

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class CommunityReply(models.Model):
    thread = models.ForeignKey(CommunityThread, on_delete=models.CASCADE, related_name='replies')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='replies')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_solution = models.BooleanField(default=False)
    upvotes = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f'Reply to {self.thread.title} by {self.author.username}'


# class Bookmark(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookmarks')
#     content_type = models.CharField(max_length=20, choices=[
#         ('slip', 'Slip Solution'),
#         ('topic', 'Explore Topic'),
#         ('thread', 'Community Thread'),
#     ])
#     content_id = models.PositiveIntegerField()
#     title = models.CharField(max_length=200)
#     url = models.URLField()
#     created_at = models.DateTimeField(auto_now_add=True)

#     class Meta:
#         ordering = ['-created_at']
#         unique_together = ['user', 'content_type', 'content_id']

#     def __str__(self):
#         return f'{self.user.username} - {self.title}'
