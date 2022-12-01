from django.shortcuts import render, redirect
from .forms import *
from .models import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .filters import *
from django.views.generic.edit import CreateView


def create_bio_data(request):
    if request.method =="POST":
        form = PersonForm(request.POST,request.FILES)
        if form.is_valid():
            cc=form.save(commit=False)
            cc.status='New'
            cc.save()
            church = request.user.profile.church
            member= cc
            
            Church_Members.objects.create(church=church, member=member)
            messages.success(request, "Record Saved Successuflly")
            return redirect("church:baptism", pk=cc.id)

    else:
        form = PersonForm()

    template = "church/create_biodata.html"
    context ={
        'form':form,
    }
    return render(request,template,context)


def Update_member(request,pk):
    bio = People.objects.get(id=pk)
    if request.method =="POST":
        form = PersonForm(request.POST,request.FILES,instance=bio)
        if form.is_valid():
            cc=form.save()
            messages.success(request, "Record Updated Successuflly")

            return redirect("church:baptism", pk=bio.id)

    else:
        form = PersonForm(instance=bio)

    template = "church/create_biodata.html"
    context ={
        'form':form,
    }
    return render(request,template,context)


def delete_bio(request,pk):
    bio = People.objects.get(id=pk)
    bio.delete()
    messages.success(request,'Member Deleted')
    return redirect('agric:manage_biodata')


def manage_members(request):
    profile = request.user.profile.church
    bio = Church_Members.objects.filter(church=profile)
    myFilter = MemberFilter(request.GET, queryset=bio)
    bio = myFilter.qs
    total = bio.count()
    male = bio.filter(member__gender='Male').count()
    female = bio.filter(member__gender='Female').count()

    # myFilter = BioFilter(request.GET, queryset=bio)
    # bio = myFilter.qs
    # total = bio.count()
    # male = bio.filter(sex__name='Male').count()
    # female = bio.filter(sex__name='Female').count()

    template = 'church/church_members.html'

    context = {
        'bio':bio,
        'total': total,
        'male':male,
        'female':female,
        'myFilter':myFilter

    }
    return render(request,template,context)


def peoples_children(request,pk):
    bio = People.objects.get(id=pk)
    children = Peoples_Children.objects.filter(parent=bio.id)
    if request.method =="POST":
        form = ChildrenForm(request.POST)
        if form.is_valid():
            cc=form.save(commit=False)
            cc.parent = bio
            cc.save()
            messages.success(request, "Record Updated Successuflly")

            return redirect("church:peoples_children", pk=bio.id)

    else:
        form = ChildrenForm()

    template = "church/childrenform.html"
    context ={
        'form':form,
        'bio':bio,
        'children':children
    }
    return render(request,template,context)


def update_peoples_children(request,pk):
    child = Peoples_Children.objects.get(id=pk)
    bio = People.objects.get(id=child.parent.id)
    children = Peoples_Children.objects.filter(parent=bio.id)
    
    if request.method =="POST":
        form = ChildrenForm(request.POST,instance=child)
        if form.is_valid():
            cc=form.save(commit=False)
            cc.bio = bio
            cc.save()
            messages.success(request, "Child Information Updated")
            return redirect("church:peoples_children", pk=bio.id)
           
    else:
        form = ChildrenForm(instance=child)
    
    template = "church/childrenform.html"
    context ={
        'form':form,
        'bio':bio,
        'children':children,
    }
    return render(request,template,context)


def delete_peoples_children(request,pk):
    child = Peoples_Children.objects.get(id=pk)
    bio = People.objects.get(id=child.parent.id)
    child.delete()
    messages.success(request,'Child Deleted')
    return redirect("church:peoples_children", pk=bio.id)

def baptisms(request,pk):
    bio = People.objects.get(id=pk)
    baptism = Baptism.objects.filter(member=bio.id)
    if request.method =="POST":
        form = BaptismForm(request.POST)
        if form.is_valid():
            cc=form.save(commit=False)
            church = request.user.profile.church
            cc.member= bio
            cc.church=church
            cc.save()
            messages.success(request, "Record Updated Successuflly")
            return redirect("church:baptism", pk=bio.id)
    else:
        form = BaptismForm(instance=bio)

    template = "church/baptismform.html"
    context ={
        'form':form,
        'baptism':baptism,
        'bio':bio
    }
    return render(request,template,context)



