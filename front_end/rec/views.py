from django.shortcuts import render
from django.http import HttpResponse
import pandas as pd
import os

# Create your views here.

def home(request):
    # return HttpResponse("<h1>Hello World!</h1>")
    return render(request, 'home.html', {'title': 'New Vehicle Recommendation System'})


def knowledge_based_rec(df,
                        manufacturer=None,
                        category=None,
                        price=None,
                        comfort=None,
                        driving=None,
                        interior=None,
                        tech=None,
                        utility=None):

    if comfort+driving+interior+tech+utility == 1:
        cu = []
        for i, row in df.iterrows():
            calculated_utility = comfort*row['comfort'] + driving*row['driving']
            + interior*row['interior'] + tech*row['tech'] + utility*row['utility']
            cu.append(calculated_utility)
        df.insert(0, 'Calculated Utility', cu, allow_duplicates=True)
    else:
        print(f"Percentages of comfort, driving, interior, tech, and utility need to equal 100%. Try Again.")

def recommend(request):
    cwd = os.getcwd()
    csv_name = "post_process_edmund_rating.csv"
    # DATA_SRC = "C:/Users/Aaron/workspace/cmpe256/car_rec_system/front_end/rec/post_process_edmund_rating.csv"
    DATA_SRC = os.path.join(cwd, 'rec', csv_name)
    print(f"DATA_SRC: {DATA_SRC}")
    df = pd.read_csv(DATA_SRC)

    manufacturer = request.POST['manufacturer']
    veh_type = request.POST['vehicle_type']

    # comfort = request.POST['comfort']
    # driving = request.GET['driving']
    # interior = request.GET['interior']
    # tech = request.GET['tech']
    # utilitiy = request.GET['utility']

    knowledge_based_rec(df, manufacturer, veh_type, None, .14, .23, .21, .12, .30)
    z = df.sort_values('Calculated Utility').tail(10)
    z = z.to_html()
    # z = z.to_html(escaped=False)

    # context = {'data': d}
    # context = {'data': DATA_SRC}
    context = {'data': z}

    # return render(request, "result.html", {'rec': z})
    return render(request, "result.html", context)