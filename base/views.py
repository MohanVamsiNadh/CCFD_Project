from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
import os
import pickle

# Assuming your pickle file is named "model.pkl" and is located in the "models" directory
pickle_file_path = os.path.join(os.path.dirname(__file__), 'models', 'CreditCardTransaction.pkl')

def load_model():
    with open(pickle_file_path, 'rb') as f:
        model = pickle.load(f)
    return model

def make_prediction(slider_values):
    model = load_model()
    # Use the loaded model to make predictions with the slider_values
    prediction_result = model.predict([slider_values])  # Assuming model.predict() accepts a list of values
    return prediction_result


@login_required
def home(request):
    if request.method =="POST":
        slider_values = []
        scaled_amount = float(request.POST.get('scaled_amount'))
        scaled_time = float(request.POST.get('scaled_time'))
        slider_values.append(scaled_amount)
        slider_values.append(scaled_time)
        # Retrieve all slider values from the POST data and store them in the list
        for i in range(1, 29):
            slider_name = 'v{}'.format(i)
            slider_value = float(request.POST.get(slider_name))
            slider_values.append(slider_value)
        #Below is a Not Fraud Data
        #output=make_prediction([-0.349231,0.610999,2.072580,0.149607,-1.999704,1.031397,0.958539,-0.248227,0.483135,-0.182755,0.072029,0.443366,-0.259533,0.467590,-0.555728,0.743943,-1.102466,-0.225939,-0.729392,0.216198,0.458528,-0.297658,0.024975,0.269702,-0.130068,-1.101987,0.554918,-0.441049,-0.020914,-0.084783])
        #Blow is a Fraut Data
        #output=make_prediction=([0.9229597201381718, -0.7378035166627184, -8.25711081724667, -4.81446073955621, -5.36530689032661, 1.20422986423394, -3.3474200965739, -1.33160147516446, -1.96789279857039, 1.29543781710486, -1.67441524280437, -3.42605225253339, 0.144562690111297, -4.28352931016896, -0.24089504151477, -3.65749040377527, 0.923104767832095, 0.844221069436753, -3.94831185243281, -1.8075159915996, 0.105878827218844, -1.23398725720348, 0.436390207477188, -0.077552722802211, -3.09162435615504, -0.390200885685448, -0.288688941339997, -0.340004217403437, 0.0398191045440342, -1.00790031022705])
        output=make_prediction(slider_values)
        print(slider_values)
        if(output==[0]):
            result="Not-Fraud"
        else:
            result="Fraud"
        return render(request, 'home.html',{'output':result})
    return render(request, 'home.html',{})



def authView(request):
 if request.method == "POST":
  form = UserCreationForm(request.POST or None)
  if form.is_valid():
   form.save()
   return redirect("base:login")
 else:
  form = UserCreationForm()
 return render(request, "registration/signup.html", {"form": form})
