# ECV (Explained Cluster Variance) Test

- TSS(Total Sum of Squares)에 따른 ECV(Explained Cluster Variance)의 변화를 확인하기 위한 실험
- TSS가 높으면 각 패턴들끼리의 이격정도가 높다는 것이고, 그러면 클러스터링도 더욱 분산되기 때문에 좋은 ECV를 뽑아낼 수 있지 않을까? 로부터 시작된 실험

(Notion Page)

[ECV (Explained Cluster Variance) Test]()

# 1. Fomula

1. TSS (Total Sum of Squares)

   $$\Sigma^N_{i=1}Distance(m, x_i)^2$$

   - 전체 데이터 평균으로부터 모든 데이터들의 거리 제곱합 ( 이는 KMeans 에서 k의 개수가 1일 때의 centerois 로부터의 거리의 합을 말한다.)

2. WSS (Within cluster Sum of Squares)

   $$\Sigma^K_{j=1}\Sigma_{i\in e_j}Distance(c_j, x_i)$$

   - 각 클러스터의 중심점과 클러스터 멤버들의 거리를 모두 합한 값으로, 클러스터 안에 이격정도를 나타냄.

3. ECV (Explainde Cluster Variance)

   $$1 - (WSS / TSS)$$

   - K의 개수가 늘어질 수록 이격정도는 줄어든다. 그래서 WSS가 줄어든다.
   - 데이터 셋들의 이격정도가 낮을 수록 TSS는 줄어든다.

     → 즉, 클러스터링이 잘 되어 있을수록 ECV의 값은 올라간다.

# 2. Household Analysis

> ECV 내림차순 정렬 ( 상위 5개 데이터 )

![ECV%20(Explained%20Cluster%20Variance)%20Test%20fffb5f575e4945ecbe8eb5bfe98d6d2d/Untitled.png](<ECV%20(Explained%20Cluster%20Variance)%20Test%20fffb5f575e4945ecbe8eb5bfe98d6d2d/Untitled.png>)

> ECV 오름차순 정렬 ( 하위 5개 데이터 )

![ECV%20(Explained%20Cluster%20Variance)%20Test%20fffb5f575e4945ecbe8eb5bfe98d6d2d/Untitled%201.png](<ECV%20(Explained%20Cluster%20Variance)%20Test%20fffb5f575e4945ecbe8eb5bfe98d6d2d/Untitled%201.png>)

> TSS 내림차순 정렬 ( 상위 5개 데이터 )

![ECV%20(Explained%20Cluster%20Variance)%20Test%20fffb5f575e4945ecbe8eb5bfe98d6d2d/Untitled%202.png](<ECV%20(Explained%20Cluster%20Variance)%20Test%20fffb5f575e4945ecbe8eb5bfe98d6d2d/Untitled%202.png>)

> TSS 오름차순 정렬 ( 하위 5개 데이터 )

![ECV%20(Explained%20Cluster%20Variance)%20Test%20fffb5f575e4945ecbe8eb5bfe98d6d2d/Untitled%203.png](<ECV%20(Explained%20Cluster%20Variance)%20Test%20fffb5f575e4945ecbe8eb5bfe98d6d2d/Untitled%203.png>)

- 처음에 해당 테스트를 시작한 이유인, TSS가 높으면 (이격도가 높으면) 클러스터링도 더 잘 되기 때문에 ecv가 높게 나오지 않을까? 하고 시작했지만 결과는 그렇지 않았다.

  → **TSS 만이 ECV를 결정 짓지는 않는다.**

- 심지어 tss 가 3번째로 낮은 [아파트3-103-1607]는 ecv가 3번째로 높다.

  → ECV를 결정 짓는 여러 가지 케이스들이 있을 것 이다.

> 클러스터링 전의 평균 방향성 (mcdpv)

![ECV%20(Explained%20Cluster%20Variance)%20Test%20fffb5f575e4945ecbe8eb5bfe98d6d2d/Untitled%204.png](<ECV%20(Explained%20Cluster%20Variance)%20Test%20fffb5f575e4945ecbe8eb5bfe98d6d2d/Untitled%204.png>)

