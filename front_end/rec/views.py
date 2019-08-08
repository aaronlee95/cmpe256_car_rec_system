from django.shortcuts import render
from django.http import HttpResponse
import pandas as pd
import os

# Create your views here.

def home(request):
    # return HttpResponse("<h1>Hello World!</h1>")
    return render(request, 'home.html', {'title': 'New Vehicle Recommendation System'})


# def knowledge_based_rec(df,manufacturer=None, category=None,price=None,comfort=None,driving=None,interior=None,tech=None,utility=None):
    # int(False) = 0, int(True) = 1
    # attributes = {'comfort': int(comfort), 'driving': int(driving), 'interior': int(interior), 
    #               'tech': int(tech), 'utility':int(utility)}

    # sum = int(comfort) + int(driving) + int(interior) + int(tech) + int(utility)
    # if 0 == sum:
    #     weight = 0.2
    # else:
    #     weight = 1/sum
    # # calculated utilty depending on the User's Preference
    # cu = []
    # for i, row in df.iterrows():
    #     calculated_utility = (attributes['comfort']*weight)*row['comfort'] + (attributes['driving']*weight)*row['driving']
    #     + (attributes['interior']*weight)*row['interior'] + (attributes['tech']*weight)*row['tech'] + (attributes['utility']*weight)*row['utility']
        
    #     cu.append(calculated_utility)
    # df.insert(0, 'Calculated Utility', cu, allow_duplicates=True)
    # int(False) = 0, int(True) = 1
def knowledge_based_rec(df,manufacturer=None, category=None,price=None,comfort=None,driving=None,interior=None,tech=None,utility=None):
    # int(False) = 0, int(True) = 1
    attributes = {'comfort': int(comfort), 'driving': int(driving), 'interior': int(interior), 
                  'tech': int(tech), 'utility':int(utility)}

    cu = []

    sum = int(comfort) + int(driving) + int(interior) + int(tech) + int(utility)
    if 0 == sum:
        weight = 0.2
        for i, row in df.iterrows():
            calculated_utility = weight*row['comfort'] + weight*row['driving'] + weight*row['interior'] + weight*row['tech'] + weight*row['utility']
            cu.append(calculated_utility)
    else:
        weight = 1/sum
        for i, row in df.iterrows():
            calculated_utility = (attributes['comfort']*weight)*row['comfort'] + (attributes['driving']*weight)*row['driving'] + (attributes['interior']*weight)*row['interior'] + (attributes['tech']*weight)*row['tech'] + (attributes['utility']*weight)*row['utility']
            cu.append(calculated_utility)

    print(f"Weight: {weight}")
    print(cu)
    if 'Calculated Utility' in df.columns:
        del df['Calculated Utility']

    df.insert(0, 'Calculated Utility', cu, allow_duplicates=True)



def recommend(request):
    # Get path and Read CSV FIle with weight of each vehicles
    cwd = os.getcwd()
    csv_name = "post_process_edmund_rating.csv"
    DATA_SRC = os.path.join(cwd, 'rec', csv_name)
    df = pd.read_csv(DATA_SRC)

    manufacturer = request.POST['manufacturer']
    veh_type = request.POST['vehicle_type']

    price = request.POST.get('price', None)

    comfort = request.POST.get('comfort', False)
    driving = request.POST.get('driving', False)
    interior = request.POST.get('interior', False)
    tech = request.POST.get('tech', False)
    utility = request.POST.get('utility', False)

    # knowledge_based_rec(df, manufacturer, veh_type, None, .14, .23, .21, .12, .30)
    knowledge_based_rec(df, manufacturer, veh_type, None, comfort, driving, interior, tech, utility)

    z = df.sort_values('Calculated Utility').tail(10)
    z = z.to_html()
    # z = z.to_html(escaped=False)

    # context = {'data': price}
    # context = {'data': DATA_SRC}
    context = {'data': z}

    # return render(request, "result.html", {'rec': z})
    return render(request, "result.html", context)