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

$$MaximumOutliersRange = Q3 + (1.5 * IQR)$$

- 전체 데이터셋의 평균 패턴이라함은, 전체 데이터의 특징을 어느정도 하나씩은 담고 있다는 것을 말한다. 그리고 우리는 이를 기반으로 차원축소를 진행했다.
- 평균이라는 패턴을 만들어내는데 많은 역할을 하지 않는 패턴들은 이상치인 것이고, 이들을 거리가 멀고 방향성이 떨어지는 패턴들이다.

```python
dis_check = np.percentile(
            self.dr_datas['x'], 75) + (np.percentile(
                self.dr_datas['x'], 75) - np.percentile(self.dr_datas['x'], 25)) * outlier_range
        sim_check = np.percentile(
            self.dr_datas['y'], 25) - (np.percentile(
                self.dr_datas['y'], 75) - np.percentile(self.dr_datas['y'], 25)) * outlier_range

remove_index = self.dr_datas[
            (self.dr_datas['x'] >= dis_check) |
            (self.dr_datas['y'] <= sim_check)
        ].index
```

- Euclidean Distance는 거리가 멀 수록 값의 출력이 높게 나오고, Cosine Similarity는 방향이 다를 수록 값의 출력이 낮게 나온다.
- 때문에 X 축에서는 MaximumOutlier들을, Y 축에서는 MinimummOulier들을 잡아내도록 한다.

## 4. Dimensionality Reduction

> **Remove Outlier Datas Based**

- 아웃라이어의 제거로 인해 전체 데이터셋의 평균이 바뀔 것이다. 때문에 바뀐 평균을 기반으로 다시 한번 차원축소를 진행하도록 한다.

## 5. Number Of K

```python
K = round(math.sqrt((len(self.datas.columns) / 2)))
```

$$K = \sqrt{n/2}$$

- K의 개수 선정에는 널리 알려진 rule of thumb 방법론을 이용하였다.

## 6. Initial K Selection

> **K-Index Divided**

- 첫 번째 클러스터링 루프에서, K의 선택은 클러스터링의 결과를 좌지우지하는 아주 중요한 단계이다.
- 이러한 K를 마구잡이로 뽑아내면 매번 다른 결과를 뽑아낼 수 있기에 정형화된 K를 선정하는 로직이 필요로 했다.

