from pymongo import MongoClient as mc
from datetime import datetime as dt
from modules.CommonDatas import SEASONS, SEASONSARR
from modules.KmeansObject import Household
from numpy import dot
from numpy.linalg import norm
from scipy.spatial import distance
import pandas as pd
import random


class KETIDB:
    def __init__(self):
        self.mongo_uri = "mongodb://localhost:27017"

    def connect(self):
        print("connect KETIDB,,,")
        self.client = mc(self.mongo_uri)
        self.keti_pr_db = self.client.keti_pattern_recognition
        self.household_col = self.keti_pr_db.household_info
        self.uid_check = []
        print("connect success!!")

    def close(self):
        print("disconnect KETIDB,,,")
        self.client.close()
        self.uid_check = []
        print("disconnect success!!")

    def init_check(self):
        self.uid_check = []

    def processing(self, db_datas):
        uid_in, timeslot = db_datas['uid'], db_datas['timeslot']

        datelist = [
            dt.strptime(ts['time'], "%Y-%m-%d T%H:%M %z").date()
            for ts in timeslot
        ]
        datelist = list(set(datelist))
        datelist.sort()

        ts_datas = {}
        start_idx = 0
        end_idx = 96
        enl = 1

        for date in datelist:
            ts_datas[date] = [ts['power'] *
                              enl for ts in timeslot[start_idx:end_idx]]
            start_idx = end_idx
            end_idx = end_idx + 96

        ts_datas = pd.DataFrame(ts_datas).T
        datas = ts_datas.reset_index().copy()

        datas.rename(columns={"index": "date"}, inplace=True)
        datas['date'] = pd.to_datetime(datas['date'])
        datas['month'] = [dt.month for dt in datas['date']]
        datas = [
            datas[(datas['month'].isin(SEASONS[season]))].copy()
            for season in SEASONSARR
        ]

        season_datas = {
            "봄": datas[0].copy(),
            "여름": datas[1].copy(),
            "가을": datas[2].copy(),
            "겨울": datas[3].copy()
        }

        return Household(uid_in, season_datas)

    def find_one(self, uid, processing=False):
        if processing == True:
            return self.processing(self.household_col.find_one({
                "uid": uid
            }))
        else:
            return self.household_col.find_one({
                "uid": uid
            })

    def find_random(self, save=False, processing=False):
        self.total = self.household_col.find(
            {"uid": {"$nin": self.uid_check}}).count()
        db_datas = False
        while True:
            db_datas = list(self.household_col.find({
                "uid": {"$nin": self.uid_check}
            }).skip(random.randrange(0, self.total)).limit(1))
            if len(db_datas) == 0:
                continue
            else:
                db_datas = db_datas[0]
                break
        if save:
            self.uid_check.append(db_datas['uid'])

        if processing:
            return self.processing(db_datas)
        else:
            return db_datas


def euclidean_distance(A, B):
    return distance.euclidean(A, B)


def cosine_similarity(A, B):
    return dot(A, B) / (norm(A) * norm(B))


def min_max_normalization(list):
    return [
        (val - list.min()) /
        (list.max() - list.min())
        for val in
        list.values
    ]
