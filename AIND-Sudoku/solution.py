assignments = []

def cross(A, B):
    return [a+b for a in A for b in B]

rows = 'ABCDEFGHI'
cols = '123456789'
# boxes는 행과 열의 교차점에 있는 개별 상자이며, cross함수로 생성하여 할당
# units는 전체의 3 x 3 정사각형, 행, 열의 단위이며 총 27개의 boxes가 존재
# 전체 상자 9개, 행 9개, 열 9개 = 27개
# peers는 하나의 값이 units에 생성될 때, 하나의 행과, 하나의 열, 그리고 하나의 박스에 이 숫자
# 외에 동일한 숫자가 있으면 안되는 것을 검사, 총 20개의 boxes가 존재
boxes = cross(rows, cols) # ['A1', 'A2',...,'I9']

# 행을 생성함 [['A1', 'A2',...'A9'], ['B1', 'B2',...,'B9'],..., ['I1',...,'I9']]
row_units = [cross(r, cols) for r in rows]

# 열을 생성함 [['A1', 'B1', 'C1', 'D1', 'E1', 'F1', 'G1', 'H1', 'I1'],...,[]]
column_units = [cross(rows, c) for c in cols]

# print([x+y for x in 'ABCD' for y in '1'])
# 3 x 3 상자 총 9개를 구성 [['A1', 'A2', 'A3', 'B1', 'B2', 'B3', 'C1', 'C2', 'C3'],...,[]]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]

# cols 역방향 [::-1]
# 대각선 만들기
left_units = [[rows[i]+cols[i] for i in range(len(rows))]]
right_units = [[rows[i]+sorted(cols, reverse=True)[i] for i in range(len(rows))]]

# 전체 행, 열, 상자의 합 = 27
# unitlist = row_units + column_units + square_units
# Dictionary를 생성하고, 각 key값에 해당 행, 열, 상자를 생성 9*9=81개의 값을 생성
# 각 boxess는 27개의 리스트(행,열,상자)
unitlist = row_units + column_units + square_units + left_units + right_units

units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)


def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """
    if values[box] == value:
        return values

    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values


def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """
    # 똑같은 값을 묶어 할당
    # 각 피어와 비교하여 값을 리스트로 묶음

    for unit in unitlist:
        # unit에서 values == 2 인 것 찾기
        unit_twins = [u for u in unit if len(values[u]) == 2]
        # peer에서 values == 2 인 것 찾기(twins discover in peer)
        peer_twins = [u for u in unit_twins for p in peers[u] if len(values[u]) and values[u] == values[p]]
        # peers 와 units에서 1차 처리하기
        twins_discovered = [u for u in unit_twins for p in peer_twins if len(unit_twins) >= 2 and len(peer_twins) >=2 and u != p and values[u] == values[p]]
        # 중복값을 없애기 위해 set() 함수로 중복 값 처리
        naked_twins = set(twins_discovered)
        # set() - set() 함수로 분류하기 none_twins와 현재 unit 간에서
        # seperate twins and unit duplicate key values to eliminate
        none_twins = unit.copy()

        for i in naked_twins:
            for n in none_twins:
                if i == n:
                    none_twins.remove(i)

        # values값에 none_twins에 대한 값을 ''처리하기
        # print(none_twins)
        for box in naked_twins:
            # eliminate 와 똑같이 하기
            for digit in values[box]:
                for none in none_twins:
                    # none_twins의 values length가 1이상인 값을
                    # values > 1 1은 이미 solution이나 default values
                    if len(values[none]) > 1:
                        values = assign_value(values, none, values[none].replace(digit, ''))

        # def eliminate(values)
        # for box in solved_values:
        #     digit = values[box]
        #     for peer in peers[box]:
        #         # a.replace(s, r) → 문자열 a의 s라는 문자열을 r이라는 문자열로 치환한다.
        #         assign_value(values, peer, values[peer].replace(digit,''))
    return values



def grid_values(grid):
    """Convert grid string into {<box>: <value>} dict with '123456789' value for empties.

    Args:
        grid: Sudoku grid in string form, 81 characters long
    Returns:
        Sudoku grid in dictionary form:
        - keys: Box labels, e.g. 'A1'
        - values: Value in corresponding box, e.g. '8', or '123456789' if it is empty.

    grid_values(): 는 boxes의 총 81개에 에 각각의 값을 넣어줌
    이면 그 자리에 '123456789'의 숫자를 다 할당
    """
    values = []
    all_digits = '123456789'
    for c in grid:
        if c == '.':
            values.append(all_digits)
        elif c in all_digits:
            values.append(c)
    assert len(values) == 81
    return dict(zip(boxes, values))


def display(values):
    """
    Display the values as a 2-D grid.
    Input: The sudoku in dictionary form
    Output: None
    """
    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    print


def eliminate(values):
    # for loop을 사용하기 위해 dintionary key 값을 리스트로 묶는다. 총 81개
    solved_values = [box for box in values.keys() if len(values[box]) == 1]

    for box in solved_values:
        digit = values[box]
        for peer in peers[box]:
            # a.replace(s, r) → 문자열 a의 s라는 문자열을 r이라는 문자열로 치환한다.
            values = assign_value(values, peer, values[peer].replace(digit,''))
            # 즉, 1개의 기본값이 중복되어있는 모든 peer에 대해 공백을 만들어서 다 제거해버린다. A1에 1이라는 고정값이고 A2에 123456789가 있으면
            # 1을 제거하고 ''으로 처리한다음 23456789만 남김.
    return values

def only_choice(values):

    for unit in unitlist:
        for digit in '123456789':
            dplaces = [box for box in unit if digit in values[box]]

            if len(dplaces) == 1:
                values = assign_value(values, dplaces[0], digit)

    return values


def reduce_puzzle(values):
    """
    Iterate eliminate() and only_choice(). If at some point, there is a box with no available values, return False.
    If the sudoku is solved, return the sudoku.
    If after an iteration of both functions, the sudoku remains the same, return the sudoku.
    Input: A sudoku in dictionary form.
    Output: The resulting sudoku in dictionary form.
    """
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    stalled = False

    while not stalled:
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
        display(values)
        values = eliminate(values)
        values = only_choice(values)
        values = naked_twins(values)

        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        stalled = solved_values_before == solved_values_after

        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values


def search(values):
    "Using depth-first search and propagation, create a search tree and solve the sudoku."
    values = reduce_puzzle(values)
    if values == False:
        return False

    if all(len(values[s]) == 1 for s in boxes):
        return values

    n,s = min((len(values[s]), s) for s in boxes if len(values[s]) > 1)
    for value in values[s]:
        new_sudoku = values.copy()
        new_sudoku[s] = value
        attempt = search(new_sudoku)
        if attempt:
            return attempt


def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    values = grid_values(grid)
    values = search(values)

    return values

if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    values = grid_values(diag_sudoku_grid)
    display(values)
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
