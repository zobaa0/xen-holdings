from django.contrib.sites.shortcuts import get_current_site

from .models import Site


def get_site_details(request):
    current_site = get_current_site(request)
    siteURL = current_site.domain
    protocol = 'https' if request.is_secure() else 'http'
    
    address = ''
    siteName = ''
    year = ''
    phone = ''
    email = ''
    founder = ''
    btc = ''
    eth = ''
    usdt = ''

    for i in Site.objects.all():
        address = i.address
        siteName = i.name
        year = i.year
        phone = i.phone
        email = i.email
        founder = i.founder
        btc = i.btc
        eth = i.eth
        usdt = i.usdt

    context = {
        'siteName': siteName, 'siteURL': siteURL, 'address': address, 'year': year,
        'email': email, 'phone': phone, 'founder': founder, 'btc': btc, 'eth': eth,
        'usdt': usdt, 'protocol': protocol
    }
    return context
