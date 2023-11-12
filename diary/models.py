from django.db import models

# Create your models here.
class Record(models.Model):
    pressure_high=models.IntegerField()
    pressure_lower=models.IntegerField()
    pulse=models.IntegerField()
    timestamp=models.DateTimeField()
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    
    def __str__(self) -> str:
        return "{} / {} - {} at {}".format(self.pressure_high, self.pressure_lower, self.pulse, self.timestamp)