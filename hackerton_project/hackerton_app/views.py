from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
import pandas as pd
import pickle
from .models import survey

# import csv
# import os
# import django

# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "testbed3_app.settings")
# django.setup()


# csv_path = r"C:\Users\WIN10\hackerton_project2\hackerton_project\hackerton_app\data\survey.csv"
# # survey 데이터베이스 저장하기
# with open(csv_path, 'r', encoding='utf-8') as csvfile:
#     data_reader = csv.DictReader(csvfile)
#     for row in data_reader:
#         print(row)
#         survey.objects.create(
#             Q_1 = row["Q_1"],
#             Q_2 = row["Q_2"],
#             Q_3 = row["Q_3"],

#             Q_4 = row["Q_4"],
#             Q_5 = row["Q_5"],
#             Q_6 = row["Q_6"],

#             Q_7 = row["Q_7"],
#             Q_8 = row["Q_8"],
#             Q_9 = row["Q_9"],

#             Q_10 = row["Q_10"],
#             Q_11 = row["Q_11"],
#             Q_12 = row["Q_12"]
#         )


# Create your views here.
def main(request):
    return render(request, "main.html")

def input(request):
    return render(request, "input.html")


def predict(request): 
    #새로운 고객의 설문조사 결과를 출력(예측하는) 함수
    #DB에서 데이터 불러오기
    # surveys = survey.objects.all()
    # survey_list = []
    # for s in surveys:
    #     inner_list = []
    #     a1 = s.Q_1
    #     inner_list.append(a1)
    #     a2 = s.Q_2
    #     inner_list.append(a2)
    #     a3 = s.Q_3
    #     inner_list.append(a3)
    #     a4 = s.Q_4
    #     inner_list.append(a4)
    #     a5 = s.Q_5
    #     inner_list.append(a5)
    #     a6 = s.Q_6
    #     inner_list.append(a6)
    #     a7 = s.Q_7
    #     inner_list.append(a7)
    #     a8 = s.Q_8
    #     inner_list.append(a8)
    #     a9 = s.Q_9
    #     inner_list.append(a9)
    #     a10 = s.Q_10
    #     inner_list.append(a10)
    #     a11 = s.Q_11
    #     inner_list.append(a11)
    #     a12 = s.Q_12
    #     inner_list.append(a12)
    #     survey_list.append(inner_list)


    #DB에서 받아온 데이터를 바탕으로 데이터프레임 신규생성
    # survey_df = pd.DataFrame(survey_list)
    # survey_df.columns = ["Q_1", "Q_2", "Q_3", "Q_4", "Q_5", "Q_6", 
    #               "Q_7", "Q_8", "Q_9", "Q_10", "Q_11", "Q_12"]
    
    # #군집화 학습 진행하기
    # kmeans = KMeans(n_clusters=3, random_state=77)
    # kmean_label = kmeans.fit(survey_df)
    # 0 -> 1단계, 1 -> 3단계, 2 -> 2단계

    #설문조사 값 가져오기
    lst = []
    q1 = request.POST["1"]; q2 = request.POST["2"]; q3 = request.POST["3"]
    q4 = request.POST["4"]; q5 = request.POST["5"]; q6 = request.POST["6"]
    q7 = request.POST["7"]; q8 = request.POST["8"]; q9 = request.POST["9"]
    q10 = request.POST["10"]; q11 = request.POST["11"]; q12 = request.POST["12"]
    

    #데이터 베이스에 설문조사 값 저장하기
    survey.objects.create(
        Q_1 = int(q1),
        Q_2 = int(q2),
        Q_3 = int(q3),
        Q_4 = int(q4),
        Q_5 = int(q5),
        Q_6 = int(q6),
        Q_7 = int(q7),
        Q_8 = int(q8),
        Q_9 = int(q9),
        Q_10 = int(q10),
        Q_11 = int(q11),
        Q_12 = int(q12)
    )
    
    #임시 리스트에 저장하고 데이터프레임 생성하기
    lst.append(int(q1))
    lst.append(int(q2))
    lst.append(int(q3))
    lst.append(int(q4))
    lst.append(int(q5))
    lst.append(int(q6))
    lst.append(int(q7))
    lst.append(int(q8))
    lst.append(int(q9))
    lst.append(int(q10))
    lst.append(int(q11))
    lst.append(int(q12))
    print(lst)

    #고객의 입력값을 바탕으로 데이터프레임 생성
    new_df = pd.DataFrame(lst).T
    new_df.columns = ["Q_1", "Q_2", "Q_3", "Q_4", "Q_5", "Q_6", 
                  "Q_7", "Q_8", "Q_9", "Q_10", "Q_11", "Q_12"]
    #설문조사 임시 리스트에 저장된 값을 바탕으로, 어느 클러스터에 속하게 될지 예측을 진행한다.
    with open(r"model_save.pkl", "rb") as file:
        save_model = pickle.load(file) 
        pred = save_model.predict(new_df)
        cluster_integer = int(pred)

    if cluster_integer == 0:
        immunity_level = 1
    elif cluster_integer == 2:
        immunity_level = 2
    elif cluster_integer == 1:
        immunity_level = 3

    #랜덤 시드 값을 기반으로 컨텐츠 6개 추천해주기
    contents = pd.read_csv(r"hackerton_app\data\corona_youtube_contents_v2.csv")
    contents = contents.sample(frac=1)
    contents_pick = contents.iloc[0:6, :]

    contents_list = list(contents_pick.contents_name)
    href_list = list(contents_pick.href)

    #context에 결과값 매핑해서 저장
    context = {
        "immunity_level" : immunity_level,
        "contents_list" : contents_list,
        "href_list" : href_list,
    }

    #최종 리턴 작성
    #return render(request, "predict.html", context)
    return render(request, "result.html", context)
