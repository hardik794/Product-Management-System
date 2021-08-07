from django.http import HttpResponse
from django.shortcuts import render, redirect
from app1.models import Company_Details, Company_Customers,Company_Product, Customer_Order

import smtplib
import random
import email.message
# Create your views here.
# ------------------------------------- Company ---------------------


def Company_Login(request):
    if request.POST:
        em = request.POST['email']
        pass1 = request.POST['pass']
        print(em, pass1)

        try:
            var = Company_Details.objects.get(c_email=em)
            print(var)
            if var.c_pass == pass1:
                request.session['com_data'] = var.id
                return redirect('CompDashBoard')
            else:
                return HttpResponse("<h1><a href=""> You Have Entered Wrong Password </a></h1>")
        except:
            return HttpResponse("<h1><a href=""> Email Id Is Not Registered </a></h1>")
    return render(request, 'company/login/login.html')


def Company_Regi(request):
    if request.POST:
        nm = request.POST['name']
        em = request.POST['email']
        pass1 = request.POST['pass']
        pass2 = request.POST['re_pass']

        try:
            var = Company_Details.objects.get(c_email=em)
            return HttpResponse("<h1><a href=""> Email Id Already Registered... </a></h1>")
        except:
            if pass1 == pass2:
                obj = Company_Details()
                obj.c_name = nm
                obj.c_email = em
                obj.c_pass = pass2
                obj.save()
                return redirect('c_login')
    return render(request, 'company/login/regi.html')


def CompForgetPass(request):
    if request.POST:
        em1 = request.POST['em']
        try:
            valid = Company_Details.objects.get(c_email=em1)
            print(valid)

            sender_email = "memakiyapratik2001@gmail.com"
            sender_pass = '8866381041'
            reciv_email = em1

            server = smtplib.SMTP('smtp.gmail.com', 587)

            # OTP Create---------
            nos = [1, 2, 3, 4, 5, 6, 7, 8, 9, 0]
            otp = ""
            for i in range(6):
                otp += str(random.choice(nos))
                print(otp)
            print(otp)

            mes1 = f"""
            This Is Your OTP From This New Site
            {otp}


            Note:- Don't share With Others......
            """

            msg = email.message.Message()
            msg['Subject'] = "OTP From This Site"
            msg['From'] = sender_email
            msg['To'] = reciv_email
            password = sender_pass
            msg.add_header('Content-Type', 'text/html')
            msg.set_payload(mes1)

            server.starttls()
            server.login(msg['From'], password)
            server.sendmail(msg['From'], msg['To'], msg.as_string())

            request.session['otp'] = otp
            request.session['New_User'] = valid.id

            print(request.session['New_User'])
            print(request.session['otp'])
            return redirect('OTP_checker')
        except:
            return HttpResponse("<a href=''> You Have Entered Wrong Email Id </a>")
    return render(request, 'company/login/ForgetPass.html')


def OTP_checker(request):
    if 'otp' in request.session.keys():
        if request.POST:
            ot1 = request.POST['otp']
            print(ot1)
            print(request.session['otp'])
            if request.session['otp'] == ot1:
                del request.session['otp']
                return redirect('Create_NewPass')
            else:
                del request.session['otp']
                return redirect('CompForgetPass')
        return render(request, 'company/login/otp_check.html')
    else:
        return redirect('c_login')


def Create_NewPass(request):
    if 'New_User' in request.session.keys():
        if request.POST:
            p1 = request.POST['pass1']
            p2 = request.POST['pass2']
            print(p1, p2)
            if p1 == p2:
                obj = Company_Details.objects.get(
                    id=int(request.session['New_User']))
                obj.c_pass = p2
                obj.save()
                del request.session['New_User']
                return redirect('c_login')
            else:
                return HttpResponse('<a href=""> Both Passwords Are not Same </a>')
        return render(request, 'company/login/New_Pass1.html')
    else:
        return redirect('CompForgetPass')


def CompDashBoard(request):
    if 'com_data' in request.session.keys():
        comp = Company_Details.objects.get(id=int(request.session['com_data']))
        return render(request, 'company/dash/index.html', {'USERS': comp})
    else:
        return redirect('c_login')


