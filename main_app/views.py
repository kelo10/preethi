from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http import JsonResponse
from datetime import date

from django.core.management import call_command

from django.contrib import messages
from django.contrib.auth.models import User , auth
from .models import patient , doctor , diseaseinfo , consultation ,rating_review
from chats.models import Chat,Feedback

# Create your views here.


#loading trained_model
import joblib as jb
model = jb.load('trainedd_model')


def run_migrations(request):
    if request.method == "POST":
        call_command("migrate")
        return JsonResponse({"status": "migrations applied"})
    return JsonResponse({"error": "Invalid request"}, status=400)

def home(request):

  if request.method == 'GET':
        
      if request.user.is_authenticated:
        return render(request,'homepage/index.html')

      else :
        return render(request,'homepage/index.html')



   

       


def admin_ui(request):

    if request.method == 'GET':

      if request.user.is_authenticated:

        auser = request.user
        Feedbackobj = Feedback.objects.all()

        return render(request,'admin/admin_ui/admin_ui.html' , {"auser":auser,"Feedback":Feedbackobj})

      else :
        return redirect('home')



    if request.method == 'POST':

       return render(request,'patient/patient_ui/profile.html')





def patient_ui(request):

    if request.method == 'GET':

      if request.user.is_authenticated:

        patientusername = request.session['patientusername']
        puser = User.objects.get(username=patientusername)

        return render(request,'patient/patient_ui/profile.html' , {"puser":puser})

      else :
        return redirect('home')



    if request.method == 'POST':

       return render(request,'patient/patient_ui/profile.html')

       


def pviewprofile(request, patientusername):

    if request.method == 'GET':

          puser = User.objects.get(username=patientusername)

          return render(request,'patient/view_profile/view_profile.html', {"puser":puser})




