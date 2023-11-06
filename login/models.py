from django.db import models
from crypt_tools.cert.elgamal import elgamal

# Create your models here.

class Account(models.Model):
    password = models.CharField(max_length=200)
    name = models.CharField(max_length=30)
    email = models.CharField(max_length=60)


    def is_authenticated(self, msg, Sig):
        res = Account.objects.get(name=self.name)
        asymc = res.asymc
        au_elgamal = elgamal()
        au_elgamal.p, au_elgamal.g, au_elgamal.y = res.p, res.g, res.y
        return au_elgamal.verify(msg, Sig)