def Profile_Manage(request):
    if 'com_data' in request.session.keys():
        comp = Company_Details.objects.get(id=int(request.session['com_data']))
        if request.POST:
            nm = request.POST['nm1']
            em = request.POST['em1']
            con = request.POST['con1']
            add1 = request.POST['add1']
            pass1 = request.POST['pass1']
            img1 = request.FILES.get('img1')

            comp.c_name = nm
            comp.c_email = em
            comp.c_cno = con
            comp.c_add = add1
            comp.c_pass = pass1
            print(img1)
            if img1 != None:
                comp.profile = img1

            comp.save()
            return redirect('CompDashBoard')

        return render(request, 'company/dash/Profile.html', {'USERS': comp})
    else:
        return redirect('c_login')


def AddCompCustomers(request):
    if 'com_data' in request.session.keys():
        comp = Company_Details.objects.get(id=int(request.session['com_data']))
        if request.POST:
            nm = request.POST['nm1']
            em = request.POST['em1']
            con = request.POST['con1']

            obj = Company_Customers()
            obj.comp = comp  # customers gets entered in the particular industry by passing its object
            obj.cust_nm = nm
            obj.cust_em = em
            obj.cust_con = con

             # password Create---------
            salfa = 'qwertyuiopasdfghjklzxcvbnm'
            ualfa = salfa.upper()
            spic = '!@#$%^&*()'
            num = '1234567890'

            data = salfa+ualfa+spic+num
            otp = ""
            for i in range(8):
                otp += str(random.choice(data))
                print(otp)
            print(otp)

            obj.cust_pass = otp
            obj.save()

            try:

                sender_email = "memakiyapratik2001@gmail.com"
                sender_pass = '8866381041'
                reciv_email = em

                server = smtplib.SMTP('smtp.gmail.com', 587)

                mes1 = f"""
                This is your new login id and password and Link
                email id={em}
                password={otp}
                Link = http://127.0.0.1:2751/Customer_Login
                """

                msg = email.message.Message()
                msg['Subject'] = "New Customer created"
                msg['From'] = sender_email
                msg['To'] = reciv_email
                password = sender_pass
                msg.add_header('Content-Type', 'text/html')
                msg.set_payload(mes1)

                server.starttls()
                server.login(msg['From'], password)
                server.sendmail(msg['From'], msg['To'], msg.as_string())

            except:
                return HttpResponse("<a href=''> You Have Entered Wrong Email Id </a>")

        return render(request, 'company/dash/add_customer.html', {'USERS': comp})
    else:
        return redirect('c_login')


def ViewCustomers(request):
    if 'com_data' in request.session.keys():
        comp_user = Company_Details.objects.get(
            id=int(request.session['com_data']))
        custs = Company_Customers.objects.filter(comp=comp_user)
        print(custs)
        return render(request, "company/dash/view_customer.html", {'USERS': comp_user, 'cust': custs})

    else:
        return redirect('c_login')


def DeleteCustomers(request, id):
    if 'com_data' in request.session.keys():

        custs = Company_Customers.objects.get(id=id)
        custs.delete()

        return redirect('ViewCustomers')
    else:
        return redirect('c_login')


def AddProduct(request):
    if 'com_data' in request.session.keys():
            comp = Company_Details.objects.get(
            id=int(request.session['com_data']))
            if request.POST:
                nm = request.POST['nm1']
                pr = request.POST['pr1']
                qty = request.POST['qty1']
                img = request.FILES.get('img1')

                var = Company_Product()
                var.comp = comp
                var.prod_nm = nm
                var.prod_price = pr
                var.prod_qty = qty
                var.prod_img = img
                var.save()
                return redirect('ViewProduct')
            return render(request, 'company/dash/add_product.html', {'USERS': comp})
    else:
        return redirect('c_login')


def UpdateProduct(request, id):
    if 'com_data' in request.session.keys():
            comp = Company_Details.objects.get(
                id=int(request.session['com_data']))
            prod = Company_Product.objects.get(id = id)
            if request.POST:
                nm = request.POST['nm1']
                pr = request.POST['pr1']
                qty = request.POST['qty1']
                img = request.FILES.get('img1')
                
                prod.comp = comp
                prod.prod_nm = nm
                prod.prod_price = pr
                prod.prod_qty = qty
                if img != None:
                    prod.prod_img = img
                prod.save()
                return redirect('ViewProduct')
            return render(request,'company/dash/update_product.html',{'USERS':comp,'prod':prod})
    else:
            return redirect('c_login')

def ViewProduct(request):
    if 'com_data' in request.session.keys():
        comp = Company_Details.objects.get(id = int(request.session['com_data']))
        prods = Company_Product.objects.filter(comp = comp)
        return render(request,'company/dash/view_product.html',{'USERS':comp,'prod':prods})
    else:
        return redirect('c_login')

