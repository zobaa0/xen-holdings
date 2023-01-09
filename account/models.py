from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from django.dispatch import receiver
from django.db.models.signals import post_save
from datetime import timedelta, datetime
from .utils import generate_ref_code


# Override Django's case-sensitive username checks
class CustomUserManager(UserManager):
    def get_by_natural_key(self, username):
        case_insensitive_username_field = '{}__iexact'.format(
            self.model.USERNAME_FIELD)
        return self.get(**{case_insensitive_username_field: username})


class CustomUser(AbstractUser):
    COUNTRIES = (
        ('', 'Choose Country'),
        ('GB', 'United Kingdom'),
        ('AF', 'Afghanistan'),
        ('AX', 'Aland Islands'),
        ('AL', 'Albania'),
        ('DZ', 'Algeria'),
        ('AS', 'American Samoa'),
        ('AD', 'Andorra'),
        ('AO', 'Angola'),
        ('AI', 'Anguilla'),
        ('AQ', 'Antarctica'),
        ('AG', 'Antigua and Barbuda'),
        ('AR', 'Argentina'),
        ('AM', 'Armenia'),
        ('AW', 'Aruba'),
        ('AU', 'Australia'),
        ('AT', 'Austria'),
        ('AZ', 'Azerbaijan'),
        ('BS', 'Bahamas'),
        ('BH', 'Bahrain'),
        ('BD', 'Bangladesh'),
        ('BB', 'Barbados'),
        ('BY', 'Belarus'),
        ('BE', 'Belgium'),
        ('BZ', 'Belize'),
        ('BJ', 'Benin'),
        ('BM', 'Bermuda'),
        ('BT', 'Bhutan'),
        ('BO', 'Bolivia'),
        ('BA', 'Bosnia and Herzegovina'),
        ('BW', 'Botswana'),
        ('BV', 'Bouvet Island'),
        ('BR', 'Brazil'),
        ('IO', 'British Indian Ocean Territory'),
        ('BN', 'Brunei Darussalam'),
        ('BG', 'Bulgaria'),
        ('BF', 'Burkina Faso'),
        ('BI', 'Burundi'),
        ('KH', 'Cambodia'),
        ('CM', 'Cameroon'),
        ('CA', 'Canada'),
        ('CV', 'Cape Verde'),
        ('KY', 'Cayman Islands'),
        ('CF', 'Central African Republic'),
        ('TD', 'Chad'),
        ('CL', 'Chile'),
        ('CN', 'China'),
        ('CX', 'Christmas Island'),
        ('CC', 'Cocos Keeling Islands'),
        ('CO', 'Colombia'),
        ('KM', 'Comoros'),
        ('CG', 'Congo'),
        ('CD', 'Congo, The Democratic Republic of the'),
        ('CK', 'Cook Islands'),
        ('CR', 'Costa Rica'),
        ('CI', 'Cote d\'Ivoire'),
        ('HR', 'Croatia'),
        ('CU', 'Cuba'),
        ('CY', 'Cyprus'),
        ('CZ', 'Czech Republic'),
        ('DK', 'Denmark'),
        ('DJ', 'Djibouti'),
        ('DM', 'Dominica'),
        ('DO', 'Dominican Republic'),
        ('EC', 'Ecuador'),
        ('EG', 'Egypt'),
        ('SV', 'El Salvador'),
        ('GQ', 'Equatorial Guinea'),
        ('ER', 'Eritrea'),
        ('EE', 'Estonia'),
        ('ET', 'Ethiopia'),
        ('FK', 'Falkland Islands Malvinas'),
        ('FO', 'Faroe Islands'),
        ('FJ', 'Fiji'),
        ('FI', 'Finland'),
        ('FR', 'France'),
        ('GF', 'French Guiana'),
        ('PF', 'French Polynesia'),
        ('TF', 'French Southern Territories'),
        ('GA', 'Gabon'),
        ('GM', 'Gambia'),
        ('GE', 'Georgia'),
        ('DE', 'Germany'),
        ('GH', 'Ghana'),
        ('GI', 'Gibraltar'),
        ('GR', 'Greece'),
        ('GL', 'Greenland'),
        ('GD', 'Grenada'),
        ('GP', 'Guadeloupe'),
        ('GU', 'Guam'),
        ('GT', 'Guatemala'),
        ('GG', 'Guernsey'),
        ('GN', 'Guinea'),
        ('GW', 'Guinea-Bissau'),
        ('GY', 'Guyana'),
        ('HT', 'Haiti'),
        ('HM', 'Heard Island and McDonald Islands'),
        ('VA', 'Holy See Vatican City State'),
        ('HN', 'Honduras'),
        ('HK', 'Hong Kong'),
        ('HU', 'Hungary'),
        ('IS', 'Iceland'),
        ('IN', 'India'),
        ('ID', 'Indonesia'),
        ('IR', 'Iran, Islamic Republic of'),
        ('IQ', 'Iraq'),
        ('IE', 'Ireland'),
        ('IM', 'Isle of Man'),
        ('IL', 'Israel'),
        ('IT', 'Italy'),
        ('JM', 'Jamaica'),
        ('JP', 'Japan'),
        ('JE', 'Jersey'),
        ('JO', 'Jordan'),
        ('KZ', 'Kazakhstan'),
        ('KE', 'Kenya'),
        ('KI', 'Kiribati'),
        ('KP', 'Korea, Democratic People\'s Republic of'),
        ('KR', 'Korea, Republic of'),
        ('KW', 'Kuwait'),
        ('KG', 'Kyrgyzstan'),
        ('LA', 'Lao People\'s Democratic Republic'),
        ('LV', 'Latvia'),
        ('LB', 'Lebanon'),
        ('LS', 'Lesotho'),
        ('LR', 'Liberia'),
        ('LY', 'Libyan Arab Jamahiriya'),
        ('LI', 'Liechtenstein'),
        ('LT', 'Lithuania'),
        ('LU', 'Luxembourg'),
        ('MO', 'Macao'),
        ('MK', 'Macedonia, The Former Yugoslav Republic of'),
        ('MG', 'Madagascar'),
        ('MW', 'Malawi'),
        ('MY', 'Malaysia'),
        ('MV', 'Maldives'),
        ('ML', 'Mali'),
        ('MT', 'Malta'),
        ('MH', 'Marshall Islands'),
        ('MQ', 'Martinique'),
        ('MR', 'Mauritania'),
        ('MU', 'Mauritius'),
        ('YT', 'Mayotte'),
        ('MX', 'Mexico'),
        ('FM', 'Micronesia, Federated States of'),
        ('MD', 'Moldova'),
        ('MC', 'Monaco'),
        ('MN', 'Mongolia'),
        ('ME', 'Montenegro'),
        ('MS', 'Montserrat'),
        ('MA', 'Morocco'),
        ('MZ', 'Mozambique'),
        ('MM', 'Myanmar'),
        ('NA', 'Namibia'),
        ('NR', 'Nauru'),
        ('NP', 'Nepal'),
        ('NL', 'Netherlands'),
        ('AN', 'Netherlands Antilles'),
        ('NC', 'New Caledonia'),
        ('NZ', 'New Zealand'),
        ('NI', 'Nicaragua'),
        ('NE', 'Niger'),
        ('NG', 'Nigeria'),
        ('NU', 'Niue'),
        ('NF', 'Norfolk Island'),
        ('MP', 'Northern Mariana Islands'),
        ('NO', 'Norway'),
        ('OM', 'Oman'),
        ('PK', 'Pakistan'),
        ('PW', 'Palau'),
        ('PS', 'Palestinian Territory, Occupied'),
        ('PA', 'Panama'),
        ('PG', 'Papua New Guinea'),
        ('PY', 'Paraguay'),
        ('PE', 'Peru'),
        ('PH', 'Philippines'),
        ('PN', 'Pitcairn'),
        ('PL', 'Poland'),
        ('PT', 'Portugal'),
        ('PR', 'Puerto Rico'),
        ('QA', 'Qatar'),
        ('RE', 'Reunion'),
        ('RO', 'Romania'),
        ('RU', 'Russian Federation'),
        ('RW', 'Rwanda'),
        ('BL', 'Saint Barthelemy'),
        ('SH', 'Saint Helena'),
        ('KN', 'Saint Kitts and Nevis'),
        ('LC', 'Saint Lucia'),
        ('MF', 'Saint Martin'),
        ('PM', 'Saint Pierre and Miquelon'),
        ('VC', 'Saint Vincent and the Grenadines'),
        ('WS', 'Samoa'),
        ('SM', 'San Marino'),
        ('ST', 'Sao Tome and Principe'),
        ('SA', 'Saudi Arabia'),
        ('SN', 'Senegal'),
        ('RS', 'Serbia'),
        ('SC', 'Seychelles'),
        ('SL', 'Sierra Leone'),
        ('SG', 'Singapore'),
        ('SK', 'Slovakia'),
        ('SI', 'Slovenia'),
        ('SB', 'Solomon Islands'),
        ('SO', 'Somalia'),
        ('ZA', 'South Africa'),
        ('GS', 'South Georgia and the South Sandwich Islands'),
        ('ES', 'Spain'),
        ('LK', 'Sri Lanka'),
        ('SD', 'Sudan'),
        ('SR', 'Suriname'),
        ('SJ', 'Svalbard and Jan Mayen'),
        ('SZ', 'Swaziland'),
        ('SE', 'Sweden'),
        ('CH', 'Switzerland'),
        ('SY', 'Syrian Arab Republic'),
        ('TW', 'Taiwan, Province of China'),
        ('TJ', 'Tajikistan'),
        ('TZ', 'Tanzania, United Republic of'),
        ('TH', 'Thailand'),
        ('TL', 'Timor-Leste'),
        ('TG', 'Togo'),
        ('TK', 'Tokelau'),
        ('TO', 'Tonga'),
        ('TT', 'Trinidad and Tobago'),
        ('TN', 'Tunisia'),
        ('TR', 'Turkey'),
        ('TM', 'Turkmenistan'),
        ('TC', 'Turks and Caicos Islands'),
        ('TV', 'Tuvalu'),
        ('UG', 'Uganda'),
        ('UA', 'Ukraine'),
        ('AE', 'United Arab Emirates'),
        ('US', 'United States'),
        ('UM', 'United States Minor Outlying Islands'),
        ('UY', 'Uruguay'),
        ('UZ', 'Uzbekistan'),
        ('VU', 'Vanuatu'),
        ('VE', 'Venezuela'),
        ('VN', 'Viet Nam'),
        ('VG', 'Virgin Islands, British'),
        ('VI', 'Virgin Islands, U.S.'),
        ('WF', 'Wallis and Futuna'),
        ('EH', 'Western Sahara'),
        ('YE', 'Yemen'),
        ('ZM', 'Zambia'),
        ('ZW', 'Zimbabwe'),
    )

    objects = CustomUserManager()
    email = models.EmailField(unique=True, max_length=30)
    phone = models.CharField(null=True, blank=True,
                             max_length=20, verbose_name='Phone number')
    address = models.CharField(null=True, blank=True, max_length=60)
    country = models.CharField(
        default="", blank=True, choices=COUNTRIES, max_length=2)
    state = models.CharField(null=True, blank=True, max_length=15)
    terms = models.BooleanField(default=False)
    del_account = models.BooleanField(
        default=False, verbose_name="Delete account")
    deactivation_duration = models.PositiveIntegerField(default=14)
    del_account_due_date = models.DateField(
        null=True, blank=True, verbose_name='Delete account due date')
    balance = models.DecimalField(
        max_digits=1000, decimal_places=2, default=0.00, verbose_name='Account balance')
    profit = models.DecimalField(
        max_digits=1000, decimal_places=2, default=0.00)
    tf_enabled = models.BooleanField(
        default=False, verbose_name='Enable Transfer')
    otp_enabled = models.BooleanField(default=False)
    otp_verified = models.BooleanField(default=False)
    otp_base32 = models.CharField(max_length=255, null=True, editable=False)
    otp_auth_url = models.CharField(max_length=255, null=True, editable=False)

    def __str__(self):
        return self.username

    @classmethod
    def deactivate_user(cls, sender, instance, created, *args, **kwargs):
        """Deactivate user account"""
        CustomUser.objects.filter(del_account=True).update(
            is_active=False,
            del_account_due_date=datetime.today() + timedelta(days=instance.deactivation_duration)
        )


post_save.connect(CustomUser.deactivate_user, sender=CustomUser)


class Referral(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    bonus = models.DecimalField(
        max_digits=100, decimal_places=2, default=0.00, verbose_name="Referral bonus")
    bonus_percent = models.DecimalField(
        max_digits=10, decimal_places=2, editable=False, default=10)
    bonus_amount = models.DecimalField(
        max_digits=10, decimal_places=2, editable=False, default=100)
    code = models.CharField(max_length=12, blank=True,
                            verbose_name="Referral code")
    recommended_by = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, null=True, blank=True, related_name='ref_by')
    # updated
    # created

    class Meta:
        verbose_name_plural = "Referral Profile"

    def __str__(self):
        return self.user.username

    def get_recommend_profiles(self):
        """Get a list of all referrals"""
        qs = Referral.objects.all()
        total_rec = [p for p in qs if p.recommended_by == self.user]
        return total_rec

    def save(self, *args, **kwargs):
        """"Override the default save method"""
        if self.code == "":
            code = self.user.username
            self.code = code
        super().save(*args, **kwargs)
