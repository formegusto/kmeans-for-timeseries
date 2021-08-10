# General KMeans VS New KMeans

- Euclidean Distance 기반의 기존 KMeans와 Cosine Similarity의 개념을 기존 KMeans 개념에 더한 새로운 KMeans의 결과를 직접 분석해보면서 새로운 KMeans가 효과적인 KMeans인가에 대해서 검증을 해보려고 한다.


(Notion Page)
[General KMeans VS New KMeans](https://elegant-tern-afc.notion.site/General-KMeans-VS-New-KMeans-f30fbd3cae0a4e5ca85b824494631f02) 

# 1. Cluster Pattern Direction Value (CPDV) (예명)

> **새로운 패턴 클러스터링 평가방법**

$$CluterPatternDirectionValue = \frac{\Sigma^K_{j=1}\Sigma_{i\in e_j}CosineSimilarity(c_j, x_i)}{n}$$

- 테스트 자체의 품질을 평가하는 값이 ECV 이기 때문에, 새로운 KMeans에게 어느정도 불리하게 작용할 것 이다. 그렇기 때문에 새로운 패턴 클러스터링 품질 평가 값을 제시한다.
- ECV가 거리를 기반으로 군집의 이격 정도를 평가하는 방법이라 쳤을 때, 방향을 기반으로 평가하는 방법도 비슷하게 시도해볼 수 있지 않을까 하고 생각했다.
- 이론은 이러하다 클러스터의 중심부와 해당 클러스터 군집 내에 속한 데이터셋의 방향성 체크 값을 모두 합한 후 데이터셋의 크기 만큼 나누어주면 해당 클러스터링 결과의 평균의 방향성에 대한 데이터를 표현할 수 있을 것 이라는 생각에서 시작됐다.

# 2. **일반 KMeans의 평가가 높았던 케이스**

![Untitled](https://user-images.githubusercontent.com/52296323/128806890-e50ff100-558a-4cc7-b1c1-a37501715254.png)

![Untitled 1](https://user-images.githubusercontent.com/52296323/128806897-70c1edcf-0de5-4722-a51c-2bcbda779da1.png)

![Untitled 2](https://user-images.githubusercontent.com/52296323/128806900-ff5f85bd-33f4-4892-aaa2-0964dbdf0ad3.png))

![Untitled 3](https://user-images.githubusercontent.com/52296323/128806907-407f9f49-02f9-456d-bcef-6bf15365bc69.png)

- 일반 KMeans는 ECV 52%, CPDV 0.978 을 기록했다.
- **새로운 KMeans**는 ECV 48%, CPDV 0.979 를 기록했다.
- TSS를 보면 **새로운 KMeans**에서 일반 KMeans 보다 많은 이상치들을 제거한 것을 확인할 수 가 있는데, 때문에 **새로운 KMeans**에서는 더 다양한 군집 패턴을 나타냈다.

  - 그렇기 때문에 군집 안에 하나의 요소만 가지고 있는 클러스터는 WSS 0을 나타내게 되고, 자연스럽게 일반 KMeans의 WSS가 낮아지면서 다음과 같은 결과가 나타났다. 여기서 ECV의 한계점이 나타나고 우리는 다음을 고민해야 한다.

    **→ 군집의 요소가 하나라는 결과를 나타낸 클러스터링이 좋은 것인가? 여러 패턴의 군집을 만들어냈지만 ECV가 낮게 나온 클러스터링이 좋은 것인가?**

  - 오히려 오차범위를 나타낸 그래프를 보면, **새로운 KMeans**의 클러스터들을 큰 오차범위를 안 가지고 있는 것을 확인할 수 있다. 일반 KMeans의 6번 클러스터 ,**새로운 KMeans**의 7번 클러스터를 보면, 이상치 제거에 의해 일반 KMeans의 6번 클러스터의 오차범위 끝에 있던 데이터 셋 다른 군집에 속하면서 **새로운 KMeans**의 7번 클러스터에서는 오차범위가 작은 형태로 군집을 구성한 것을 확인할 수 있다.

    (ECV의 한계를 이상치 제거를 통해 잡아준다.)

# 3. 새로운 KMeans**의 평가가 높았던 케이스**

![Untitled 4](https://user-images.githubusercontent.com/52296323/128806921-65235e69-e8ff-4e25-8d5c-8a31a23fc6ac.png)

![Untitled 5](https://user-images.githubusercontent.com/52296323/128806939-001c0fac-3f2f-4485-b965-8ec4789aa3c9.png)

![Untitled 6](https://user-images.githubusercontent.com/52296323/128806947-dfa4040e-66b7-40bd-99cb-9431b114fcb3.png)

![Untitled 7](https://user-images.githubusercontent.com/52296323/128806953-da72253c-000f-409b-b1e1-6813c5681eed.png)

- 일반 KMeans의 ECV는 35%, CPDV는 0.986을 나타냈다.
- **새로운 KMeans**의 ECV는 36%, CPDV는 0.987을 나타냈다.
- **새로운 KMeans**는 더 많은 유형의 클러스터 패턴을 나타낸 것을 확인할 수 있다. TSS에서는 큰 차이가 없지만, 아웃라이어를 좀 더 제거해 TSS가 줄어들고, 더 다양한 군집패턴을 만들어내는 와중에 일반 KMeans에 단 하나의 요소만 가지고 있는 군집이 있는데도 불구하고 ECV가 더 높게 나왔다는 것은 엄청난 성과이다.

# 4. **두 개의 평가가 같았던 케이스**

![Untitled 8](https://user-images.githubusercontent.com/52296323/128806960-cbab06ac-af92-49aa-93da-8ba2a21a4ef8.png)

![Untitled 9](https://user-images.githubusercontent.com/52296323/128806970-d78213fa-c9e7-49c5-a33c-72973bda2476.png)

![Untitled 10](https://user-images.githubusercontent.com/52296323/128806977-65b809ac-5337-4e01-b8e9-bb97951e0f88.png)

![Untitled 11](https://user-images.githubusercontent.com/52296323/128806985-2133e3f3-aa7a-44fd-be41-6613159ce891.png)

- 해당 결과물은 **새로운 KMeans**가 아웃라이어 제거를 못해서 같은 개수의 데이터셋을 가지고 클러스터링이 이루어졌는데, 이와 같은 결과물은 X:Distance, Y:Direction 차원축소가 어느정도의 특징을 추출이 된 상태로 돌아가면서 Euclidean Distance 기반의 일반 KMeans가 사용하는 Euclidean을 Cosine Similarity가 대체해줄 수 있음을 나타낸다.

# 5. **364개 가구 테스트**

![Untitled 12](https://user-images.githubusercontent.com/52296323/128806997-c074df27-2c66-440b-9ca2-d11283160442.png)

- 364개의 가구 개별적으로 클러스터링 해서, 기존의 거리기반의 클러스터링과 새로운 차원축소 개념을 도입한 클러스터링의 평가값을 비교해보았다.

![Untitled 13](https://user-images.githubusercontent.com/52296323/128807004-166a4583-7b3f-48c3-bdb0-c848f43ee352.png)

![Untitled 14](https://user-images.githubusercontent.com/52296323/128807006-92b990ed-3713-4f50-9305-417b31673aa7.png)

![Untitled 15](https://user-images.githubusercontent.com/52296323/128807012-3997dc8e-5dbc-4a5a-bf2f-3975201f7516.png)

![Untitled 16](https://user-images.githubusercontent.com/52296323/128807019-db49f294-a01c-491a-9a97-086f22debf68.png)

- 364개 가구 중, 일반 KMmeans는 156, **새로운 KMeans**는 147, 그리고 동률은 총 61 개의 ECV를 나타냈다.
- 364개 가구 중, 일반 KMmeans는 41, **새로운 KMeans**는 262, 그리고 동률은 총 61개의 CPDV를 나타냈다.
- 두 개의 결과가 다르게 나오는 가장 큰 이유는 **새로운 KMeans**가 방향성 까지 체크하기 때문도 있지만, 이상치 제거의 이유가 크다. **새로운 KMeans**는 이상치 제거 단계에서 Cosine Similarity 값을 이용한 이상치제거도 수행하기 때문에 몇 가지 케이스에서는 일반 KMeans보다 더 많은 양의 아웃라이어를 제거하게 된다.
  - **새로운 KMeans**의 TSS는 일반 KMeans에 비해 떨어지기 때문에 전체 집단안에서 더 세밀하게 클러스터링이 되어야 할 뿐더러, 군집 안에 더 많은 패턴들을 담을 수 있기 때문에 군집 안에 하나의 패턴을 가질 확률이 높은 일반 KMeans보다 ECV 평가면에서 불리하게 작용한다.
- 평균적 방향성 평가 (CPDV)는 대체적으로 **새로운 KMeans**가 더 높게 나왔다.
  - 하지만 UKMeans가 방향성이 더 높게 나온 경우도 있다. 이 또한 이상치 제거에 의해서 나타나는 현상인다. 이상치가 제거되면서 UCOSKMeans는 더 다양한 군집의 중심부 패턴을 만들어 낸다. 그렇기 때문에 방향성도 더 세밀하게 측정이 되어서 군집에 속해야 한다.

# 6. 결론

- 여기까지 새로운 KMeans의 테스트와 새로운 평가단위 CPDV 소개를 진행해보았다.
- 해당 테스트는 새로운 KMeans가 일반 KMeans의 대체재로 사용해도 된다라는 것을 보여주기도 하지만, 굳이 cosine similarity를 낀 새로운 KMeans를 사용할 필요도 없다는 것도 보여줬다.
- 이는 ECV의 성질 때문이다. 때문에 다음과 같은 고민에 맞추어 우리는 어떤 Clustering 기법을 사용할 것 인지 결정해야 한다.

  → 좋은 군집이란, 고루고루 분포되어 있는 거이 좋은 군집인가?

  → 좋은 군집이란, ECV 평가가 높게 나왔지만, 군집 안에 하나의 멤버만 속할 수 있는 것이 좋은 군집인가?
