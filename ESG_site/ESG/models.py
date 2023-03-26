from django.db import models
import hashlib
# Create your models here.

class esg_reports(models.Model):   
    title = models.CharField(max_length=256, verbose_name='标题')
    edittime = models.DateTimeField(verbose_name='上传时间')
    pdf_url = models.URLField(max_length=200, verbose_name='报告URL')
    md5 = models.CharField(max_length=500, verbose_name='md5码')
    abstract = models.TextField(verbose_name='摘要')
    key_words = models.TextField(verbose_name='关键词')
    key_phrases = models.TextField(verbose_name='关键短语')
    site = models.CharField(max_length=100,verbose_name='来源网站',default="NULL")


class User(models.Model):
    name = models.CharField(max_length=20, verbose_name='用户名', null=False)
    password = models.CharField(max_length=20, verbose_name='密码', null=False)
 
    class Meta:
        verbose_name_plural = '用户'
        verbose_name = '用户'
        db_table = 'user'
 
    def save(self, *args, **kwargs):
        sha = hashlib.sha256()
        sha.update(self.password.encode())
        self.password = sha.hexdigest()
        super(User, self).save(*args, **kwargs)