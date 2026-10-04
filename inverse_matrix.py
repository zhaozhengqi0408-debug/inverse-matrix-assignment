from math import isfinite

EPS = 1e-10


def read_matrix():
    while True:
        try:
            n = int(input("행렬 크기 n: "))
            if n > 0:
                break
        except ValueError:
            pass
        print("양의 정수를 입력하세요.")
    a = []
    for i in range(n):
        while True:
            try:
                row = [float(x) for x in input(f"{i + 1}행: ").split()]
                if len(row) == n and all(isfinite(x) for x in row):
                    a.append(row)
                    break
            except ValueError:
                pass
            print(f"유한한 숫자 {n}개를 공백으로 구분해 입력하세요.")
    return a


def show(a):
    for row in a:
        print("[ " + " ".join(f"{x:8.3f}" for x in row) + " ]")


def minor(a, row, col):
    return [r[:col] + r[col + 1:] for r in a[:row] + a[row + 1:]]


def determinant(a):
    if len(a) == 1:
        return a[0][0]
    if len(a) == 2:
        return a[0][0] * a[1][1] - a[0][1] * a[1][0]
    total = 0
    for j in range(len(a)):
        total += (-1) ** j * a[0][j] * determinant(minor(a, 0, j))
    return total


def transpose(a):
    return [[a[j][i] for j in range(len(a))] for i in range(len(a))]


def inverse_det(a):
    d = determinant(a)
    if abs(d) < EPS:
        return None
    n = len(a)
    if n == 1:
        return [[1 / d]]
    cofactors = []
    for i in range(n):
        row = []
        for j in range(n):
            row.append((-1) ** (i + j) * determinant(minor(a, i, j)))
        cofactors.append(row)
    adj = transpose(cofactors)
    return [[adj[i][j] / d for j in range(n)] for i in range(n)]


def inverse_gj(a):
    n = len(a)
    b = [a[i][:] + [int(i == j) for j in range(n)] for i in range(n)]
    print("초기 확대행렬 [A | I]:")
    show(b)
    for col in range(n):
        pivot = col
        while pivot < n and abs(b[pivot][col]) < EPS:
            pivot += 1
        if pivot == n:
            print(f"{col + 1}열에 피벗이 없습니다.")
            return None
        if pivot != col:
            b[col], b[pivot] = b[pivot], b[col]
            print(f"행 교환: {col + 1}행 <-> {pivot + 1}행")
        value = b[col][col]
        for j in range(2 * n):
            b[col][j] /= value
        for row in range(n):
            if row != col:
                value = b[row][col]
                for j in range(2 * n):
                    b[row][j] -= value * b[col][j]
        print(f"{col + 1}열 처리 후:")
        show(b)
    return [row[n:] for row in b]


def same(a, b):
    for i in range(len(a)):
        for j in range(len(a)):
            if abs(a[i][j] - b[i][j]) > 1e-8:
                return False
    return True


def check_inverse(a, b):
    n = len(a)
    product = [[0.0 for j in range(n)] for i in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                product[i][j] += a[i][k] * b[k][j]
    identity = [[int(i == j) for j in range(n)] for i in range(n)]
    return same(product, identity)


def main():
    print("[1/4] 행렬 입력")
    a = read_matrix()
    print("입력 행렬:")
    show(a)

    print("\n[2/4] 행렬식 방법")
    print("det(A) =", determinant(a))
    first = inverse_det(a)
    if first is None:
        print("오류: 역행렬이 없습니다(허용오차 기준).")
    else:
        show(first)

    print("\n[3/4] 가우스-조던 방법")
    second = inverse_gj(a)
    if second is None:
        print("오류: 역행렬이 없습니다(허용오차 기준).")
    else:
        print("역행렬:")
        show(second)

    print("\n[4/4] 결과 비교")
    if first is None or second is None:
        print("계산된 역행렬이 없어 값을 비교할 수 없습니다.")
    else:
        print("두 결과 일치(오차 1e-8 이내):", same(first, second))
        print("추가 검증 A * 역행렬 = I:")
        print("행렬식 방법:", check_inverse(a, first))
        print("가우스-조던 방법:", check_inverse(a, second))


if __name__ == "__main__":
    main()
