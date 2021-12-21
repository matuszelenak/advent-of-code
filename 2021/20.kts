import java.io.File

val steps = 50

var (algo, grid) = File("20.in").readLines().let { content ->
    content.first() to content.drop(2).map { it.toMutableList() }
}

repeat(steps) {
    val currentVoid = if (it.mod(2) == 0) '.' else '#'
    val newGrid = List(grid.size + 2) { MutableList(grid[0].size + 2) { 'X' } }
    (newGrid.indices).forEach { newY ->
        (0 until newGrid[0].size).forEach { newX ->
            val algoIndex = (-1..1).flatMap { dy ->
                (-1..1).map { dx ->
                    grid.getOrNull(newY + dy - 1)?.getOrNull(newX + dx - 1) ?: currentVoid
                }
            }.joinToString("").replace('.', '0').replace('#', '1').toInt(2)

            newGrid[newY][newX] = algo[algoIndex]
        }
    }
    grid = newGrid
}
grid.flatten().count { it == '#' }