def update_baptism(request,pk):
    baptise = Baptism.objects.get(id=pk)
    bio = People.objects.get(id=baptise.member.id)
    baptism = Baptism.objects.filter(member=bio.id)
    
    if request.method =="POST":
        form = BaptismForm(request.POST,instance=baptise)
        if form.is_valid():
            cc=form.save(commit=False)
            cc.bio = bio
            cc.save()
            messages.success(request, "Baptism Information Updated")
            return redirect("church:baptism", pk=bio.id)
           
    else:
        form = BaptismForm(instance=baptise)
    
    template = "church/baptismform.html"
    context ={
        'form':form,
        'bio':bio,
        'baptism':baptism,
    }
    return render(request,template,context)


def delete_baptism(request,pk):
    baptise = Baptism.objects.get(id=pk)
    bio = People.objects.get(id=baptise.member.id)
    baptise.delete()
    messages.success(request,'Baptism Infomation Deleted')
    return redirect("church:baptism", pk=bio.id)


def emmergency_contact(request,pk):
    bio = People.objects.get(id=pk)
    contact = Emmergency_Contact.objects.filter(member=bio.id)
    if request.method =="POST":
        form = EmmergencyForm(request.POST)
        if form.is_valid():
            cc=form.save(commit=False)
            cc.member= bio
            cc.save()
            messages.success(request, "Record Updated Successuflly")
            return redirect("church:emmergency_contact", pk=bio.id)
    else:
        form = EmmergencyForm()

    template = "church/emmergency.html"
    context ={
        'form':form,
        'contact':contact,
        'bio':bio
    }
    return render(request,template,context)



def update_emergency(request,pk):
    emergency = Emmergency_Contact.objects.get(id=pk)
    bio = People.objects.get(id=emergency.member.id)
    contact = Emmergency_Contact.objects.filter(member=bio.id)
    
    if request.method =="POST":
        form = EmmergencyForm(request.POST,instance=emergency)
        if form.is_valid():
            cc=form.save(commit=False)
            cc.bio = bio
            cc.save()
            messages.success(request, "Emergency Information Updated")
            return redirect("church:emmergency_contact", pk=bio.id)
           
    else:
        form = EmmergencyForm(instance=emergency)
    
    template = "church/emmergency.html"
    context ={
        'form':form,
        'bio':bio,
        'contact':contact,
    }
    return render(request,template,context)


def delete_emergency(request,pk):
    emergency = Emmergency_Contact.objects.get(id=pk)
    bio = People.objects.get(id=emergency.member.id)
    emergency.delete()
    messages.success(request,'Emergency Infomation Deleted')
    return redirect("church:emmergency_contact", pk=bio.id)


def profile(request,pk):
    
    bio = People.objects.get(id=pk)
    try:
        children = Peoples_Children.objects.filter(parent=bio.id)
    except Peoples_Children.DoesNotExist:
        pass
    try:
        baptism = Baptism.objects.filter(member=bio.id)
    except Baptism.DoesNotExist:
        pass
    try:
        contact = Emmergency_Contact.objects.filter(member=bio.id)
    except Emmergency_Contact.DoesNotExist:
        pass

    


    template = 'church/profile.html'
    context = {
        'bio':bio,
        'children':children,
        'baptism':baptism,
        'contact':contact,
       

    }
    return render(request,template,context)


def update_profile_member(request,pk):
    bio = People.objects.get(id=pk)
    if request.method =="POST":
        form = PersonForm(request.POST,request.FILES,instance=bio)
        if form.is_valid():
            cc=form.save()
            messages.success(request, "Record Updated Successuflly")

            return redirect("church:profile", pk=bio.id)

    else:
        form = PersonForm(instance=bio)

    template = "church/create_biodata.html"
    context ={
        'form':form,
    }
    return render(request,template,context)


def create_profile_peoples_children(request,pk):
    bio = People.objects.get(id=pk)
    children = Peoples_Children.objects.filter(parent=bio.id)
    if request.method =="POST":
        form = ChildrenForm(request.POST)
        if form.is_valid():
            cc=form.save(commit=False)
            cc.parent = bio
            cc.save()
            messages.success(request, "Child Added Successuflly")

            return redirect("church:profile", pk=bio.id)

    else:
        form = ChildrenForm()

    template = "church/childrenform.html"
    context ={
        'form':form,
        'bio':bio,
        'children':children
    }
    return render(request,template,context)


