from django.db import models

# Create your models here.


class Site(models.Model):
    name = models.CharField(
        max_length=30, verbose_name="Site name", default='siteName')
    website = models.CharField(
        max_length=30, verbose_name="Website URL", null=True, blank=True)
    address = models.CharField(
        max_length=50, verbose_name="Company address", null=True, blank=True)
    phone = models.CharField(
        max_length=20, verbose_name="Company number", null=True, blank=True)
    email = models.EmailField(
        max_length=30, verbose_name="Company email", null=True, blank=True)
    founder = models.CharField(
        max_length=30, verbose_name="Company founder", null=True, blank=True)
    logo = models.ImageField(upload_to="main/", null=True, blank=True)
    year = models.CharField(max_length=15, null=True, blank=True)
    btc = models.CharField(max_length=60, null=True,
                           verbose_name='Bitcoin address', blank=True)
    eth = models.CharField(max_length=60, null=True,
                           verbose_name='Ethereum address', blank=True)
    usdt = models.CharField(max_length=60, null=True,
                            verbose_name='USDT address', blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Site Features'


class Testimony(models.Model):
    """Model definition for Testimony."""

    # TODO: Define fields here
    name = models.CharField(max_length=20)
    title = models.CharField(max_length=20, default='Client')
    description = models.TextField()
    image = models.ImageField(upload_to='testimonies/', null=True, blank=True)

    class Meta:
        """Meta definition for Testimony."""

        verbose_name = 'Testimony'
        verbose_name_plural = 'Testimonies'

    def __str__(self):
        """Unicode representation of Testimony."""
        return self.name
