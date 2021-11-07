import pandas as pd
import numpy as np
import math

import modules.Utils as utils
from modules.CommonDatas import DAYARR


class KMeans:
    def __init__(self, init_datas, logging=True):
        print("---Init KMeans---")
        self.datas = init_datas.copy()
        self.mean_pattern = self.datas.T.mean()
        self.cluster_dict = {}
        self.cluster_info = pd.DataFrame(columns=['label'])
        self.logging = logging

    def calc_tss(self):
        self.tss = 0
        for date in self.datas:
            self.tss += utils.euclidean_distance(
                self.mean_pattern,
                self.datas[date].values
            ) ** 2
        if self.logging:
            print("- calc TSS(Total Sum Of Squareds Success! -{}-".format(self.tss))

    def calc_mcdpv(self):
        self.mcdpv = 0
        tmp_mcdpv = []
        for date in self.datas:
            tmp_mcdpv.append(
                utils.cosine_similarity(
                    self.mean_pattern,
                    self.datas[date].values
                )
            )
        self.mcdpv = np.array(utils.min_max_normalization(
            np.array(tmp_mcdpv))).mean() * 100
        if self.logging:
            print(
                "- calc MCDPV(Mean Cluster Direction Pattern Value) Success! -{}-".format(self.mcdpv))

    def calc_wss(self):
        self.wss = 0
        for date in self.datas:
            k_num = self.cluster_info.loc[date]['label']
            pattern = self.datas[date].values
            self.wss += utils.euclidean_distance(
                pattern,
                self.cluster_dict[k_num]
            ) ** 2
        if self.logging:
            print(
                "- calc WSS(Within clusterSum Of Squares) Success! -{}-".format(self.wss))

    def calc_ecv(self):
        self.calc_tss()
        self.calc_mcdpv()
        self.calc_wss()
        self.calc_cdpv()
        self.ecv = (1 - (self.wss / self.tss)) * 100
        if self.logging:
            print("- calc ECV(Explained Cluster Variance) Success! -{}-".format(self.ecv))

    def calc_cdpv(self):
        self.cdpv = 0
        tmp_cdpv = []
        for k_num in self.cluster_dict.keys():
            cluster_cdpv = []
            index = self.cluster_info[
                self.cluster_info['label'] == k_num
            ].index
            for date in index:
                cluster_cdpv.append(
                    utils.cosine_similarity(
                        self.cluster_dict[k_num],
                        self.datas[date].values
                    )
                )
            if len(cluster_cdpv) == 1:
                tmp_cdpv.append(1)
            else:
                tmp_cdpv.append(
                    np.array(utils.min_max_normalization(
                        np.array(cluster_cdpv))).mean()
                )

        self.cdpv = np.array(tmp_cdpv).mean() * 100
        if self.logging:
            print(
                "- calc CDPV(Cluster Direction Pattern Value) Success! -{}-".format(self.cdpv))

    def dimension_reduction(self):
        if self.logging:
            print("---Dimension Reduction---")

        dr_datas = pd.DataFrame(columns=['x', 'y'])
        for data in self.datas:
            date = data
            dr_datas.loc[date] = [
                utils.euclidean_distance(self.mean_pattern,
                                         self.datas[date]),
                utils.cosine_similarity(self.mean_pattern, self.datas[date])
            ]

        dr_datas['x'] = utils.min_max_normalization(dr_datas['x'])
        dr_datas['y'] = utils.min_max_normalization(dr_datas['y'])

        self.dr_datas = dr_datas
        return dr_datas

    def remove_one_pattern(self):
        if self.logging:
            print("---Remove One Pattern---")

        remove_idxes = []
        for idx in self.datas.copy():
            if len(set(self.datas[idx].values)) == 1:
                remove_idxes.append(idx)

        self.og_length = len(self.datas.columns)

        new_datas = self.datas.copy()
        new_datas = new_datas.T
        new_datas = new_datas.loc[~new_datas.index.isin(remove_idxes)]
        new_datas = new_datas.T

        self.datas = new_datas.copy()
        self.mean_pattern = self.datas.T.mean()
        self.dr_datas = self.dimension_reduction()
        self.new_length = len(self.datas.columns)

        # print(remove_idxes)
        if self.logging:
            print(
                "- remove one pattern success: {} => {}".format(self.og_length, self.new_length))
        self.calc_tss()
        self.calc_mcdpv()

    def remove_outlier(self):
        if self.logging:
            print("---Remove Outliers---")
        outlier_range = 1.5

        dis_check = np.percentile(
            self.dr_datas['x'], 75) + (np.percentile(
                self.dr_datas['x'], 75) - np.percentile(self.dr_datas['x'], 25)) * outlier_range
        sim_check = np.percentile(
            self.dr_datas['y'], 25) - (np.percentile(
                self.dr_datas['y'], 75) - np.percentile(self.dr_datas['y'], 25)) * outlier_range
        if self.logging:
            print("- dis_check: {}, sim_check: {}".format(dis_check, sim_check))

        remove_index = self.dr_datas[
            (self.dr_datas['x'] >= dis_check) |
            (self.dr_datas['y'] <= sim_check)
        ].index

        # self.og_length = len(self.datas.columns)

        self.mdis = self.dr_datas['x'].mean()
        self.mcdpv = self.dr_datas['y'].mean()

        self.datas = self.datas.loc[:, ~self.datas.columns.isin(remove_index)]
        self.mean_pattern = self.datas.T.mean()
        self.dr_datas = self.dimension_reduction()

        self.new_length = len(self.datas.columns)
        if self.logging:
            print(
                "- remove outlier success: {} => {}".format(self.og_length, self.new_length))
        self.calc_tss()
        self.calc_mcdpv()

    def get_divide_index(self, K):
        if self.logging:
            print("---Divide Index---")
        # 홀수 배열 테스트
        length = len(self.dr_datas.index)
        arr = [idx for idx in range(0, length)]

        # 가장 첫번째 (평균)
        # 가장 먼 데이터
        idxes = [0, arr[length - 1]]
        # K
        d_weight = 1
        d_weight_sum = 1
        while True:
            tmp = idxes.copy()
            tmp.sort()
            tmp.reverse()

            for dseq in range(0, d_weight):
                if self.logging:
                    print("{}: calc... {}".format(d_weight, tmp))
                in_idx = math.ceil(tmp[dseq] / 2)
                if len(idxes) != (dseq + 1):
                    in_idx = math.ceil((tmp[dseq] + tmp[dseq + 1]) / 2)
                tmp.append(in_idx)

            idxes = tmp.copy()
            if self.logging:
                print("{}: {}".format(d_weight, idxes))
            if len(idxes) >= K:
                idxes = idxes[0: K]
                break
            else:
                d_weight += d_weight_sum
                d_weight_sum += 1
        return idxes

    def cost_sort(self, datas, weight):
        # dis cost operate
        dr_datas = datas.copy()
        dr_datas['cost'] = [0 for idx in range(0, len(dr_datas.index))]
        for cost, value in enumerate(dr_datas.sort_values(by=['x']).index):
            og_cost = dr_datas.loc[value]['cost']
            og_cost += (cost ** weight)
            dr_datas.loc[value, 'cost'] = og_cost

        # sim cost operate
        for cost, value in enumerate(dr_datas.sort_values(by=['y'], ascending=False).index):
            og_cost = dr_datas.loc[value]['cost']
            og_cost += cost
            dr_datas.loc[value, 'cost'] = og_cost

        return dr_datas.sort_values(by=['cost'], ascending=[True])

    def init_cluster(self):
        if self.logging:
            print("---Init Cluster---")
            print("---First K Is Mean Pattern---")

        if self.logging:
            print("---Rest K Select---")
        idxes = self.get_divide_index(self.K)
        # sort_dr_datas = self.cost_sort(self.dr_datas, 2)
        sort_dr_datas = self.dr_datas.sort_values(
            by=['x', 'y'], ascending=[True, False]).copy()

        for idx, val in enumerate(idxes):
            date = sort_dr_datas.iloc[val].name
            self.cluster_dict[len(
                self.cluster_dict.keys()
            )] = self.datas.loc[:, date].values
            if self.logging:
                print("-{}: K Setting Okay".format(idx + 1))

    def get_visual_datas(self, distribution_data=False, cluster_dist_data=False):
        visual_datas = pd.DataFrame(
            columns=['date', 'data', 'timeslot', 'day', 'cluster'])

        for date in self.cluster_info.index:
            tmp = pd.DataFrame()
            tmp['timeslot'] = [ts for ts in range(0, len(self.datas.index))]
            tmp['data'] = self.datas[date]
            tmp['date'] = date
            tmp['day'] = DAYARR[date.weekday()]
            tmp['cluster'] = self.cluster_info.loc[date]['label']

            visual_datas = pd.concat([visual_datas, tmp])

        rtn = []
        rtn.append(visual_datas)
        if distribution_data:
            # Request Distribution Datas
            dist_data = visual_datas.groupby(by=["day", "cluster"]).count()
            dist_data = dist_data / 24
            index = pd.MultiIndex.from_tuples(
                (), names=['day', 'cluster'])
            rtn_dist_data = pd.DataFrame(columns=['count'], index=index)

            for DAY in DAYARR:
                tmp = pd.DataFrame(columns=['count'], index=index)
                for k_num in range(0, self.K):
                    tmp.loc[(DAY, k_num), :] = [0]
                for k_num in dist_data.loc[DAY].index:
                    tmp.loc[(DAY, k_num), :] = dist_data.loc[(
                        DAY, k_num)]['date']
                rtn_dist_data = pd.concat([rtn_dist_data, tmp])
            rtn.append(rtn_dist_data)

        if cluster_dist_data:
            # Request Cluster Distribution Datas
            dist_data = visual_datas.groupby(by=["cluster"]).count()
            dist_data = dist_data / 24
            dist_data['count'] = dist_data['date']
            dist_data.drop(
                columns=['date', 'data', 'timeslot', 'day'], inplace=True)
            rtn.append(dist_data)

        return rtn

    def run(self, K=10):
        if self.logging:
            print("---init TSS Check---")
        self.calc_tss()
        self.calc_mcdpv()

        self.remove_one_pattern()
        if len(self.datas.columns) < 10:
            return False, "It is not worth"
        self.remove_outlier()

        self.sequence = 1
        prev_ecv = 0

        self.K = round(math.sqrt((len(self.datas.columns) / 2)))
        K = self.K

        print("---K Setting {} ---".format(K))

        print("---{}:Clustering Start---".format(K))
        self.cluster_dict = {}

        while True:
            print("---Now {}---".format(self.sequence))
            datas = self.datas.copy()

            if self.sequence == 1:
                print("---First Cluster Group Init---")
                self.init_cluster()
            else:
                for k_num in self.cluster_dict.keys():
                    idx_arr = self.cluster_info[
                        self.cluster_info['label'] == k_num
                    ].index.values
                    if len(idx_arr) != 0:
                        self.cluster_dict[k_num] = self.datas[idx_arr].T.mean(
                        ).values
            # Clustering
            if self.logging:
                print("---Cluster Init Okay KMeans Start---")
            self.cluster_info = pd.DataFrame()
            self.visual_datas = pd.DataFrame()
            self.labels = []

            cols = ['x', 'y']
            rows = [idx for idx in range(0, K)]
            for date in datas:
                sim_info = pd.DataFrame(columns=cols)
                for row in rows:
                    sim_info.loc[row] = [
                        utils.euclidean_distance(
                            self.cluster_dict[row],
                            datas[date].values
                        ),
                        utils.cosine_similarity(
                            self.cluster_dict[row],
                            datas[date].values
                        )
                    ]
                # self.labels.append(
                #     self.cost_sort(sim_info, 2).index[0]
                # )
                self.labels.append(sim_info.sort_values(
                    by=cols, ascending=[True, False]).index[0])

            # cluster info
            self.cluster_info['date'] = datas.columns
            self.cluster_info['label'] = self.labels
            self.cluster_info.set_index(['date'], inplace=True)

            # visual data
            for date in datas:
                tmp = pd.DataFrame()
                tmp['timeslot'] = range(0, 24)
                tmp['date'] = date
                tmp['data'] = list(datas[date].values)
                tmp['label'] = self.cluster_info.loc[date]['label']

                self.visual_datas = pd.concat([
                    tmp,
                    self.visual_datas
                ], ignore_index=True)

            self.calc_ecv()
            if self.logging:
                print("{} : TSS: {}, WSS: {}, ECV: {}, CDPV: {}".format(
                    self.sequence,
                    self.tss,
                    self.wss,
                    self.ecv,
                    self.cdpv
                ))

            if prev_ecv == self.wss:
                break
            else:
                self.sequence += 1
                prev_ecv = self.wss
                continue

        return True, "Success"