def checkdisease(request):

  diseaselist=['Diabetes Mellitus', 'Hypothyroidism', 'Hyperthyroidism', 'Cushing Syndrome', 'Addisons Disease', 
                   'Hypopituitarism', 'Hyperparathyroidism', 'Hypoparathyroidism', 
                   'Acromegaly', 'Adrenal Insufficiency', 'Pineal Tumors', 'Type 2 Diabetes', 'Type 1 Diabetes']


  symptomslist=['fatigue', 'stretch_marks', 'osteoporosis', 'sleep_disturbances', 'low_blood_sugar', 'salt_craving', 'slow_healing_sows', 'thin_skin', 'weight_gain', 'weight_loss', 'increased_hunger', 'increased_thirst', 
                    'frequent_urination', 'dry_skin', 'hair_loss', 'heat_intolerance', 'cold_intolerance', 
                    'muscle_weakness', 'joint_pain', 'irregular_menstrual_cycles', 'excessive_hair_growth', 
                    'acne', 'abdominal_pain', 'depression', 'anxiety', 'nausea', 
                    'vomiting', 'darkening_of_skin', 'constipation', 'low_blood_pressure', 'high_blood_pressure', 
                    'vision_problems', 'dizziness', 'palpitations', 'tremors', 'sweating', 
                    'headache', 'nervousness', 'difficulty_sleeping', 'mood_swings', 'dehydration', 
                    'slow_heart_rate', 'rapid_heart_rate', 'goiter', 'hoarseness', 'frequent_infections']

  alphabaticsymptomslist = sorted(symptomslist)

  


  if request.method == 'GET':
    
     return render(request,'patient/checkdisease/checkdisease.html', {"list2":alphabaticsymptomslist})




  elif request.method == 'POST':
       
      ## access you data by playing around with the request.POST object
      
      inputno = int(request.POST["noofsym"])
      print(inputno)
      if (inputno == 0 ) :
          return JsonResponse({'predicteddisease': "none",'confidencescore': 0 })
  
      else :

        psymptoms = []
        psymptoms = request.POST.getlist("symptoms[]")
       
        print(psymptoms)

      
        """      #main code start from here...
        """
      

      
        testingsymptoms = []
        #append zero in all coloumn fields...
        for x in range(0, len(symptomslist)):
          testingsymptoms.append(0)


        #update 1 where symptoms gets matched...
        for k in range(0, len(symptomslist)):

          for z in psymptoms:
              if (z == symptomslist[k]):
                  testingsymptoms[k] = 1


        inputtest = [testingsymptoms]

        print(inputtest)
      

        predicted = model.predict(inputtest)
        print("predicted disorder is : ")
        print(predicted)

        y_pred_2 = model.predict_proba(inputtest)
        confidencescore=y_pred_2.max() * 100
        print(" confidence score of : = {0} ".format(confidencescore))

        confidencescore = format(confidencescore, '.0f')
        predicted_disease = predicted[0]

        

        #consult_doctor codes----------

        #   doctor_specialization = []
        

        Endocrinologist = ['Hyperparathyroidism','Hypothyroidism']
       
        Gynecologist = [ 'Cushing Syndrome','Hypoparathyroidism', 'Polycystic Ovary Syndrome']
       
        Primary_Care_Physician = ['Addisons Disease' ]

        Dietitian = ['Diabetes Mellitus', 'Type 1 Diabetes']

        Dermatologist = ['Acromegaly','Paralysis (brain hemorrhage)','Migraine','Cervical spondylosis']

        Oncologist = ['Hypopituitarism', 'Pituitary Tumors']

        Neurosurgeon = ['Adrenal Insufficiency', 'Pineal Tumors']

        Rheumatologist = ['Hyperthyroidism']

        Nutritionist = ['Type 2 Diabetes']
         
        if predicted_disease in Endocrinologist :
           consultdoctor = "Endocrinologist"
           
        if predicted_disease in Gynecologist :
           consultdoctor = "Gynecologist"
           

        elif predicted_disease in Primary_Care_Physician :
           consultdoctor = "Primary_Care_Physician"
     
        elif predicted_disease in Dietitian :
           consultdoctor = "Dietitian"
     
        elif predicted_disease in Dermatologist :
           consultdoctor = "Dermatologist"
     
        elif predicted_disease in Oncologist :
           consultdoctor = "Oncologist"
     
        elif predicted_disease in Neurosurgeon :
           consultdoctor = "Neurosurgeon"
     
        elif predicted_disease in Rheumatologist :
           consultdoctor = "Rheumatologist"
     
        elif predicted_disease in Nutritionist :
           consultdoctor = "Nutritionist"
     
        else :
           consultdoctor = "other"


        request.session['doctortype'] = consultdoctor 

        patientusername = request.session['patientusername']
        puser = User.objects.get(username=patientusername)
     

        #saving to database.....................

        patient = puser.patient
        diseasename = predicted_disease
        no_of_symp = inputno
        symptomsname = psymptoms
        confidence = confidencescore

        diseaseinfo_new = diseaseinfo(patient=patient,diseasename=diseasename,no_of_symp=no_of_symp,symptomsname=symptomsname,confidence=confidence,consultdoctor=consultdoctor)
        diseaseinfo_new.save()
        

        request.session['diseaseinfo_id'] = diseaseinfo_new.id

        print("disorder record saved sucessfully.............................")

        return JsonResponse({'predicteddisease': predicted_disease ,'confidencescore':confidencescore , "consultdoctor": consultdoctor})
   


   
    



   





def pconsultation_history(request):

    if request.method == 'GET':

      patientusername = request.session['patientusername']
      puser = User.objects.get(username=patientusername)
      patient_obj = puser.patient
        
      consultationnew = consultation.objects.filter(patient = patient_obj)
      
    
      return render(request,'patient/consultation_history/consultation_history.html',{"consultation":consultationnew})


def dconsultation_history(request):

    if request.method == 'GET':

      doctorusername = request.session['doctorusername']
      duser = User.objects.get(username=doctorusername)
      doctor_obj = duser.doctor
        
      consultationnew = consultation.objects.filter(doctor = doctor_obj)
      
    
      return render(request,'doctor/consultation_history/consultation_history.html',{"consultation":consultationnew})



def doctor_ui(request):

    if request.method == 'GET':

      doctorid = request.session['doctorusername']
      duser = User.objects.get(username=doctorid)

    
      return render(request,'doctor/doctor_ui/profile.html',{"duser":duser})



      


def dviewprofile(request, doctorusername):

    if request.method == 'GET':

         
         duser = User.objects.get(username=doctorusername)
         r = rating_review.objects.filter(doctor=duser.doctor)
       
         return render(request,'doctor/view_profile/view_profile.html', {"duser":duser, "rate":r} )








       
