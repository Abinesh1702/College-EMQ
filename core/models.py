from django.db import models

# Create your models here.
from django.urls import reverse

class Candidate(models.Model):
    name = models.CharField(max_length=255 , null=False , blank=False)
    slogan = models.CharField(max_length=255, null=True, blank=True)
    text = models.CharField(max_length=255, null=True, blank=True)
    para1 = models.TextField(max_length=255, null=True, blank=True)
    para2 = models.TextField(max_length=255, null=True, blank=True)
    para3 = models.TextField(max_length=255, null=True, blank=True)
    para4 = models.TextField(max_length=255, null=True, blank=True)
    para5 = models.TextField(max_length=255, null=True, blank=True)
    profile_picture = models.FileField(upload_to='profile_picture/', blank=True, null=True)
    vote_count = models.IntegerField(default=0)  # New field to track votes


    def __str__(self):
        return self.name

    # Add this method to generate the candidate detail page URL
    def get_absolute_url(self):
        return reverse('candidate_detail', args=[str(self.pk)])
class Voter(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False)
    reg_no = models.CharField(max_length=20, unique=True, null=False, blank=False)  # Unique registration number
    email = models.EmailField(max_length=255, null=False, blank=False)
    has_voted = models.BooleanField(default=False)  # Track if the voter has voted


    def __str__(self):
        return self.name
# class Vote(models.Model):
#     voter = models.ForeignKey(Voter, on_delete=models.CASCADE)
#     candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
#     timestamp = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f'{self.voter.name} voted for {self.candidate.name}'
