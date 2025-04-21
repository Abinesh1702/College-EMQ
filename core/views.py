from django.shortcuts import render , redirect , get_object_or_404
from .models import Candidate ,Voter 
from django.contrib import messages

# Create your views here.
def demo(request):
    candidatescount = Candidate.objects.all().count
    candidates = Candidate.objects.all()
    voters=Voter.objects.all().count()
    voter_list=Voter.objects.all()
    true_voters=[]
    for i in voter_list:
        if i.has_voted==True:
            true_voters.append(i)
    length_true_voters=len(true_voters)
    print(length_true_voters)
    context={'candidates':candidates,'voters':voters ,'candidate_count':candidatescount,'true_voters':length_true_voters}
    return render(request,'dashboard.html',context)
def candidate(request):
    candidates = Candidate.objects.all()
    
    # Pass the candidates to the template
    return render(request, 'candidate.html', {'candidates': candidates})
def person(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        slogan = request.POST.get('slogan')
        text = request.POST.get('text')
        para1 = request.POST.get('para1')
        para2 = request.POST.get('para2')
        para3 = request.POST.get('para3')
        para4 = request.POST.get('para4')
        para5 = request.POST.get('para5')
        profile_picture = request.FILES.get('profile_picture')

        Candidate.objects.create(
            name=name,
            slogan=slogan,
            text=text,
            para1=para1,
            para2=para2,
            para3=para3,
            para4=para4,
            para5=para5,
            profile_picture=profile_picture
        )

        messages.success(request, 'Candidate registered successfully!')
        return redirect('person')

    candidates = Candidate.objects.all() 
    return render(request, 'person.html', {'candidates': candidates})

def candidate_table(request):
    # Get all candidates from the database
    candidates = Candidate.objects.all()
    
    # Pass the candidates to the template
    return render(request, 'table.html', {'candidates': candidates})
def candidate_detail(request, pk):
    # Get the candidate by primary key (pk)
    candidate = get_object_or_404(Candidate, pk=pk)
    
    # Pass the candidate to the template
    return render(request, 'candidate.html', {'candidate': candidate})
import qrcode
from io import BytesIO
from django.http import HttpResponse, Http404
 
 
def generate_qr_code(request, pk):
    # Get the candidate by primary key (pk)
    candidate = get_object_or_404(Candidate, pk=pk)
    
    # Generate the URL for the candidate's detail page
    candidate_url = request.build_absolute_uri(candidate.get_absolute_url())
    
    # Create a QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(candidate_url)
    qr.make(fit=True)

    # Create an image of the QR code
    img = qr.make_image(fill_color="black", back_color="white")
    
    # Save image to a BytesIO object
    buffer = BytesIO()
    img.save(buffer, format='PNG')
    buffer.seek(0)
    
    # Return the image as an HTTP response
    response = HttpResponse(buffer, content_type="image/png")
    response['Content-Disposition'] = f'inline; filename="candidate_{candidate.pk}_qr.png"'
    return response

def generate_vote_qr_code(request):
    # candidate = get_object_or_404(Candidate)
    
    # The URL to the log page (voter registration page)
    log_page_url = request.build_absolute_uri('/register/') 
    
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    
    qr.add_data(log_page_url)  # QR code contains the log.html URL for registration
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    
    buffer = BytesIO()
    img.save(buffer, format='PNG')
    buffer.seek(0)
    
    response = HttpResponse(buffer, content_type="image/png")
    response['Content-Disposition'] = f'inline; filename="vote_qr.png"'
    return response

def voter_register(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        reg_no = request.POST.get('reg_no')
        email = request.POST.get('email')

        if not name or not reg_no or not email:
            messages.error(request, 'All fields are required.')
        else:
            if Voter.objects.filter(reg_no=reg_no).exists():
                messages.error(request, 'Registration number already exists. Please use a different one.')
            else:
                # Create and save the new voter
                voter = Voter.objects.create(name=name, reg_no=reg_no, email=email)
                
                # Save reg_no in the session so we can associate the voter with their votes
                request.session['voter_reg_no'] = reg_no
                
                messages.success(request, 'Voter registered successfully!')
                
                # Redirect to the voting page after successful registration
                return redirect('vote')  # Redirect to the vote page

    return render(request, 'log.html')


# Voting view
def vote(request):
    if request.method == 'POST':
        candidate_id = request.POST.get('candidate_id')  # Candidate selected
        candidate = Candidate.objects.get(pk=candidate_id)

        # Get the voter from the session (based on reg_no stored in the session)
        reg_no = request.session.get('voter_reg_no')
        if not reg_no:
            messages.error(request, 'Please register before voting.')
            return redirect('voter_register')

        voter = Voter.objects.get(reg_no=reg_no)

        # Check if the voter has already voted
        if voter.has_voted:
            messages.error(request, 'You have already voted!')
        else:
            # Increment the vote count for the selected candidate
            candidate.vote_count += 1
            candidate.save()

            # Mark the voter as having voted
            voter.has_voted = True
            voter.save()

            messages.success(request, 'Your vote has been cast successfully!')

        return redirect('vote')  # Redirect back to the voting page after voting

    candidates = Candidate.objects.all()  # Fetch all candidates to display
    return render(request, 'vote.html', {'candidates': candidates})

def total_voters(request):
    voter_list=Voter.objects.all()
    true_voters=[]
    for i in voter_list:
        if i.has_voted==True:
            true_voters.append(i)
    print(true_voters)
    return render(request,'total_voters.html',{'voters':true_voters})

def register_voters(request):
    voter_reg=Voter.objects.all()
    return render(request,'register_voters.html',{'voters':voter_reg})