def DeleteProduct(request,id):
    if 'com_data' in request.session.keys():
        prod=Company_Product.objects.get(id=id)
        prod.delete()
        return redirect('ViewProduct')
    else:
        return redirect('c_login')

def ViewOrders(request):
    if 'com_data' in request.session.keys():
        comp = Company_Details.objects.get(id = int(request.session['com_data']))
        cord = Customer_Order.objects.filter(comp = comp,status = 'False')
        return render(request,'company/dash/ViewOrders.html',{'USERS':comp,'cord':cord})
    else:
        return redirect('c_login')

def YEsOrder(request,id):
    if 'com_data' in request.session.keys():
        cord = Customer_Order.objects.get(id = id)
        cord.status = 'Yes'
        cord.save()
        return redirect('ViewOrders')
    else:
        return redirect('c_login')    

def NoOrder(request,id):
    if 'com_data' in request.session.keys():
        cord = Customer_Order.objects.get(id = id)
        cord.status = 'No'
        cord.save()
        return redirect('ViewOrders')
    else:
        return redirect('c_login') 



def ComLogout(request):
    if 'com_data' in request.session.keys():
        del request.session['com_data']
        return redirect('c_login')
    else:
        return redirect('c_login')

# ------------------------------------- Company ---------------------

# ------------------------------------- Customer ---------------------


def Customer_Login(request):
    if request.POST:
        em = request.POST['email']
        ps = request.POST['pass']
        
        try:
            valid = Company_Customers.objects.get(cust_em = em, cust_pass = ps)
            request.session['custom_user'] = valid.id
            return redirect('Customer_dash')
        except:
            return redirect('Customer_Login')
    return render(request, "customer/login/login.html")

def Customer_dash(request):
    if 'custom_user' in request.session.keys():
        cust = Company_Customers.objects.get(id = int(request.session['custom_user']))
        prod = Company_Product.objects.filter(comp = cust.comp)
        return render(request,'customer/dash/index.html',{'prod':prod})
       
     
    else:
        return redirect('Customer_Login')

def profile(request):
    if 'custom_user' in request.session.keys():
        cust = Company_Customers.objects.get(id = int(request.session['custom_user']))
        if request.POST:
            nm = request.POST['nm']
            em = request.POST['em']
            con = request.POST['cno']
            pa1 = request.POST['pass']
            img1 = request.FILES.get('img1')
            ad1 = request.POST['ad1']
            ad2 = request.POST['ad2']
            
            cust.cust_nm = nm
            cust.cust_em = em
            cust.cust_con = con
            cust.cust_add1 = ad1
            cust.cust_add2 = ad2
            cust.cust_pass = pa1
            if img1 != None:
                cust.cust_profile = img1
            cust.save()
        return render(request,'customer/dash/profile.html',{'cust':cust})
    else:
        return redirect('Customer_Login')

def Order_place(request,id):
    if 'custom_user' in request.session.keys():
        cust = Company_Customers.objects.get(id = int(request.session['custom_user']))
        prod = Company_Product.objects.get(id=id)
        if request.POST:
            qty = request.POST['qty1']
            obj = Customer_Order()
            obj.comp = prod.comp
            obj.cust = cust
            obj.prod = prod
            obj.qty = qty
            obj.status = 'False'
            obj.tot_price = int(int(qty) * int(prod.prod_price))
            obj.save()
            return redirect('Customer_dash')
        return render(request,'customer/dash/Order_place.html',{'prod':prod})
    else:
        return redirect('Customer_Login')

def ViewOrders(request):
    if 'com_data' in request.session.keys():
        comp = Company_Details.objects.get(id = int(request.session['com_data']))
        cord = Customer_Order.objects.filter(comp = comp,status = 'False')
        return render(request,'company/dash/ViewOrders.html',{'USERS':comp,'cord':cord})
    else:
        return redirect('c_login')

def All_Orders(request):
    if 'custom_user' in request.session.keys():
        cust = Company_Customers.objects.get(id = int(request.session['custom_user']))
        ord = Customer_Order.objects.filter(cust = cust)
        return render(request,'customer/dash/all_orders.html',{'ord':ord})
    else:
        return redirect('Customer_Login')


def Customer_logout(request):
    if 'custom_user' in request.session.keys():
        request.session['custom_user']
        return redirect('Customer_Login')    
    else:
        return redirect('Customer_Login')  


# ------------------------------------- Customer ---------------------
