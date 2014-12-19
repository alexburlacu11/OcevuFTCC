from django.db import models

# Create your models here.

from common.models import Agent


class SDMNController(Agent):
    
    def __init__(self):
        Agent.__init__(self, 'SDMN')