from django.db import models

# Create your models here.
class GoodsType(models.Model):
    title = models.CharField(max_length=50,verbose_name='类型名称')
    desc = models.TextField(verbose_name='类型的描述')
    picture = models.ImageField(upload_to='static/upload/goodstype',null=True,verbose_name='类型图片')

    def to_dict(self):
        dic = {
            'title':self.title,
            'desc':self.desc,
            'picture':self.picture.__str__(),
        }
        return dic

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'goods_type'
        verbose_name = '商品类型'
        verbose_name_plural = verbose_name


class Goods(models.Model):
    title = models.CharField(max_length=50,verbose_name='商品名称')
    price = models.DecimalField(max_digits=7,decimal_places=2,verbose_name='商品价格')
    spec = models.CharField(max_length=20,verbose_name='商品规格')
    picture = models.ImageField(upload_to = 'static/upload/goods',verbose_name='商品图片')
    goodsType = models.ForeignKey(GoodsType,verbose_name='商品类型')
    isActive = models.BooleanField(default=True,verbose_name='是否上架')

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'goods'
        verbose_name = '商品'
        verbose_name_plural = verbose_name


class Users(models.Model):
    #电话号码 - CharField()
    uphone = models.CharField(max_length=11,verbose_name='电话号码')
    #密码 - CharField()
    upwd = models.CharField(max_length=30,verbose_name="密码")
    #用户邮箱 - EmailField()
    uemail = models.EmailField(verbose_name="电子邮件")
    #用户名 - CharField()
    uname = models.CharField(max_length=30,verbose_name="用户名")
    #启用/禁用 - BooleanField(）
    isActive = models.BooleanField(default=True,verbose_name="启用/禁用")

    def __str__(self):
        return self.uname

    def __repr__(self):
        return "<User:%r>"%self.uname

    class Meta:
        db_table = "users"
        verbose_name = '用户'
        verbose_name_plural = verbose_name

class CartInfo(models.Model):
    #关联关系：关联Users实体（一）
    user = models.ForeignKey(Users)
    #关联关系：关联Goods实体（一）
    good = models.ForeignKey(Goods)
    #商品数量
    count = models.IntegerField()

    class Meta:
        db_table = "cartinfo"







