# New Dimensionality Reduction - Euclidean Distance, Cosine Similarity

- scikit의 PCA라이브러리를 차원축소를 할 때 사용했으나, 공식의 파악이 힘들뿐더러 나중에 제어가 가능하려면 차원축소를 이해하고 있는 방식으로 사용하는 것이 좋을 거 같다로 부터 시작된 실험
- Euclidean Distance의 단점과 이를 보완해 줄 Cosine Similarity의 특징을 살펴보도록 하자.

(Notion Page)

[New Dimensionality Reduction - Euclidean Distance, Cosine Similarity](https://elegant-tern-afc.notion.site/New-Dimensionality-Reduction-Euclidean-Distance-Cosine-Similarity-3f6c6b6e3d834536abf2ef7dab3c8cfb)

# 1. Euclidean Distance

$$\sqrt{\Sigma^n_{i=1}(p_i-q_i)^2}$$

- 두 점 사이의 거리를 계산할 때 쓰이는 방법이다.
- 흔히 유클리드 거리를 이용하여 리스트 데이터의 유사도를 축정 하는 방법을 거리 기반 유사도 측정이라고 한다.

> **Euclidean Distance의 한계점**

- 유클리드 거리 측정은 차원이 작을수록 빛을 볼 뿐더러, 단순히 점과 점사이의 거리만 측정하기 때문에 해당 연구의 시간적 개념은 잡아내지 못하게 된다.
- 이는 거리기반 유사도 측정의 한계이기도 한데, 이들은 벡터의 성질(크기 + 방향)때문이다. 크기 based인 거리기반 유사도 측정은 방향을 측정하지 못한다.
- 그래서 이 유클리드 거리측정을 기반으로 평가를 하는 ECV가 과연 평가의 정도를 측정해줄 수 있을까? 에 대한 의문이 들었다.

  → 이는 후에 ECV Test로 이어진다.

  [ECV (Explained Cluster Variance) Test](https://www.notion.so/ECV-Explained-Cluster-Variance-Test-284ed49d54ba4dc7a58a2f6be21d63c1)

# 2. 다양한 방식의 유사도 측정

> **Cosine Similarity**

$$\frac{ab}{\lvert\lvert{a}\rvert\rvert_2\lvert\lvert{b}\rvert\rvert_2}$$

- Cosine Similarity는 두 벡터 간의 코사인 각도를 이용하여 구할 수 있는 두 벡터의 유사도를 의미한다. 방향이 완전히 동일한 경우에는 1의 값을 가지며, 반대의 방향을 가지면 0의 성질을 가지게 된다.
- Cosine Similarity는 두 벡터의 방향을 파악하는데, 사용할 수 있지만 거리는 전혀 관여하지 않는다. 패턴 자체가 똑같으면, 두 벡터의 크기가 달라도 높은 값의 유사도를 나타낸다.

> **DTW (Dynamic Time Warping)**

- DTW란 2개의 시간 sequence의 유사도를 측정하는 알고리즘이다.
- 시간에 따른 가중치를 부여함으로서 비용(cost)을 계산한다.

> **다양한 방식의 유사도 측정을 차원축소에 적용하여 테스트**

![_(29)](https://user-images.githubusercontent.com/52296323/128674525-eb3e3730-a824-4a2d-8278-c66cf38816ec.png)

기본 클러스터링 ( euclidean distance )

![_(30)](https://user-images.githubusercontent.com/52296323/128674545-1d105b08-adb5-4d57-8a12-97f4a7eb83ce.png)

PCA clustering

![_(31)](https://user-images.githubusercontent.com/52296323/128674560-c2673617-f8be-49af-941f-8c2151d6e589.png)

x = euclidean, y = cosine similar

![Untitled](https://user-images.githubusercontent.com/52296323/128674605-9d3c41e2-4191-4e7c-996d-b1876b01e7a0.png)

remove-outlier x=DTW, y = cosine similar

![_(32)](https://user-images.githubusercontent.com/52296323/128674592-1ec03edf-dba4-484f-9b67-d81d83b8a6f3.png)

x = DTW, y = cosine similar

- 약식으로 테스팅을 진행해보았는데, 대체적으로 모든 차원축소 기법들이 비슷비슷한 결과물을 보여주었다.

  → DTW 일단 보류

- 굳이 차원축소를 할 필요가 있나 싶겠지만, 거리만으로 측정하는 것보다, 하나의 특징을 추가하여 차원축소 후 클러스터링을 진행하면 수치적으로 다른 특징도 잡아낼 수 있게 되기 때문에 해당 테스트를 진행했다.
- 위에 결과들 중에서 현재 상황에서 제일 이해가 쉬울 거 같은 "x=euclidean distance, y=cosine similarity"를 골랐다. 또한 방향을 고려하지 않는 euclidean, 거리를 고려하지 않는 cosine, 두 개로 차원축소하면 적절한 패턴의 특징을 추출했다고 볼 수 있을 것 이라고 생각했다.

# 3. Euclidean Distance + Cosine Similarity

![Untitled 1](https://user-images.githubusercontent.com/52296323/128674618-3c1e39d8-2211-4baa-8a96-62e726ee6830.png)

- x=Euclidean Distance, y=Cosine Similarity 의 형태로 24차원 배열을 2차원 배열로 차원축소를 진행하고, 이들을 구할 때 사용한 전체 데이터셋의 평균과 Best Cost Pattern( x가 낮고, y가 높은 ), Worst Cost Pattern( x가 높고, y가 낮은 )을 비교해보았다.

![Untitled 2](https://user-images.githubusercontent.com/52296323/128674633-35227252-5e76-49a7-b229-f0e31ba36cf6.png)

- 결과는 아주 흥미로웠다. Worst Pattern은 정말 평균과 방향성이나, 거리 자체가 멀리 떨어져 있었고, Best Pattern은 평균 패턴과의 엄청난 유사성을 보여줬다.

> **300개의 가구에서 Test**

![Untitled 3](https://user-images.githubusercontent.com/52296323/128674662-eb2e253b-d9b0-4b03-b21b-33e2541c45ec.png)

![Untitled 4](https://user-images.githubusercontent.com/52296323/128674675-272861b5-0da2-4ade-b433-91a48df56eb7.png)

![Untitled 5](https://user-images.githubusercontent.com/52296323/128674689-eebc0781-019c-4e5d-8661-f903e34b978b.png)

- **Worst Pattern은 Red**, **Best Pattern은 Green**, **Worst Pattern은 Blue** 로 표시하였다.
- 전체적으로 보아도 **Worst Pattern**은 **Mean Pattern**과 차이가 많이 나는 것을 확인할 수 있고, **Best Pattern**은 **Mean Pattern**과 거의 유사함을 확인할 수 있었다.
- 추가적으로 **Best Distance Pattern은 Black**, **Best Similarity Pattern은 Gray**로 표시하였는데, 거리가 가장 가까운 패턴은 대체로 유사함을 나타냈고, **대부분이 Best Pattern과 똑같은 패턴**을 잡아냈다. 하지만 거리와 방향을 모두 따진 **Best Pattern과 패턴이 다른 경우에는 Best Pattern쪽이 평균패턴의 거리와 방향을 좀 더 잘 잡아낸 것을 확인**했다.

![Untitled 6](https://user-images.githubusercontent.com/52296323/128674698-e1eaa56c-f93f-4a5b-92b9-78d6802ee1fd.png)

![Untitled 7](https://user-images.githubusercontent.com/52296323/128674710-829c40e8-3116-4ec6-9f07-2c18ef35250f.png)

- 방향의 유사도를 나타낸 패턴도 **대부분이 Best Pattern과 똑같은 패턴**을 가리켰다. 하지만 **거리를 전혀 고려하지 않는 Cosine Similarity는 평균패턴과는 거리가 전혀 다른 패턴(이상치)을 Best Pattern**으로 잡아냈다.
- 이러한 거리를 고려하지 않는 Cosine Similarity의 특성은 Euclidean Distance와 함께 비교했을 때, 중화시킬 수 있다는 것을 확인했다. (X, Y)

# 4. 이상치 제거에 활용하기

> **이상치 제거에 앞서, 거리가 먼(Worst Distance), 방향성이 다른(Worst Similarity) 패턴들이 평균 패턴과 얼마나 차이를 보이는 지 테스팅을 해보았다.**

![Untitled 8](https://user-images.githubusercontent.com/52296323/128674726-307779ee-3c7b-4361-af70-5c04d020abbd.png)

![Untitled 9](https://user-images.githubusercontent.com/52296323/128674745-ee23425a-5375-492b-a880-21c620d7f665.png)

![Untitled 10](https://user-images.githubusercontent.com/52296323/128674776-2740460e-c474-48d7-ab0a-0bb2a7cd0a79.png)

- **거리가 먼 패턴은 black**, **방향성이 다른 패턴은 gray**로 표시를 했다.
- 한 눈에 보아도 이상치들을 잡아낸 것을 확인할 수가 있는데, 각 각의 유사도 평가들이 다른 이상치들을 잡아낸 것도 확인할 수 있었다.
- 또한 서로가 다른 패턴을 잡아내기도 하면서, 더 많은 이상치들을 제거할 수 있음을 보여준다.
