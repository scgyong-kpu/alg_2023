# Sort 지원
- 알고리즘은 각 언어 시스템에서 잘 지원된다. 
- 알고리즘의 세부 구현을 라이브러리 이용자가 알 필요는 없다
- stable vs unstable
  - C언어: `qsort()` 만 있음
  - C++: `stable_sort()` vs `sort()`
  - Java: **Dual Pivot Quick Sort** vs **Tim Sort**
  - 그 외 언어에서는 비교적 TimSort 를 이용하는 편.

# 비교하기
- 프로그래머가 비교하는 방법을 반드시 제시해야만 한다
- `callback(a, b)` 형태를 띠어야 한다.
  - 프로그래머는 Function Pointer, Interface, Code block, Function Object, Lambda 등 언어 특성에 맞는 다양한 형태로 제공해야 한다
- 비교 결과를 제시하는 방법
  - int 로 제시하는 방법
    - `a` 가 `b` 보다 앞서면 **음수**, `b` 가 앞서면 **양수**, `a` 와 `b` 가 같으면 **0** 을 리턴한다
    - `C`, `Java`, `JavaScript`
  - boolean 으로 제시하는 방법
    - `a` 가 `b` 보다 앞서면 **true**, 그렇지 않으면 **false** 를 리턴한다
    - `C++ STL`, 
  - key function 으로 제시하는 방법
    - `callback(a)` 형태이며 `a` 는 배열 안의 각 원소이다. `a` 를 이용하여 시스템이 비교할 수 있는 값의 형태로 리턴한다
    - Python
  - 객체 자체를 Comparable 하게 만드는 방법
    - `C++`: Operator overload 를 통해 객체에 `<` 연산자를 구현한다
    - `Python`: Operator overload 를 통해 객체에 `__lt__(self)` 함수를 구현한다
    - `Java`: Java interface 인 `Comparator` 를 구현한다
   
# Mutable vs Immutable
- `sort()`
  - 원래의 배열 객체 내의 원소들을 재배치한다
- `sorted()`
  - 원래의 배열은 그대로 두고, 정렬을 마친 원소들로 구성된 새로운 배열을 리턴한다
- Examples:
  - JavaScript: `Array.sort()` vs `Array.toSorted()`
  - Python: `sort()` vs `sorted()`
  - Java: `Collections.sort(list)` vs `List.stream().sorted().collect()`

