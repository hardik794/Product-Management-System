from django.db import models

# Create your models here.

class Company_Details(models.Model):
    c_name = models.CharField(default="",max_length=200)
    c_email = models.EmailField(default="",max_length=200)
    c_cno = models.CharField(default="",max_length=50)
    c_add = models.TextField(default="")
    join_date = models.DateField(auto_now=True,blank=True,null=True)
    profile = models.ImageField(upload_to="Com_Prof/",max_length=300,default="",blank=True,null=True) 
    c_pass = models.CharField(default="",max_length=200)

    def __str__(self):
        return self.c_name
    

class Company_Customers(models.Model):
    comp=models.ForeignKey('Company_Details',on_delete=models.CASCADE,blank=True,null=True)
    cust_nm = models.CharField(default="",max_length=200)
    cust_em = models.EmailField(default="",max_length=200)
    cust_con = models.CharField(default="",max_length=50)
    cust_add1 = models.TextField(default="")
    cust_add2 = models.TextField(default="")
    cust_pass = models.CharField(default="",max_length=200)
    regi_date = models.DateField(auto_now_add=True,blank=True,null=True)
    cust_profile = models.ImageField(upload_to="Cust_Pic/",max_length=300,default="",blank=True,null=True) 

    def __str__(self):
        return self.cust_nm

class Company_Product(models.Model):
    comp=models.ForeignKey('Company_Details',on_delete=models.CASCADE,blank=True,null=True)
    prod_nm = models.CharField(default="",max_length=200)
    prod_price = models.PositiveIntegerField(default=0)
    prod_qty = models.PositiveIntegerField(default=0)
    prod_img = models.ImageField(upload_to="ProductPic/",max_length=300,default="",blank=True,null=True) 

    def __str__(self):
        return self.prod_nm


class Customer_Order(models.Model):
    comp = models.ForeignKey('Company_Details',on_delete=models.CASCADE,blank=True, null=True)
    cust = models.ForeignKey('Company_Customers',on_delete=models.CASCADE,blank=True, null=True)
    prod = models.ForeignKey('Company_Product',on_delete=models.CASCADE,blank=True, null=True)
    qty = models.PositiveIntegerField(default=0)    
    tot_price = models.PositiveIntegerField(default=0)
    order_date = models.DateTimeField(auto_now_add=True,blank=True, null=True)
    status = models.CharField(default="False",max_length=200)

    def __str__(self):
        return self.prod