def update_profile_peoples_children(request,pk):
    child = Peoples_Children.objects.get(id=pk)
    bio = People.objects.get(id=child.parent.id)
    children = Peoples_Children.objects.filter(parent=bio.id)
    
    if request.method =="POST":
        form = ChildrenForm(request.POST,instance=child)
        if form.is_valid():
            cc=form.save(commit=False)
            cc.bio = bio
            cc.save()
            messages.success(request, "Child Information Updated")
            return redirect("church:profile", pk=bio.id)
           
    else:
        form = ChildrenForm(instance=child)
    
    template = "church/childrenform.html"
    context ={
        'form':form,
        'bio':bio,
        'children':children,
    }
    return render(request,template,context)


def create_profile_baptisms(request,pk):
    bio = People.objects.get(id=pk)
    baptism = Baptism.objects.filter(member=bio.id)
    if request.method =="POST":
        form = BaptismForm(request.POST)
        if form.is_valid():
            cc=form.save(commit=False)
            church = request.user.profile.church
            cc.member= bio
            cc.church=church
            cc.save()
            messages.success(request, "Record Updated Successuflly")
            return redirect("church:profile", pk=bio.id)
    else:
        form = BaptismForm(instance=bio)

    template = "church/baptismform.html"
    context ={
        'form':form,
        'baptism':baptism,
        'bio':bio
    }
    return render(request,template,context)



def update_profile_baptism(request,pk):
    baptise = Baptism.objects.get(id=pk)
    bio = People.objects.get(id=baptise.member.id)
    baptism = Baptism.objects.filter(member=bio.id)
    
    if request.method =="POST":
        form = BaptismForm(request.POST,instance=baptise)
        if form.is_valid():
            cc=form.save(commit=False)
            cc.bio = bio
            cc.save()
            messages.success(request, "Baptism Information Updated")
            return redirect("church:profile", pk=bio.id)
           
    else:
        form = BaptismForm(instance=baptise)
    
    template = "church/baptismform.html"
    context ={
        'form':form,
        'bio':bio,
        'baptism':baptism,
    }
    return render(request,template,context)


def create_profile_emmergency_contact(request,pk):
    bio = People.objects.get(id=pk)
    contact = Emmergency_Contact.objects.filter(member=bio.id)
    if request.method =="POST":
        form = EmmergencyForm(request.POST)
        if form.is_valid():
            cc=form.save(commit=False)
            cc.member= bio
            cc.save()
            messages.success(request, "Record Updated Successuflly")
            return redirect("church:profile", pk=bio.id)
    else:
        form = EmmergencyForm()

    template = "church/emmergency.html"
    context ={
        'form':form,
        'contact':contact,
        'bio':bio
    }
    return render(request,template,context)



def update_profile_emergency(request,pk):
    emergency = Emmergency_Contact.objects.get(id=pk)
    bio = People.objects.get(id=emergency.member.id)
    contact = Emmergency_Contact.objects.filter(member=bio.id)
    
    if request.method =="POST":
        form = EmmergencyForm(request.POST,instance=emergency)
        if form.is_valid():
            cc=form.save(commit=False)
            cc.bio = bio
            cc.save()
            messages.success(request, "Emergency Information Updated")
            return redirect("church:profile", pk=bio.id)
           
    else:
        form = EmmergencyForm(instance=emergency)
    
    template = "church/emmergency.html"
    context ={
        'form':form,
        'bio':bio,
        'contact':contact,
    }
    return render(request,template,context)


def new_member_status(request,pk):
    person = People.objects.get(id=pk)
    person.status = 'New'
    person.save()
    messages.success(request,'Membership Status Changed')
    return redirect("church:profile", pk=person.id)

def foundationclass_status(request,pk):
    person = People.objects.get(id=pk)
    person.status = 'Foundation Class'
    person.save()
    messages.success(request,'Membership Status Changed')
    return redirect("church:profile", pk=person.id)

def member_status(request,pk):
    person = People.objects.get(id=pk)
    person.status = 'Member'
    person.save()
    messages.success(request,'Membership Status Changed')
    return redirect("church:profile", pk=person.id)

def inactive_status(request,pk):
    person = People.objects.get(id=pk)
    person.status = 'Inactive'
    person.save()
    messages.success(request,'Membership Status Changed')
    return redirect("church:profile", pk=person.id)

def deceased_status(request,pk):
    person = People.objects.get(id=pk)
    person.status = 'Deceased'
    person.save()
    messages.success(request,'Membership Status Changed')
    return redirect("church:profile", pk=person.id)