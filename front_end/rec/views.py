from django.shortcuts import render
from django.http import HttpResponse
import pandas as pd
import os

# Create your views here.

def home(request):
    """
    Test === Used to pass the title and render to home.html
    """
    return render(request, 'home.html', {'title': 'Vehicle Recommendation System'})

def knowledge_based_rec(df,
                        manufacturer=None,
                        category=None,
                        price=None,
                        comfort=None,
                        driving=None,
                        interior=None,
                        tech=None,
                        utility=None):
    """
    Calculate Utility based on Edmunds Rating from the User's Requirements.

    """

    # int("0") = 0, int("1") = 1
    attributes = {'comfort': int(comfort),
                  'driving': int(driving),
                  'interior': int(interior),
                  'tech': int(tech),
                  'utility':int(utility),
                  'weight': None,
                  'manufacturer': manufacturer,
                  'category': category,
                  'price': price
                  }

    cu = []

    sum = int(comfort) + int(driving) + int(interior) + int(tech) + int(utility)
    if 0 == sum:
        weight = 0
        attributes['weight'] = weight

        for i, row in df.iterrows():
            calculated_utility = (row['comfort'] + row['driving'] + row['interior'] + row['tech'] + row['utility'])/5
            cu.append(calculated_utility)

    else:
        weight = 1/sum
        attributes['weight'] = weight

        for i, row in df.iterrows():
            calculated_utility = (attributes['comfort']*weight)*row['comfort']
            + (attributes['driving']*weight)*row['driving'] + (attributes['interior']*weight)*row['interior'] + (attributes['tech']*weight)*row['tech'] + (attributes['utility']*weight)*row['utility']

            cu.append(calculated_utility)

    if 'Calculated Utility' in df.columns:
        del df['Calculated Utility']

    df.insert(0, 'Calculated Utility', cu, allow=_duplicatesTrue)


    print(f"Weight: {weight}")
    print(f"attributes: {attributes}")
    return attributes

def recommend(request):
    # Get path and Read CSV FIle with weight of each vehicles
    cwd = os.getcwd()
    csv_name = "post_process_edmund_rating.csv"
    DATA_SRC = os.path.join(cwd, 'rec', csv_name)
    df = pd.read_csv(DATA_SRC)

    manufacturer = request.POST.get('manufacturer', None)
    veh_type = request.POST.get('vehicle_type', None)

    price = request.POST.get('price', None)

    comfort = request.POST.get('comfort', 0)
    driving = request.POST.get('driving', 0)
    interior = request.POST.get('interior', 0)
    tech = request.POST.get('tech', 0)
    utility = request.POST.get('utility', 0)

    attributes = knowledge_based_rec(df, manufacturer, veh_type, price, comfort, driving, interior, tech, utility)
    z = df.sort_values('Calculated Utility').tail(10)

    # if 0 != attributes['weight']:
    #     z = df.sort_values('Calculated Utility').tail(10)
    # else:
    #     z = df.sort_values('overall rating').tail(10)





    z = z.to_html()
    # z = z.to_html(escaped=False)

    # context = {'data': price}
    # context = {'data': DATA_SRC}
    context = {'data': z}

    # return render(request, "result.html", {'rec': z})
    return render(request, "result.html", context)
