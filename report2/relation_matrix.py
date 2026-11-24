"""이산수학 Report 2: 관계행렬의 동치 관계 판별과 폐포"""

SIZE = 5


def read_matrix():
    print("집합 A = {1, 2, 3, 4, 5}")
    print("관계행렬을 한 행씩 입력하세요. 0과 1 사이에는 공백을 넣으세요.")
    matrix = []
    while len(matrix) < SIZE:
        values = input(f"{len(matrix) + 1}행 > ").split()
        if len(values) != SIZE or any(v not in ("0", "1") for v in values):
            print("0 또는 1을 정확히 5개 입력하세요. 같은 행을 다시 입력합니다.")
            continue
        matrix.append([int(v) for v in values])
    return matrix


def print_matrix(matrix):
    for row in matrix:
        print(" ".join(str(value) for value in row))


# 세 함수는 성질이 성립하면 None, 성립하지 않으면 첫 번째 반례를 반환한다.
def check_reflexive(matrix):
    for i in range(SIZE):
        if matrix[i][i] == 0:
            return f"({i + 1}, {i + 1})이 없습니다."
    return None


def check_symmetric(matrix):
    for i in range(SIZE):
        for j in range(SIZE):
            if matrix[i][j] == 1 and matrix[j][i] == 0:
                return f"({i + 1}, {j + 1})은 있지만 ({j + 1}, {i + 1})은 없습니다."
    return None


def check_transitive(matrix):
    for i in range(SIZE):
        for j in range(SIZE):
            for k in range(SIZE):
                if matrix[i][j] and matrix[j][k] and not matrix[i][k]:
                    return (f"({i + 1}, {j + 1}), ({j + 1}, {k + 1})은 있지만 "
                            f"({i + 1}, {k + 1})은 없습니다.")
    return None


def check_relation(matrix, show_examples=False):
    results = {
        "반사성": check_reflexive(matrix),
        "대칭성": check_symmetric(matrix),
        "추이성": check_transitive(matrix),
    }
    for name, example in results.items():
        if example is None:
            print(f"{name}: 성립")
        else:
            print(f"{name}: 불성립")
            if show_examples:
                print(f"  반례: {example}")
    equivalent = all(example is None for example in results.values())
    print("판정: 동치 관계입니다." if equivalent else "판정: 동치 관계가 아닙니다.")
    return equivalent


def equivalence_class(matrix, element):
    row = matrix[element - 1]
    return [j + 1 for j in range(SIZE) if row[j] == 1]


def print_classes(matrix):
    for element in range(1, SIZE + 1):
        members = equivalence_class(matrix, element)
        print(f"[{element}] = {{" + ", ".join(map(str, members)) + "}")


def reflexive_closure(matrix):
    result = [row.copy() for row in matrix]
    for i in range(SIZE):
        result[i][i] = 1
    return result


def symmetric_closure(matrix):
    result = [row.copy() for row in matrix]
    for i in range(SIZE):
        for j in range(SIZE):
            if matrix[i][j]:
                result[j][i] = 1
    return result


def transitive_closure(matrix):
    result = [row.copy() for row in matrix]
    # 와샬 알고리즘: k를 중간에 거쳐 갈 수 있는 경로를 추가한다.
    for k in range(SIZE):
        for i in range(SIZE):
            for j in range(SIZE):
                if result[i][k] and result[k][j]:
                    result[i][j] = 1
    return result


def show_closure(title, original, closed):
    print(f"\n[{title}]")
    print("변환 전")
    print_matrix(original)
    print("변환 후")
    print_matrix(closed)
    if check_relation(closed):
        print_classes(closed)
        return True
    return False


def main():
    matrix = read_matrix()
    print("\n[입력한 관계행렬]")
    print_matrix(matrix)
    if check_relation(matrix, show_examples=True):
        print_classes(matrix)
        return

    # 각 폐포는 같은 원본에서 따로 구한다.
    closures = [
        ("반사 폐포", check_reflexive, reflexive_closure),
        ("대칭 폐포", check_symmetric, symmetric_closure),
        ("추이 폐포", check_transitive, transitive_closure),
    ]
    found_equivalence = False
    for title, check, close in closures:
        if check(matrix) is not None:
            if show_closure(title, matrix, close(matrix)):
                found_equivalence = True

    # 한 종류의 폐포만으로 부족하면 세 성질을 모두 만족하게 만든다.
    if not found_equivalence:
        closed = transitive_closure(symmetric_closure(reflexive_closure(matrix)))
        show_closure("동치 폐포 (반사, 대칭, 추이 순서)", matrix, closed)


if __name__ == "__main__":
    main()
