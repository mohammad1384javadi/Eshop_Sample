from django.db import models


# Create your models here.


class SiteSetting(models.Model):
    site_name = models.CharField(max_length=300, verbose_name='نام سایت')
    site_url = models.CharField(max_length=300, verbose_name='دامنه سایت')
    addres = models.CharField(max_length=300, verbose_name='آدرس', blank=True, null=True)
    phone = models.CharField(max_length=300, verbose_name='تلفن', blank=True, null=True)
    fax = models.CharField(max_length=300, verbose_name='فکس', null=True, blank=True)
    email = models.CharField(max_length=300, verbose_name='ایمیل')
    about_us_text = models.TextField(verbose_name='متن درباره ما')
    copyright_text = models.TextField(verbose_name='متن کپی رایت')
    site_logo = models.ImageField(verbose_name='تصویر', upload_to='images/site_setting')
    is_main_setting = models.BooleanField(verbose_name='تنظیمات اصلی')
    is_active = models.BooleanField(verbose_name='فعال / غیرفعال', default=True)

    def __str__(self):
        return self.site_name

    class Meta:
        verbose_name = 'تنظیمات سایت'
        verbose_name_plural = 'تنظیمات'


class FooterLinkBox(models.Model):
    title = models.CharField(max_length=300, verbose_name='دسته بندی لینک')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'دسته بندی لینک های فوتر'
        verbose_name_plural = 'دسته بندی های لینک های فوتر'


class FooterLink(models.Model):
    title = models.CharField(max_length=300, verbose_name='عنوان لینک')
    url = models.URLField(max_length=500, verbose_name='آدرس لینک')
    footer_link_box = models.ForeignKey(FooterLinkBox, on_delete=models.CASCADE, verbose_name='دسته بندی لینک')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'لینک فوتر'
        verbose_name_plural = 'لینک های فوتر'


class Slider(models.Model):
    title = models.CharField(max_length=300, verbose_name='عنوان')
    url = models.URLField(max_length=500, verbose_name='لینک اسلایدر')
    url_title = models.CharField(max_length=300, verbose_name='عنوان لینک')
    image = models.ImageField(verbose_name='تصویر', upload_to='images/sliders')
    description = models.TextField(verbose_name='توضیحات اسلایدر')
    is_active = models.BooleanField(default=True, verbose_name='فعال / غیرفعال')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'اسلایدر'
        verbose_name_plural = 'اسلایدرها'


class SiteBanner(models.Model):
    class SiteBannerPositions(models.TextChoices):
        product_list = 'product_list', 'صفحه لیست محصولات'
        product_detail = 'product_detail', 'صفحه جزییات محصولات'
        about_us = 'about_us', 'صفحه درباره ما'

    title = models.CharField(max_length=300, verbose_name='عنوان بنر')
    url = models.URLField(max_length=450, verbose_name='آدرس بنر', null=True, blank=True)
    image = models.ImageField(upload_to='images/banners', verbose_name='تصویر بنر')
    is_active = models.BooleanField(verbose_name='فعال/غیرفعال')
    position = models.CharField(max_length=400, choices=SiteBannerPositions.choices, verbose_name='مکان قرارگیری بنر')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'بنر تبلیغاتی'
        verbose_name_plural = 'بنرهای تبلیغاتی'