def  consult_a_doctor(request):


    if request.method == 'GET':

        
        doctortype = request.session['doctortype']
        print(doctortype)
        dobj = doctor.objects.all()
        #dobj = doctor.objects.filter(specialization=doctortype)


        return render(request,'patient/consult_a_doctor/consult_a_doctor.html',{"dobj":dobj})

   


def  make_consultation(request, doctorusername):

    if request.method == 'POST':
       

        patientusername = request.session['patientusername']
        puser = User.objects.get(username=patientusername)
        patient_obj = puser.patient
        
        
        #doctorusername = request.session['doctorusername']
        duser = User.objects.get(username=doctorusername)
        doctor_obj = duser.doctor
        request.session['doctorusername'] = doctorusername


        diseaseinfo_id = request.session['diseaseinfo_id']
        diseaseinfo_obj = diseaseinfo.objects.get(id=diseaseinfo_id)

        consultation_date = date.today()
        status = "active"
        
        consultation_new = consultation( patient=patient_obj, doctor=doctor_obj, diseaseinfo=diseaseinfo_obj, consultation_date=consultation_date,status=status)
        consultation_new.save()

        request.session['consultation_id'] = consultation_new.id

        print("consultation record is saved sucessfully.............................")

         
        return redirect('consultationview',consultation_new.id)



def  consultationview(request,consultation_id):
   
    if request.method == 'GET':

   
      request.session['consultation_id'] = consultation_id
      consultation_obj = consultation.objects.get(id=consultation_id)

      return render(request,'consultation/consultation.html', {"consultation":consultation_obj })

   #  if request.method == 'POST':
   #    return render(request,'consultation/consultation.html' )





def rate_review(request,consultation_id):
   if request.method == "POST":
         
         consultation_obj = consultation.objects.get(id=consultation_id)
         patient = consultation_obj.patient
         doctor1 = consultation_obj.doctor
         rating = request.POST.get('rating')
         review = request.POST.get('review')

         rating_obj = rating_review(patient=patient,doctor=doctor1,rating=rating,review=review)
         rating_obj.save()

         rate = int(rating_obj.rating_is)
         doctor.objects.filter(pk=doctor1).update(rating=rate)
         

         return redirect('consultationview',consultation_id)





def close_consultation(request,consultation_id):
   if request.method == "POST":
         
         consultation.objects.filter(pk=consultation_id).update(status="closed")
         
         return redirect('home')






#-----------------------------chatting system ---------------------------------------------------


def post(request):
    if request.method == "POST":
        msg = request.POST.get('msgbox', None)

        consultation_id = request.session['consultation_id'] 
        consultation_obj = consultation.objects.get(id=consultation_id)

        c = Chat(consultation_id=consultation_obj,sender=request.user, message=msg)

        #msg = c.user.username+": "+msg

        if msg != '':            
            c.save()
            print("msg saved"+ msg )
            return JsonResponse({ 'msg': msg })
    else:
        return HttpResponse('Request must be POST.')



def chat_messages(request):
   if request.method == "GET":

         consultation_id = request.session['consultation_id'] 

         c = Chat.objects.filter(consultation_id=consultation_id)
         return render(request, 'consultation/chat_body.html', {'chat': c})


def run_migrations(request):
    try:
        call_command('migrate')
        return HttpResponse("✅ Migrations completed successfully.")
    except Exception as e:
        return HttpResponse(f"❌ Migration Error: {e}")

def create_admin_user(request):
    try:
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@example.com', 'adminpass123')
            return HttpResponse("✅ Superuser created: admin / adminpass123")
        return HttpResponse("ℹ️ Superuser already exists.")
    except Exception as e:
        return HttpResponse(f"❌ Error: {e}")

from django.http import HttpResponse
from django.db import connection  # Import the connection object

from django.http import HttpResponse
from django.db import connection

def grant_permissions(request):
    try:
        with connection.cursor() as cursor:
            cursor.execute("GRANT CREATE ON SCHEMA public TO disorder_user;")
            cursor.execute("GRANT USAGE ON SCHEMA public TO disorder_user;") # Add USAGE permission
            return HttpResponse("Successfully granted CREATE and USAGE permission on public schema to disorder_user.")
    except Exception as e:
        return HttpResponse(f"Failed to grant permissions: {e}")


#-----------------------------chatting system ---------------------------------------------------
