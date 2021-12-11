import java.io.File

val grid = File("9.in").readLines().map { l -> l.map { it.toString().toInt() }.toMutableList() }

fun List<List<Int>>.lower(r: Int, c: Int, than: Int) = (getOrNull(r)?.getOrNull(c) ?: 10) > than

val lowPoints = grid.flatMapIndexed { r, row ->
    row.mapIndexed { c, cell ->
        c to (grid.lower(r - 1, c, cell) && grid.lower(r + 1, c, cell) && grid.lower(r, c - 1, cell) && grid.lower(r, c + 1, cell))
    }.filter { it.second }.map { r to it.first }
}

fun flood(r: Int, c: Int): Int {
    val cell = grid.getOrNull(r)?.getOrNull(c) ?: return 0
    if (cell == 9) return 0
    grid[r][c] = 9
    return 1 + flood(r - 1, c) + flood(r + 1, c) + flood(r, c - 1) + flood(r, c + 1)
}

lowPoints.map { flood(it.first, it.second) }.sortedDescending().take(3).reduce(Int::times)