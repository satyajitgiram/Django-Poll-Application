from django.db import models

class Poll(models.Model):
    question = models.TextField()
    option_one = models.CharField(max_length=250,blank=True)
    option_two = models.CharField(max_length=250,blank=True)
    option_three = models.CharField(max_length=250,blank=True)
    option_four = models.CharField(max_length=250,blank=True)
    option_one_count = models.IntegerField(default=0,blank=True)
    option_two_count = models.IntegerField(default=0,blank=True)
    option_three_count = models.IntegerField(default=0,blank=True)
    option_four_count = models.IntegerField(default=0,blank=True)
    dateTime=models.DateTimeField(auto_now_add=True)

    def total(self):
        return self.option_one_count + self.option_two_count + self.option_three_count + self.option_four_count