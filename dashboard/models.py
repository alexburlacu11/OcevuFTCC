from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)


class MyUserManager(BaseUserManager):
    def create_user(self, email, firstname, lastname,laboratory,telnumber, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email), 
            firstname=firstname,
            lastname=lastname,
            laboratory=laboratory,
            telnumber=telnumber,            
            #date_of_birth=date_of_birth,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, firstname, lastname,laboratory,telnumber, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email=self.normalize_email(email),
            firstname=firstname,
            lastname=lastname,
            laboratory=laboratory,
            telnumber=telnumber,            
            #date_of_birth=date_of_birth,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user
    
    def getByEmail(self, email):     
        """
        Returns a user by searching for the e-mail
        """   
        v = MyUser.objects.get(email=email)
        return v


class MyUser(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )    
    firstname = models.CharField(max_length=20)
    lastname = models.CharField(max_length=20)
    laboratory = models.CharField(max_length=20)
    telnumber = models.CharField(max_length=20)
    address = models.TextField()
    AFFILIATION = (
    ('France', 'France'),
    ('Mexico', 'Mexico'),
    ('Other', 'Other'),    
    )   
    affiliation = models.CharField(max_length=20, choices=AFFILIATION)
    url = models.CharField(max_length=200)
    joined = models.DateTimeField(auto_now_add=True)    
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    ADMIN_LEVEL = (
    ('User', '0'),
    ('Scientific_Manager', '1'),
    ('Administrator', '2'),    
    )   
    level_admin = models.IntegerField(max_length=20, choices=ADMIN_LEVEL, default=0)     
    last_connect = models.DateTimeField(auto_now_add=True)    
    valid_from = models.DateTimeField(auto_now_add=True)    
    valid_to = models.DateTimeField(auto_now_add=True) 
    valid_instrument_from = models.DateTimeField(auto_now_add=True) 
    valid_instrument_to = models.DateTimeField(auto_now_add=True) 
    quota_theorique = models.IntegerField(default=0)     
    quota_already_consumed = models.IntegerField(default=0)  
    priority_user = models.IntegerField(default=0)  
    priority_img_proc = models.IntegerField(default=0)  
    
    
    """ 
             
    admin fields:
    quota_theorique - percentage or nb of seconds (meme que le quota de requete) 40 000 seconds dans une nuit
    quota_already_consumed - from the beginning of the year (cumulated)
    priority_user - default priority for requests
    priority_proc - priority for image processing
    
    --- check definition of plan sequence album ---
    ( 10 jours max pour une requete )
    ( 100 sequences in a request , 20  min for a seq max ) 
    ( 3 albums in a sequence )
    ( 42 plans in an album )
    ( 1.4 sec for an image )
    ( using math find out number max of plans and images )
    simulation in request form returns a warning
    validation -> we also call the simulator
    
    
    instrument infrargouge :
     optique derierre 
     filtre a l interieur du cryostat
     interieur du cyostat = pas de dark
     
     etude optique
     etude experimentale
     etude mecanique
     
     logiciel de pilotage cagire:
     filtre, dithering, acq donees, formatage des fichiers avec info concernant l instrument
     
     tests d interface :
     1 int avec telescope
     1 simple miroire 
     tests sur camera proche infrarouge
     GSE = ground support equipment
     
     data product = analyse de donnes
     donc on fait d archivage
     client leger icy et de travailler sur place
     
     cloud pour archivage ? -> open nebula
     
     IDLE or reset ? - automatic mangamenet  ?
     
     implication sur le plan logiciel 
     
     dithering and saturation
     
     reception d alarme de la part cagire
     
     sur le telescope tbl:
     etage de c and c 
     
     ordinateur present dans les tests
     interface camera visible & infrarouge les memes et sur d autres cameras pour le faire leplus generique possible
     meta grammaire - grammaire generique  - semantic web
        
        objet
        
     demare un document sur les interfaces
     filtres froids et chauds et le dithering et la mecanique de lentiles qui bougent
     contraintes optiques -> contraintes mecaniques
     
     change filtre pendent le dithering ?
     int : acq donnees et gestion des alertes
     alertes hardware -> somethingwnet wrong 
     
     datation des images
     pps
     arduino - fpga
     
     1. cloud for storage
     2. arduino fpga
     
     
     interfacage avec instruments
     
     oft cagire 3 23 juin
         
    
    """

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['firstname', 'lastname','laboratory','telnumber']

    def get_full_name(self):
        # The user is identified by their email address
        return self.email

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    # On Python 3: def __str__(self):
    def __unicode__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin