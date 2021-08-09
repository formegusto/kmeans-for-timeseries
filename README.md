# kmeans-uclidean-cosine

(Notion Page)

[kmeans-uclidean-cosine](https://elegant-tern-afc.notion.site/kmeans-uclidean-cosine-50a38509f23b44bb9c17e9a0bba03a02)

# 1. Summary

- 현재 국내외적으로 다양한 형태의 P2P(Peer to Peer) 전력거래가 구현되고 있는 상황에서 효과적인 P2P 형태의 전력 거래를 위해서는 개별 수용가의 부하 패턴을 분류하여 특정 월, 일, 시간별 전력 부하 패턴에 대한 추정이 매우 중요하다.
- **해당 연구의 목적**은 개별 수용가 전력 패턴들을 클러스터링하여, **특정 가구의 "계절별", "요일별", "시간별" 패턴을 추출해내고, RNN (Recurrent Neural Network) Model을 통하여, 후의 패턴까지 예측하게 함으로서 효과적인 P2P 전력거래 매칭을 성사** 시키는데 있다.
- **해당 프로젝트**는 RNN에 들어서기 전에, **Sequence Data로 분류되는 전력 패턴을 어떻게 효과적으로 클러스터링 할 수 있을까에 대한 Research Project** 이다.

![Untitled](https://user-images.githubusercontent.com/52296323/128653433-338586df-ff19-4651-8c01-e97080558eb5.png)

Original Pattern-Recognition Process

![Untitled 1](https://user-images.githubusercontent.com/52296323/128653439-89cb5cf3-0a06-4397-924e-d333aa170391.png)

New Pattern-Recognition Process

- K-분할 클러스터링 패턴 선택(예명), Euclidean Distance-Cosine Similarity 를 이용한 차원축소 및 아웃라이어 제거와 같은 새로운 기법을 프로세스에 적용한 클러스터링 모델을 소개한다.

# 2. Clustering Technic

- 수용가별 전력 부하 패턴을 분류하기 위해 공동주택 398가구의 2018년 5월부터 2019년 4월까지의 데이터의 1년간의 15분 단위 전력 사용량 데이터를 활용하였다.
- Sequence Data가 가질 수 있는 특징인 거리(Distance)와 방향(Direction)을 활용한 새로운 클러스터링 기법을 소개한다.

## 1. Clustering Data - Store - Data PreProcessing

![Untitled 2](https://user-images.githubusercontent.com/52296323/128653444-e9eee492-59c5-49f3-a4a3-dc2ecafd4e16.png)

![Untitled 3](https://user-images.githubusercontent.com/52296323/128653450-1d75c2ec-e99e-46e5-90ce-730d7c597019.png)

```python
class Household:
    def __init__(self, uid, season_datas):
        self.uid = uid
        self.season_datas = season_datas
        self.merge_datas = {}
		def merging(self, hours=1):
			# 4개의 timeslot data를
			# 합쳐서 1시간 단위의 전력패턴을
			# 만들어주는 함수
```

![Untitled 4](https://user-images.githubusercontent.com/52296323/128653455-aa679110-aba8-4c3a-a4dc-382f382569b5.png)

- 전력 부하 데이터 파일의 가구별 전력사용량 데이터를 데이터베이스에 가구별, 시간별로 객체배열로 저장을 해두고, 이를 조회하여 다수개의 날짜를 계절별로 분류하고(season_datas), 하나의 날짜에 대하여 15분 단위로 쪼개져있는 96개의 배열을 4개씩 전력을 더하여 1시간 단위의 24개 배열(merge_datas)로 패턴을 구성하여 클러스터링에 투입했다.

## 2. Dimensionality Reduction - Feature Extraction

> **Euclidean Distance(X), Cosine Similarity(Y) Based Dimensionality Reduction**

$$EuclideanDistance(a_n,b_n) = \sqrt{\Sigma^{n}_{i=1}(a_i - b_i)^2}$$

$$CosineSimilarity(a,b)=\frac{ab}{\lvert\lvert{a}\rvert\rvert_2\lvert\lvert{b}\rvert\rvert_2}$$

- 유사도 측정에 주로 쓰이는 Euclidean Distance와 Cosine Similarity를 특징을 추출하기 위한 차원축소에 활용했다.
- 하나의 가구의 전체 데이터셋의 평균으로부터 전체 데이터들의 거리와 방향을 측정하여, X축은 Eclidean Distance, Y축은 Cosine Similarity로 차원축소를 했고, 이를 minmax 정규화를 통하여 값의 확인이 수월하도록 정규화를 해주면서 24차원의 데이터를 2차원의 데이터로 구성했다.

```python
def dimension_reduction(self):
      dr_datas = pd.DataFrame(columns=['x', 'y'])
      for data in self.datas:
          date = data
          dr_datas.loc[date] = [
              distance.euclidean(self.mean_pattern,
                                 self.datas[date]),
              cos_sim(self.mean_pattern, self.datas[date])
          ]

      dr_datas['x'] = min_max_normalization(dr_datas['x'])
      dr_datas['y'] = min_max_normalization(dr_datas['y'])

      self.dr_datas = dr_datas
      return dr_datas
```

![Untitled 5](https://user-images.githubusercontent.com/52296323/128653461-79eaff40-adc7-4968-8814-679abd880339.png)

## 3. Remove Outliers

> **IQR (InterQuartile Range) Based Remove Outliers**

$$IQR = Q3 - Q1$$

$$Q1 = percentile(data_n, 25)$$

$$Q3 = percentile(data_n, 75)$$

$$MinimumOutliersRange = Q1 - (1.5 * IQR)$$

$$MinimumOutliersRange = Q3 + (1.5 * IQR)$$
