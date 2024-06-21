from django.shortcuts import redirect, render, get_object_or_404
from django.views import View
from django.db.models import Q
from .models import Message, UserMessage  # Veritabanı modellerini import ediyoruz
from .forms import MessageForm, UserMessageForm  # Formları import ediyoruz
from users.models import CustomUser  # Kullanıcı modelini import ediyoruz
from django.contrib.auth.decorators import login_required  # Giriş zorunluluğu decorator'ı

# Ana sayfa görünümü
def home(request):
    users = CustomUser.objects.all()  # Tüm kullanıcıları alıyoruz
    return render(request, 'home.html', {'users': users})  # 'home.html' şablonunu kullanarak kullanıcıları render ediyoruz

# Mesaj gönderme işlevi
@login_required  # Giriş zorunlu
def send_message_view(request):
    if request.method == 'POST':  # İstek POST ise
        form = MessageForm(request.POST, request.FILES)  # Mesaj formunu oluştur
        if form.is_valid():  # Form geçerli ise
            message = form.save(commit=False)  # Formu kaydet, ancak veritabanına hemen kaydetme (commit=False)
            message.sender = request.user  # Gönderen olarak mevcut kullanıcıyı ayarla
            if 'attachment' in request.FILES:  # Eğer ek dosya varsa
                message.attachment = request.FILES['attachment']  # Ek dosyayı ayarla
            message.save()  # Mesajı kaydet
            return redirect('group')  # 'group' adlı URL'ye yönlendir
    else:  # İstek POST değilse
        form = MessageForm()  # Boş bir mesaj formu oluştur
    return render(request, 'send_message.html', {'form': form})  # 'send_message.html' şablonunu kullanarak formu render et

# Belirli bir kullanıcıya mesaj gönderme işlevi
@login_required  # Giriş zorunlu
def send_message_users(request, pk):
    user = get_object_or_404(CustomUser, id=pk)  # Kullanıcıyı al veya 404 hatası döndür
    if request.method == 'POST':  # İstek POST ise
        form = UserMessageForm(request.POST, request.FILES)  # Kullanıcıya mesaj formu oluştur
        if form.is_valid():  # Form geçerli ise
            message = form.save(commit=False)  # Formu kaydet, ancak veritabanına hemen kaydetme (commit=False)
            message.sender = request.user  # Gönderen olarak mevcut kullanıcıyı ayarla
            message.receiver = user  # Alıcıyı ayarla
            if 'attachment' in request.FILES:  # Eğer ek dosya varsa
                message.attachment = request.FILES['attachment']  # Ek dosyayı ayarla
            message.save()  # Mesajı kaydet
            return redirect('user_messages', pk=user.id)  # 'user_messages' adlı URL'ye yönlendir, kullanıcı kimliği ile
    else:  # İstek POST değilse
        form = UserMessageForm()  # Boş bir kullanıcı mesajı formu oluştur
    return render(request, 'send_message_to_user.html', {'form': form, 'user': user})  # 'send_message_to_user.html' şablonunu kullanarak formu render et

# Kullanıcı mesajları sınıf tabanlı görünümü
class UserMessages(View):
    def get(self, request, pk):
        user = get_object_or_404(CustomUser, id=pk)  # Kullanıcıyı al veya 404 hatası döndür
        messages = UserMessage.objects.filter(  # Kullanıcı mesajlarını filtrele
            (Q(sender=request.user) & Q(receiver=user)) | (Q(sender=user) & Q(receiver=request.user))  # Şartları uygula
        ).order_by('created_at')  # Oluşturulma zamanına göre sırala
        form = MessageForm()  # Mesaj formu oluştur
        return render(request, 'user_messages.html', {'messages': messages, 'user': user, 'form': form})  # 'user_messages.html' şablonunu kullanarak mesajları ve formu render et

    def post(self, request, pk):
        user = get_object_or_404(CustomUser, id=pk)  # Kullanıcıyı al veya 404 hatası döndür
        form = MessageForm(request.POST, request.FILES)  # Mesaj formunu oluştur
        if form.is_valid():  # Form geçerli ise
            message = form.save(commit=False)  # Formu kaydet, ancak veritabanına hemen kaydetme (commit=False)
            message.sender = request.user  # Gönderen olarak mevcut kullanıcıyı ayarla
            message.receiver = user  # Alıcıyı ayarla
            message.save()  # Mesajı kaydet
            return redirect('user_messages', pk=pk)  # 'user_messages' adlı URL'ye yönlendir, kullanıcı kimliği ile
        messages = UserMessage.objects.filter(  # Kullanıcı mesajlarını filtrele
            (Q(sender=request.user) & Q(receiver=user)) | (Q(sender=user) & Q(receiver=request.user))  # Şartları uygula
        ).order_by('created_at')  # Oluşturulma zamanına göre sırala
        return render(request, 'user_messages.html', {'messages': messages, 'user': user, 'form': form})  # 'user_messages.html' şablonunu kullanarak mesajları ve formu render et

def about_site(request):
    return render(request, 'about_site.html')  # 'about_site.html' şablonunu kullanarak sayfayı render et