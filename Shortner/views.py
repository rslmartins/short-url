from django.shortcuts import render
from django.contrib import messages
from django.utils.safestring import mark_safe
from rest_framework.response import Response
from . models import URLData
from . forms import URLDataForm
from . serializers import URLDataSerializers
from django.shortcuts import redirect
import string
import random

#Declare Key Varaibles
BASE_LIST='0123456789abcdefghijklmnopqrstuvwxyz./:'
BASE_DICT=dict((c,idx) for idx,c in enumerate(BASE_LIST))
host='127.0.0.1'
port = ':8000'

#Convert ID to FullURL
def base_encode(integer, alphabet=BASE_LIST): 
    if integer == 0:
        return alphabet[0]
    arr = []
    base = len(alphabet)
    while integer:
        integer, rem = divmod(integer, base)
        arr.append(alphabet[rem])
    arr.reverse()
    return ''.join(arr)

#Convert Full URL to ID
def base_decode(request, reverse_base=BASE_DICT): 
    longurl=request
    length = len(reverse_base)
    ret = 0
    for i, c in enumerate(longurl[::-1]):
        ret += (length ** i) * reverse_base[c]
    return ret

#Get Shortened URL endpoint
def shortChars(): 
    SHORT_LIST_CHAR='0123456789'+string.ascii_letters
    return ''.join([random.choice(SHORT_LIST_CHAR) for i in range(10)])

def create_url(ID):
    sc=str(shortChars())
    Retreived_IDs=list(URLData.objects.values_list('URLID', flat=True))
    if str(ID) in Retreived_IDs:
        surl=URL_ID=URLData.objects.all().filter(URLID=str(ID))[0].ShortURL
        mess=('Record Already Exists: <a href = http://{}{}/{}> Shortened Link </a>'.format(host,port,surl))
    else:
        U=URLData(URLID=ID, ShortURL=sc)
        U.save()
        mess=('Congratulatons: <a href = http://{}{}/{}> Shortened Link </a>'.format(host,port,sc))
    return mess

def redirect_short_url(request, short_url):
    redirect_url = host+'/shorten'
    try:
        URL_ID=URLData.objects.all().filter(ShortURL=short_url)[0].URLID
        redirect_url = base_encode(int(URL_ID))
    except Exception as e:
        print (e)
    return redirect(redirect_url)   

def appendPrefix(entry):
    match=['http','https']
    if any(x in entry for x in match):
        return entry
    else:
        return('https://'+str(entry))

def get_form(request):
    if request.method=='POST':
        form=URLDataForm(request.POST)
        if form.is_valid():
            fullurl=form.cleaned_data['EnterURL']
            fullurladj=appendPrefix(fullurl)
            ID=base_decode(fullurladj.lower())
            messages.info(request, mark_safe('{}'.format(create_url(ID))))
    form=URLDataForm()
    return render(request, 'myform/form.html', {'form':form})

