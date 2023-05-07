from django.db import models
from django.contrib.auth.models import User
from django_quill.fields import QuillField

# Create your models here.
class UserAccount(models.Model):
    user  = models.OneToOneField(User,on_delete=models.CASCADE)
    phone = models.CharField(max_length=12,null=True,default="")
    city = models.CharField(max_length=30,null=True,default="")
    state = models.CharField(max_length=30,null=True,default="")
    country = models.CharField(max_length=30,null=True,default="")
    address = models.CharField(max_length=400,null=True,default="")
    def __str__(self):
        return self.user.username

class Post(models.Model):
    # username = models.OneToOneField(User,on_delete=models.CASCADE)
    username = models.ForeignKey(UserAccount,on_delete=models.CASCADE)
    timeposted = models.TimeField()
    title = models.CharField(primary_key=True,max_length=80,null=False,default="")
    desc = QuillField(default='ici')
    def __str__(self):
        return self.username.user.username
# commentnew = Comment.object.create(postedwhere = Post.objects.filter(username = UserAccount.objects.filter(user=User.objects.filter(username='khushi')[0])[0]))


class Comment(models.Model):
    postedwhere = models.ForeignKey(Post,on_delete=models.CASCADE)
    userwhoposted = models.ForeignKey(UserAccount,on_delete=models.CASCADE)
    content = models.TextField()
    timeposted = models.TimeField()
    # commentedoncomment
    def __str__(self):
        return self.postedwhere.username.user.username


class Reply(models.Model):
    commentwhereposted = models.ForeignKey(Comment,on_delete=models.CASCADE)
    userwhoposted = models.ForeignKey(UserAccount,on_delete=models.CASCADE)
    content = models.TextField()
    timeposted = models.TimeField()
    # userwhomentioned = models.ForeignKey(UserAccount,on_delete=models.CASCADE)
    def __str__(self):
        return self.commentwhereposted.postedwhere.username.user.username

class OTPStorage(models.Model):
    username = models.ForeignKey(UserAccount,on_delete=models.CASCADE)
    otphere = models.CharField(max_length=6,null=False)
    timecreation = models.TimeField()
    timevalid = models.TimeField()
    def __str__(self):
        return self.username.user.username
    # def add_comment(objj:Comment):
    #     try:
    #         OTPStorage.comments.append(objj)
    #         return True
    #     except:
    #         return False

# class Followers(models.Model):
#     person = models.ForeignKey(UserAccount,on_delete=models.CASCADE)
#     followedby = models.ForeignKey(User,on_delete=models.CASCADE)
#     def __str__(self):
#         return self.person.user.username

class Following(models.Model):
    person = models.ForeignKey(UserAccount,on_delete=models.CASCADE)
    userfollowed = models.ForeignKey(User,on_delete=models.CASCADE)
    def __str__(self):
        return self.person.user.username
    
# class Meta:
#     unique_together = (('person','userfollowed'))
# class Meta:
#     constraints = [
#         models.UniqueConstraint(
#             fields=['person', 'userfollowed'], name='unique_migration_host_combination'
#         )
#     ]
    