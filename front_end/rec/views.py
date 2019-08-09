from django.shortcuts import render
from django.http import HttpResponse
import pandas as pd
import os

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

    df.insert(0, 'Calculated Utility', cu, allow_duplicates=True)


    # print(f"Weight: {weight}")
    # print(f"attributes: {attributes}")
    return attributes

def recommend(request):
    """
        Get path and Read CSV FIle with weight of each vehicles
        Based on the User's Requirements that is selected from the
        Web application , sort and Filter based on manufacturer, vehicle type,
        Price, and selected vehicle aspects.

        If choices/preferecense are not selected, display all vehicles with the
        highest calcuated utiltiy.
    """

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

    if (manufacturer != 'None') and (veh_type != 'None'):
        #  Manufacturer and Vehicle Type was selected in drop down list
        mf = df.loc[(df['Manufacturer'] == manufacturer)].sort_values('Calculated Utility')
        z = mf.loc[(mf['category'] == veh_type)]
    elif manufacturer != 'None':
        # Manufacturer Selected Only
        z = df.loc[(df['Manufacturer'] == manufacturer)].sort_values('Calculated Utility')
    elif veh_type != 'None':
        # Vehicle Type Selected Only
        z = df.loc[(df['category'] == veh_type)].sort_values('Calculated Utility')
    else:
        # No choices Selected
        z = df.sort_values('Calculated Utility')

    if price != '':
        # Filter data if maximum price was selected
        try:
            if(int(price)):
                z = z.loc[(z['MSRP(Min)'] <= int(price)) & (int(price) >= z['MSRP(Max)'])]
        except ValueError as err:
            print("Please enter Valid Integer Values")

    z = z.tail(10).iloc[::-1].to_html()

    context = {'data': z}
    return render(request, "result.html", context)