![Untitled 6](https://user-images.githubusercontent.com/52296323/129122343-b45d8551-9045-45bb-80ae-2eb18bf844a2.png)

![Untitled 7](https://user-images.githubusercontent.com/52296323/128657052-ba69f712-9c72-48de-a1d4-e95b864fd5a6.png)

- 오른쪽과 같이 2차원으로 축소된 데이터를 거리(x)는 오름차순 정렬, 방향(y)은 내림차순 정렬을 하여 K를 선정한다.
- 선정방법은 다음과 같다.
  - K=7 일 때,
  1. 전체 데이터셋의 평균(mean_pattern)으로부터의 가장 우월한 패턴을 첫 번째 K로, 평균과 거리, 방향 평가가 모두 저하한 데이터(worst_pattern)를 두 번째 K로 선정한다.
  2. worst_pattern과 best_pattern의 사이에 있는 패턴을 3번째 K로 선정한다.
  3. 이와 같이 계속 분리해 나가면서 K의 개수를 늘려간다.
  4. 이와 같이 진행하면 설정된 K의 개수를 넘는 수의 클러스터가 생기게 되는데, 이 때는 이상치 쪽에 가까운 패턴들을 클러스터로 선정하여, 클러스터 과정에서 더 다양한 패턴을 뽑을 수 있도록 의도한다.

## 7. Evaluate

$$TSS = \Sigma^n_{i=1}Distance(m, x_i)^2$$

$$WSS = \Sigma^K_{j=1}\Sigma_{i\in e_j}Distance(c_j, x_i)$$

$$ECV = 1 - (WSS/TSS)$$

- 클러스터링의 정지조건과 품질평가에는 ECV(Explained Cluster Variance)를 사용한다.

# 3. Result

```python
def get_visual_datas(self, distribution_data=False, cluster_dist_data=False):
	// ...
```

![Untitled 8](https://user-images.githubusercontent.com/52296323/128970318-c518236a-485b-4552-8e12-3305124bcc73.png)

![Untitled 9](https://user-images.githubusercontent.com/52296323/128970327-dab9f047-9336-4b0c-83cd-39f4dba1c9ea.png)

![Untitled 10](https://user-images.githubusercontent.com/52296323/128970332-03a9c30b-bff9-4021-91df-e7009f782cf6.png)

- 해당 함수는 총 3개의 데이터를 반환한다. (visual_datas, dist_datas, cluster_dist_datas)
- visual_datas는 전체 데이터의 패턴 데이터와 날짜 클러스터링 번호가 들어가 있다.
- dist_datas에는 요일별 클러스터 분포도가 들어가 있다.
- cluster_dist_datas에는 클러스터별 분포도를 나타낸다.

## 1. Visualization

> Line Map Test : 클러스터 안에 속해 있는 패턴들을 그룹지어 모음

- ECV 80% Pattern

  ![Untitled 11](https://user-images.githubusercontent.com/52296323/128970343-440e7369-d6f5-4517-a015-19ea9ecb4ffa.png)

  ![Untitled 12](https://user-images.githubusercontent.com/52296323/128970352-7e4dc3ae-6040-4ffb-ab16-1a2f719f3aab.png)

- ECV 55% Pattern

  ![Untitled 13](https://user-images.githubusercontent.com/52296323/128970364-2494cb0f-3f38-49aa-a80a-8081d7a685ea.png)

  ![Untitled 14](https://user-images.githubusercontent.com/52296323/128970370-07747c42-e908-4985-9a53-5d5226017fad.png)

> Bar Map Test(Cluster) : 클러스터 별로 요일 분포도를 보기 위한 테스트

- ECV 80% Pattern

  ![Untitled 15](https://user-images.githubusercontent.com/52296323/128970377-af9b9704-1e58-4be7-b5e5-330be15e4f82.png)

- ECV 55% Pattern

  ![Untitled 16](https://user-images.githubusercontent.com/52296323/128970389-af2b2719-7998-4cb0-9e74-63e16f699bef.png)

> Bar Map Test (Day) : 요일 별로 클러스터 분포도를 보기 위한 테스트

- ECV 80% Pattern

  ![Untitled 17](https://user-images.githubusercontent.com/52296323/128970394-22a48482-39d4-4e3a-ac02-7824472c694e.png)

- ECV 55% Pattern

  ![Untitled 18](https://user-images.githubusercontent.com/52296323/128970402-2e36ee64-7ad0-4ca6-a402-a436a2772655.png)

> Observe

- 그냥 시각화를 하기 위해서 만들었지만 조금만 더 들여다 보면 흥미로운 결과들을 확인할 수 있다.

> 요일별 다른 분포

![Untitled 19](https://user-images.githubusercontent.com/52296323/128970416-779e9de1-c145-4d1d-82d9-2462b1afd3da.png)

![Untitled 20](https://user-images.githubusercontent.com/52296323/128970419-1dff4829-9aed-4f12-a2f6-8b12cb8ee791.png)

- ECV 55%의 결과의 화요일 분포도 이다. 해당 가구는 전체적으로 5번째 패턴에 요일들이 많이 분포해 있는데, 화요일에는 3번째 패턴에 많이 분포되어 있는 것을 확인할 수 있었다. 해당 가구는 화요일만 조금은 다른 패턴을 사용하는 가구인 것 이다.

![Untitled 21](https://user-images.githubusercontent.com/52296323/128970429-4ff42552-b051-4e38-84ba-f9e6e5250660.png)

![Untitled 22](https://user-images.githubusercontent.com/52296323/128970438-13013692-3de1-49ba-8404-b9ab95827e86.png)

- 또한 해당 패턴은 주말의 분포가 평일의 분포랑 많이 다르다는 것이다. ECV가 낮았지만 요일적 특성을 잘 잡아낸 케이스라고 볼 수 있었다.

> ECV가 높지만 한 곳에 너무 분포되어 있다.

![Untitled 17](https://user-images.githubusercontent.com/52296323/128970503-2664d2dc-53db-453d-9c8f-56a6ac0b60ce.png)

- ECV 수치를 80%, 기록한 가구이다. 한쪽에 몰려 있어서 전체적인 요일별 특성을 파악하기 힘들다는 점이 있다. 이를 보고 sub cluster들의 변화도 체크를 해줘야 한다는 것을 느꼈다.

## 2. Total Visualization

> 393개의 가구에서 Best Cluster를 뽑아 해당 클러스터에 있는 데이터들을 Line Plot으로 구성을 해보도록 하자. 그리고 Best Cluster가 알맞은 군집을 형성했는지 확인해보도록 하자.

![Untitled 23](https://user-images.githubusercontent.com/52296323/129122354-b3c9994c-ffc7-4428-9632-dada6b4c7b81.png)

![Untitled 24](https://user-images.githubusercontent.com/52296323/129122362-b09df7cd-104d-4132-be64-fcea4bd6df50.png)

![Untitled 25](https://user-images.githubusercontent.com/52296323/129122365-f18c7cd2-a786-41b0-a875-7da742bfe936.png)

![Untitled 26](https://user-images.githubusercontent.com/52296323/129122370-7b9b4380-5905-4a9c-a7f2-fbcfd11ae208.png)

![Untitled 27](https://user-images.githubusercontent.com/52296323/129122375-6315e014-bd9a-4496-8df3-6143bc4896df.png)

![Untitled 28](https://user-images.githubusercontent.com/52296323/129122381-f96f8e2c-e570-4148-adaa-811c15588534.png)

![Untitled 29](https://user-images.githubusercontent.com/52296323/129122389-fb8a7add-ebe0-4848-867d-81ac83b5a5d1.png)

![Untitled 30](https://user-images.githubusercontent.com/52296323/129122395-b9789802-0efb-4ef2-9481-dfc0982e5d2b.png)

- 393가구들 중에서 각자 자신의 Best Cluster 안에 속해있는 패턴들을 뽑아 봤다. Best Cluster 안에 있는 패턴들이 군집을 잘 이루면서 하나의 자신만의 패턴을 형성한 것을 확인할 수 있었다.

## 3. Store

> 후에 있을 RNN 학습, P2P 매칭을 위해 데이터베이스에 클러스터링 결과를 다음과 같은 하나의 형태로 저장

```tsx
{
	"uid": string;
	"k": string;
	"tss": number;
	"wss": number;
	"ecv": number;
	"cdpv": number;
	"info": { "date": string; "label": number }[]
}
```

![Untitled](kmeans-uclidean-cosine%2084f6546297384e2cbf22a9f753a1472c/Untitled%2031.png)

# 4. Next?

- 여기까지 전력 패턴에는 어떻게 클러스터링을 진행하는 것이 좋은가? 품질 평가는 어떤 방식으로 이루어지는 것이 좋은가? 에 대해서 연구를 진행했다.
- 본질적으로 서로 다른 패턴들이 있으면 ECV의 지수는 크게 변동하지 않는다. 하지만 ECV를 최대한 올릴 수 있는 방법은 K의 개수를 적절하게 설정하거나, 이상치 제거를 적절하게 하거나, 초기 클러스터 인스턴스를 적절하게 잡아주는 것들이 방법이다.
- 모든 가구들이 클러스터링을 효과적으로 진행할 수 있도록 다음 과제를 진행하면서도 클러스터링 성능을 높이기 위한 노력은 계속될 것 이다.