> 클러스터링 전의 평균 거리 (mdis) : 아웃라이어가 제거 됐기 때문에 평균 거리 만이 tss를 나타내지는 않는다. (평균거리와 new_length(아웃라이어 제거 후의 데이터 길이) 를 같이 봐야한다.

![ECV%20(Explained%20Cluster%20Variance)%20Test%20fffb5f575e4945ecbe8eb5bfe98d6d2d/Untitled%205.png](<ECV%20(Explained%20Cluster%20Variance)%20Test%20fffb5f575e4945ecbe8eb5bfe98d6d2d/Untitled%205.png>)

- 여기서 클러스터링이 잘 되는 조건을 다시 따져보도록 하자. tss가 높을 수록( 이격도가 높다 = 다른 패턴, 혹은 멀리 떨어진 패턴들이 많다. ), mdis가 높을 수록 ( 평균과 다른 패턴들이 많다. ), mcdpv가 낮을 수록 ( 평균의 패턴과 방향성이 다른 패턴들이 많다 )
- 다시한번, 우리가 클러스터링을 돌리기 조건에서 얻을 수 있는 칼럼들을 살펴보자

  → K, tss, mdis, mcdpv, new_length

> mcdpv와 mdis의 관계

- "평균과 패턴이 어느정도 비슷하고(방향성), 거리가 멀면(거리), 성능이 좋은 클러스터링을 할 수 있다."

![ECV%20(Explained%20Cluster%20Variance)%20Test%20fffb5f575e4945ecbe8eb5bfe98d6d2d/Untitled%206.png](<ECV%20(Explained%20Cluster%20Variance)%20Test%20fffb5f575e4945ecbe8eb5bfe98d6d2d/Untitled%206.png>)

```
mdis mean: 0.4323243208695422
mcdpv mean: 0.62251492073534
```

- 최상위 패턴들의 mdis와 mcdpv를 보면, mdis가 높고(패턴간의 이격도가 높음), mcdpv가 높은(패턴간의 방향성이 같음) 패턴들이 속한 것을 확인할 수 있다. (평균 데이터 기준)

  → 그리고 지나치게 mdis가 낮은 패턴들도 물론 확인할 수 있었다. 하지만 이 안에 속한 데이터들을 보면,

  ![ECV%20(Explained%20Cluster%20Variance)%20Test%20fffb5f575e4945ecbe8eb5bfe98d6d2d/Untitled%207.png](<ECV%20(Explained%20Cluster%20Variance)%20Test%20fffb5f575e4945ecbe8eb5bfe98d6d2d/Untitled%207.png>)

  ![ECV%20(Explained%20Cluster%20Variance)%20Test%20fffb5f575e4945ecbe8eb5bfe98d6d2d/Untitled%208.png](<ECV%20(Explained%20Cluster%20Variance)%20Test%20fffb5f575e4945ecbe8eb5bfe98d6d2d/Untitled%208.png>)

  → 이와 같은 경우에서는 그냥 안에 패턴들 자체의 값이 낮아, 거리자체의 크기가 작게 나오기 때문에 TSS와 mdis 가 작게 나온 케이스이다. cdpv의 크기 자체는 평균을 넘어섰다. 해당 가구의 단위들 간에서 해당 mdis는 높은 것일 수도 있다.

- 최하위 패턴들의 mdis와 mcdpv를 보면, mdis가 낮고(패턴간의 이격도가 낮음), mcdpv가 낮은(패턴간의 방향성이 다름) 패턴들이 속한 것을 확인할 수 있다. (평균 데이터 기준)

  → mdis가 높은데 ecv가 낮게 나온 케이스

  ![ECV%20(Explained%20Cluster%20Variance)%20Test%20fffb5f575e4945ecbe8eb5bfe98d6d2d/Untitled%209.png](<ECV%20(Explained%20Cluster%20Variance)%20Test%20fffb5f575e4945ecbe8eb5bfe98d6d2d/Untitled%209.png>)

  mdis가 높은 대신에, mcdpv가 낮게되면, 이는 ecv를 작게 만들 수도 있다. 클러스터 간의 평균 이격도가 높은데, 방향성이 제각각이라는 뜻이기 때문이다. (클러스터 안에서 wss가 높게 나올 확률이 높음)

  → mcdpv가 높은데, ecv가 낮게 나온 케이스

  ![ECV%20(Explained%20Cluster%20Variance)%20Test%20fffb5f575e4945ecbe8eb5bfe98d6d2d/Untitled%2010.png](<ECV%20(Explained%20Cluster%20Variance)%20Test%20fffb5f575e4945ecbe8eb5bfe98d6d2d/Untitled%2010.png>)

  ![ECV%20(Explained%20Cluster%20Variance)%20Test%20fffb5f575e4945ecbe8eb5bfe98d6d2d/Untitled%2011.png](<ECV%20(Explained%20Cluster%20Variance)%20Test%20fffb5f575e4945ecbe8eb5bfe98d6d2d/Untitled%2011.png>)

  우선, mdis와 tss가 낮게 나온 이유는 패턴 데이터의 단위 때문이다. 하지만 방향성은 어느정도 높은데, 위에 mdis가 해당 단위 자체에서도 낮을 수 있기 때문이다. ( 더 세세하게 클러스터링을 해야 ecv가 눞아짐 )

> 정리를 해보자면, mdis(평균데이터와의 이격도), mcdpv(평균데이터와의 유사성) 을 높게 기록하면 높은 ecv를 얻어낼 수가 있다.

- 평균데이터는 모든 데이터들의 특성을 조금씩 담고 있다.

> 하지만, 무작정 tss가 높다고 ecv가 높게 나오지는 않는다. 왜냐면, 안에 데이터들의 단위와 방향성이 가장 큰 제약사항이기 때문이다.

→ 방향성에서 낮음을 기록하면, 방향성의 다름으로 tss가 높게 나올 수 있다. 즉, 이것은 클러스터링이 제대로 이루어지지 않고, 한 클러스터안에 (K의 개수는 한정적이기 때문) 속한 패턴들이 다 제각각일 수 있다. (WSS를 증가시킴)

# 3. TSS 크기에 의한 ECV Test

![ECV%20(Explained%20Cluster%20Variance)%20Test%20fffb5f575e4945ecbe8eb5bfe98d6d2d/Untitled%2012.png](<ECV%20(Explained%20Cluster%20Variance)%20Test%20fffb5f575e4945ecbe8eb5bfe98d6d2d/Untitled%2012.png>)

- 여기서 보이는 점은, tss가 높으면 ecv를 어느정도 보장은 해줄 수 있다. 단, 클러스터링을 진행하는 데이터 수량이 어느정도 맞춰줘야 한다.

  → tss가 높은 이유에는 단위 때문일 수도 있다. 위의 경우에는 또, 5개의 가구를 같이 돌린거기 때문에, 작은 단위를 가진 가구와 큰 단위를 가진 가구의 섞임의 의해서 tss가 크게 나올 수도 있는 것이다. 이거 때문이라면 거의 한 가구에 한 클러스터씩 붙게 되는 거라고 볼수 있다.

  → 위의 이유가 아니라면, 방향성이 많이 다른 이유인데, 이럴 경우에는 당연히 tss가 높게 나온다. 하지만 여기서 수량이 어느정도 tss 단위에 맞춰져 있으면, 방향성이 너무 다른, 해당 데이터의 단위 속에서 너무 높게, 이기 때문에 tss가 높게 나온것인데, 여기에 수량이 어느정도 받쳐주면, 해당 tss 속에서 많은 데이터들의 군집이 잡히기 때문에, 어느정도의 ecv는 보장이되는 것이다. (적어도 k=1 평균보다는 낮을 거기 때문에)

# 4. 수량에 의한 ECV Test

![ECV%20(Explained%20Cluster%20Variance)%20Test%20fffb5f575e4945ecbe8eb5bfe98d6d2d/Untitled%2013.png](<ECV%20(Explained%20Cluster%20Variance)%20Test%20fffb5f575e4945ecbe8eb5bfe98d6d2d/Untitled%2013.png>)

- 이 테스트는 위에 대한 증명이다. tss가 높을 수록, ecv가 높게 나온다가 아니고, tss와 클러스터링을 진행하는 데이터 수량을 함께 봤을 때, 적절하면 ecv가 높게 나오는 것이다. 추가적으로 mdis와 mcdpv를 살펴볼 필요도 있다.
