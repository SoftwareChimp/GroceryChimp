from django.db import models


class Delivery(models.Model):
    driver_id = models.IntegerField(primary_key=True)    
    order_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Delivery'


class Driver(models.Model):
    driver_id = models.CharField(primary_key=True, max_length=5)
    driver_first = models.CharField(max_length=20, blank=True, null=True)
    driver_last = models.CharField(max_length=20, blank=True, null=True)
    driver_email = models.CharField(max_length=30, blank=True, null=True)
    rating = models.IntegerField(blank=True, null=True)
    driver_phone = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Driver'


class Inventory(models.Model):
    store_id = models.CharField(primary_key=True, max_length=5)
    product_id = models.CharField(max_length=5)
    stock = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Inventory'
        unique_together = (('store_id', 'product_id'),)


class Order(models.Model):
    order_id = models.CharField(primary_key=True, max_length=5)
    user_id = models.CharField(max_length=5)
    store_id = models.CharField(max_length=5)
    product_id = models.CharField(max_length=5)
    driver_id = models.CharField(max_length=5)
    quantity = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'Order'
        unique_together = (('order_id', 'user_id', 'store_id', 'product_id', 'driver_id'),)


class PaymentInfo(models.Model):
    payment_id = models.CharField(primary_key=True, max_length=5)
    user_id = models.CharField(max_length=5)
    card_company = models.TextField(blank=True, null=True)
    card_number = models.IntegerField(blank=True, null=True)
    card_expiration = models.DateField(blank=True, null=True)
    card_ccv = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Payment Info'
        unique_together = (('payment_id', 'user_id'),)


class Products(models.Model):
    product_id = models.CharField(primary_key=True, max_length=5)
    product_name = models.TextField(blank=True, null=True)
    price = models.FloatField(blank=True, null=True)
    type = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Products'


class ShoppingCart(models.Model):
    cart_id = models.AutoField(primary_key=True)
    user_id = models.CharField(max_length=5)
    product_id = models.CharField(max_length=5)
    quantity = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Shopping Cart'


class Stores(models.Model):
    store_id = models.CharField(primary_key=True, max_length=5)
    store_name = models.TextField(blank=True, null=True)
    store_address = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Stores'


class Transactions(models.Model):
    transaction_id = models.CharField(primary_key=True, max_length=5)
    user_id = models.CharField(max_length=5)
    order_id = models.CharField(max_length=5)
    transaction_date = models.DateField(blank=True, null=True)
    transaction_price = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Transactions'
        unique_together = (('transaction_id', 'user_id', 'order_id'),)


class User(models.Model):
    user_id = models.CharField(primary_key=True, max_length=5)
    user_name = models.TextField(blank=True, null=True)
    user_password = models.TextField(blank=True, null=True)
    user_first = models.TextField(blank=True, null=True)
    user_last = models.TextField(blank=True, null=True)
    permission = models.IntegerField(blank=True, null=True)
    user_address = models.TextField(blank=True, null=True)
    user_email = models.CharField(max_length=25, blank=True, null=True)
    user_phone = models.CharField(max_length=14, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'User'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class StoresdisplayStores(models.Model):       
    store_id = models.CharField(max_length=100)
    name = models.CharField(max_length=100)    
    address = models.TextField()
    nearby = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'storesdisplay_stores' 